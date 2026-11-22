#!/usr/bin/env python3
"""Run upstream YingMusic-Singer with a portable attention backend and local inputs."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time


def load_langsegment():
    """Work around the broken exports in the published LangSegment 0.2.0 initializer."""
    import importlib.metadata
    import importlib.util
    try:
        import LangSegment  # noqa: F401
    except ImportError as error:
        distribution = importlib.metadata.distribution('LangSegment')
        if distribution.version != '0.2.0' or 'setLangfilters' not in str(error):
            raise
        source = distribution.locate_file('LangSegment/LangSegment.py')
        spec = importlib.util.spec_from_file_location('LangSegment', source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules['LangSegment'] = module


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def portable_load_audio(path, target_sr):
    """Match upstream mono/stereo preprocessing without its TorchCodec loader."""
    import soundfile as sf
    import torch
    import torchaudio
    samples, rate = sf.read(path, dtype='float32', always_2d=True)
    audio = torch.from_numpy(samples.T.copy()).mean(dim=0, keepdim=True)
    if target_sr == 48000:
        audio = audio.repeat(2, 1)
    if rate != target_sr:
        audio = torchaudio.functional.resample(audio, rate, target_sr)
    return audio, target_sr


def portable_attention(q, k, v, q_lens=None, k_lens=None, dropout_p=0.0,
                       softmax_scale=None, q_scale=None, causal=False,
                       window_size=(-1, -1), **kwargs):
    """Use PyTorch SDPA with the upstream [batch, time, heads, channels] contract."""
    import torch
    from torch.nn.functional import scaled_dot_product_attention

    if tuple(window_size) != (-1, -1):
        raise ValueError('Sliding-window attention is not supported by this adapter.')
    query, key, value = (x.transpose(1, 2) for x in (q, k, v))
    if q_scale is not None:
        query = query * q_scale
    mask = None
    if k_lens is not None:
        valid = torch.arange(k.shape[1], device=k.device)[None, :] < k_lens[:, None]
        mask = valid[:, None, None, :]
    if causal and mask is not None:
        mask = mask & torch.ones(q.shape[1], k.shape[1], device=q.device,
                                 dtype=torch.bool).tril()[None, None, :, :]
    result = scaled_dot_product_attention(query, key, value, attn_mask=mask,
                                         dropout_p=dropout_p,
                                         is_causal=causal and mask is None,
                                         scale=softmax_scale).transpose(1, 2)
    if q_lens is not None:
        valid = torch.arange(q.shape[1], device=q.device)[None, :] < q_lens[:, None]
        result = result * valid[:, :, None, None]
    return result.contiguous().to(q.dtype)


def align_melody_segments(reference_notes, target_notes, reference_frames, target_frames,
                          gap_frames=2, pitch_shift=0):
    import torch
    from torch.nn.functional import interpolate
    reference = interpolate(reference_notes[:, None].float(), size=reference_frames,
                             mode='nearest')[:, 0]
    target = interpolate(target_notes[:, None].float(), size=target_frames,
                          mode='nearest')[:, 0].to(reference.device)
    voiced = target > 0
    target[voiced] += pitch_shift
    if ((target[voiced] < 1) | (target[voiced] > 127)).any():
        raise ValueError('Pitch shift moved the melody outside MIDI 1–127')
    return torch.cat([reference, torch.zeros(reference.shape[0], gap_frames,
                                           device=reference.device), target], dim=1)


def aligned_inference(singer, *, reference, reference_text, lyrics, midi=None,
                      melody_audio=None, pitch_shift=0, cfg=4., steps=32, seed=2025):
    """Align each melody segment to the 25 Hz latent clock before concatenation."""
    import pretty_midi
    import soundfile as sf
    import torch
    from singer.model import get_notemidi_from_file, seed_everything

    seed_everything(seed)
    reference_features = singer.encode_audio(str(reference), 48000, singer.device).permute(0, 2, 1)
    reference_frames = reference_features.shape[1]
    reference_notes = singer.extract_melody(str(reference))
    if midi is not None:
        duration = pretty_midi.PrettyMIDI(str(midi)).get_end_time()
        target_notes = torch.from_numpy(get_notemidi_from_file(str(midi)))[None].float()
    else:
        duration = sf.info(melody_audio).duration
        target_notes = singer.extract_melody(str(melody_audio))
    target_frames = math.ceil(duration * 25)
    if target_frames < 1 or target_notes.shape[1] < 1:
        raise ValueError('The target melody is empty')
    gap_frames = 2
    combined = align_melody_segments(reference_notes.to(singer.device),
                                     target_notes.to(singer.device), reference_frames,
                                     target_frames, gap_frames, pitch_shift)
    total_frames = reference_frames + gap_frames + target_frames
    text = reference_text.strip() + ' ' + lyrics.strip()
    phonemes = singer.tokenizer.tokenize(text, '', language='auto')[0].split('|')
    features, _ = singer.sample(cond=reference_features, text=[phonemes],
                                duration=total_frames, melody_in=combined, task_tag='singing',
                                steps=steps, text_strength=cfg, sde_strength=0., seed=seed)
    features = features[:, reference_frames + gap_frames:, :].float().permute(0, 2, 1).squeeze(0)
    waveform = singer.vae.decode_audio(features.to(singer.device)).cpu().squeeze(0)
    return waveform, {'version': 1, 'latentFrameHz': 25, 'referenceFrames': reference_frames,
                      'gapFrames': gap_frames, 'targetFrames': target_frames,
                      'outputIncludesConditioningGap': False}


def lock_pitch_to_melody(waveform, sample_rate, *, melody_audio=None, midi=None,
                         pitch_shift=0, max_semitones=8):
    """Resynthesize with the guide's continuous F0 and the candidate's spectral envelope."""
    import numpy as np
    import pretty_midi
    import pyworld
    import soundfile as sf
    import torch
    import torchaudio
    from scipy.ndimage import median_filter

    raw = waveform.detach().cpu().double().numpy()
    if raw.ndim == 1:
        raw = raw[None, :]
    audio = np.ascontiguousarray(raw.mean(0))
    if not np.isfinite(audio).all() or audio.size == 0:
        raise ValueError('The candidate audio is empty or non-finite')
    f0, times = pyworld.harvest(audio, sample_rate, f0_floor=65, f0_ceil=1000,
                                frame_period=5.)
    if not np.any(f0 > 0):
        raise ValueError('No voiced frames in the candidate; melody lock cannot be verified')
    if melody_audio is not None:
        guide, rate = sf.read(melody_audio, always_2d=True, dtype='float64')
        guide = np.ascontiguousarray(guide.mean(1))
        if rate != sample_rate:
            guide = torchaudio.functional.resample(torch.from_numpy(guide), rate,
                                                    sample_rate).numpy()
        target, guide_times = pyworld.harvest(np.ascontiguousarray(guide), sample_rate,
                                               f0_floor=65, f0_ceil=1000, frame_period=5.)
        target = np.interp(times, guide_times, target, left=0., right=0.)
        target *= 2 ** (pitch_shift / 12)
    else:
        score = pretty_midi.PrettyMIDI(str(midi))
        if any(abs(b.pitch) > 0 for inst in score.instruments for b in inst.pitch_bends):
            raise ValueError('Pitch-bend MIDI needs a rendered melody audio guide')
        notes = sorted((n for inst in score.instruments if not inst.is_drum for n in inst.notes),
                       key=lambda n: n.start)
        if any(a.end > b.start + .001 for a, b in zip(notes, notes[1:])):
            raise ValueError('Use a monophonic melody; overlapping MIDI notes are ambiguous')
        target = np.zeros_like(times)
        for note in notes:
            active = (times >= note.start) & (times < note.end)
            target[active] = 440 * 2 ** ((note.pitch + pitch_shift - 69) / 12)
        # Keep small candidate vibrato; the MIDI note supplies the tonal center.
        log_f0 = np.log2(np.maximum(f0, 65))
        ornament = np.clip(12 * (log_f0 - median_filter(log_f0, size=31)), -.18, .18)
        target *= 2 ** (ornament / 12)
    active = (f0 > 0) & (target > 65)
    if not np.any(active):
        raise ValueError('No jointly voiced target frames; refusing an unverifiable melody lock')
    correction = 12 * np.log2(target[active] / f0[active])
    limited_frames = int(np.count_nonzero(abs(correction) > max_semitones))
    if limited_frames > max(3, int(active.sum() * .05)):
        raise ValueError('Too many frames exceed the melody-lock range; check guide alignment and key')
    clipped = np.clip(correction, -max_semitones, max_semitones)
    corrected = f0.copy()
    corrected[active] *= 2 ** (clipped / 12)
    envelope = pyworld.cheaptrick(audio, f0, times, sample_rate)
    aperiodicity = pyworld.d4c(audio, f0, times, sample_rate)
    locked = pyworld.synthesize(corrected, envelope, aperiodicity, sample_rate,
                                 frame_period=5.)[:audio.size]
    rms_raw = float(np.sqrt(np.mean(audio ** 2)))
    rms_new = float(np.sqrt(np.mean(locked ** 2)))
    if rms_new == 0 or not np.isfinite(locked).all():
        raise ValueError('Melody lock produced invalid audio')
    locked *= min(2., rms_raw / rms_new)
    output = torch.from_numpy(np.tile(locked, (raw.shape[0], 1))).float()
    return output, {'algorithm': 'continuous-world-f0-v1', 'pyworld': pyworld.__version__,
                     'framePeriodMs': 5, 'voicedCorrectionSeconds': float(active.sum() * .005),
                     'medianAppliedCents': float(np.median(abs(clipped)) * 100),
                     'limitedFrames': limited_frames,
                     'spectralEnvelopeSource': 'generated-candidate',
                     'targetF0Source': 'melody-audio' if melody_audio else 'midi',
                     'maxCorrectionSemitones': max_semitones}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine-root', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--reference-text-file', type=Path, required=True)
    parser.add_argument('--lyrics-file', type=Path, required=True)
    melody = parser.add_mutually_exclusive_group(required=True)
    melody.add_argument('--midi', type=Path)
    melody.add_argument('--melody-audio', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    parser.add_argument('--steps', type=int, default=32)
    parser.add_argument('--cfg', type=float, default=4.0)
    parser.add_argument('--pitch-shift', type=int, default=0)
    parser.add_argument('--seed', type=int, default=2025)
    parser.add_argument('--threads', type=int, default=6)
    parser.add_argument('--no-melody-lock', action='store_true',
                        help='Save uncorrected model audio for a controlled comparison')
    args = parser.parse_args()
    if args.steps < 1 or args.threads < 1:
        parser.error('--steps and --threads must be positive')
    inputs = [args.reference, args.reference_text_file, args.lyrics_file,
              args.midi or args.melody_audio]
    for path in inputs:
        if not path.is_file():
            parser.error(f'Input does not exist: {path}')
    required = ['singer.v1.pt', 'autoencoder_music_dsp1920.ckpt',
                'stable_audio_1920_vae.json', 'rmvpe.pt', 'some.pt']
    for name in required:
        if not (args.checkpoint / name).is_file():
            parser.error(f'Missing checkpoint file: {name}')
    if not (args.engine_root / 'src/singer/model.py').is_file():
        parser.error('--engine-root must point to the upstream source checkout')
    if args.output.suffix.lower() != '.wav':
        parser.error('--output must be a WAV file')
    manifest_path = args.output.with_suffix('.manifest.json')
    raw_path = args.output.with_suffix('.raw.wav')
    if args.output.exists() or manifest_path.exists() or raw_path.exists():
        parser.error('Output or manifest already exists; choose a new filename')
    if not args.reference_text_file.read_text().strip() or not args.lyrics_file.read_text().strip():
        parser.error('Reference transcript and lyrics must be nonempty')

    import numpy as np
    import soundfile as sf
    import torch

    reference_info = sf.info(args.reference)
    if not 0 < reference_info.duration <= 10:
        parser.error('Use a short reference (upstream recommends 5–7 seconds)')
    if args.melody_audio:
        melody_seconds = sf.info(args.melody_audio).duration
    else:
        import pretty_midi
        melody_seconds = pretty_midi.PrettyMIDI(str(args.midi)).get_end_time()
    if melody_seconds <= 0 or reference_info.duration + melody_seconds > 45:
        parser.error('Reference plus melody must be nonempty and at most 45 seconds')
    if args.device == 'cuda' and not torch.cuda.is_available():
        parser.error('CUDA is unavailable; use --device cpu')
    sys.path.insert(0, str(args.engine_root.resolve() / 'src'))
    torch.set_num_threads(args.threads)
    load_langsegment()
    from singer.decoder import modules
    modules.flash_attention = portable_attention
    from singer import model
    model.load_audio = portable_load_audio

    started = time.perf_counter()
    singer = model.YingSinger(singer_path=str(args.checkpoint.resolve()), device=args.device).eval()
    initialized = time.perf_counter()
    with torch.inference_mode():
        waveform, melody_alignment = aligned_inference(singer,
            reference=args.reference.resolve(),
            reference_text=args.reference_text_file.read_text().strip(),
            lyrics=args.lyrics_file.read_text().strip(),
            melody_audio=args.melody_audio.resolve() if args.melody_audio else None,
            midi=args.midi.resolve() if args.midi else None,
            cfg=args.cfg, steps=args.steps, pitch_shift=args.pitch_shift,
            seed=args.seed)
    neural_finished = time.perf_counter()
    raw_waveform = waveform
    melody_lock = {'applied': False}
    if not args.no_melody_lock:
        waveform, melody_lock = lock_pitch_to_melody(waveform, 48000,
            melody_audio=args.melody_audio, midi=args.midi, pitch_shift=args.pitch_shift)
        melody_lock['applied'] = True
    lock_finished = time.perf_counter()
    generated = waveform.detach().cpu().float().numpy()
    if generated.ndim == 1:
        generated = generated[None, :]
    if not np.isfinite(generated).all() or generated.size == 0:
        raise RuntimeError('The model produced empty or non-finite audio')
    peak = float(np.max(np.abs(generated)))
    if peak == 0:
        raise RuntimeError('The model produced silent audio')
    gain = min(1.0, 0.98 / peak)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists():
        raise FileExistsError(f'Raw comparison already exists: {raw_path}')
    raw_audio = raw_waveform.detach().cpu().float().numpy()
    if raw_audio.ndim == 1:
        raw_audio = raw_audio[None, :]
    sf.write(raw_path, raw_audio.T, 48000, subtype='FLOAT')
    sf.write(args.output, (generated * gain).T, 48000, subtype='PCM_24')
    finished = time.perf_counter()
    revision = subprocess.check_output(['git', '-C', str(args.engine_root),
                                        'rev-parse', 'HEAD'], text=True).strip()
    manifest = {
        'status': 'technical-validation', 'model': 'GiantAILab/YingMusic-Singer V1',
        'adapterSha256': sha256(Path(__file__)),
        'codeRevision': revision, 'weightsLicense': 'CC-BY-NC-4.0',
        'checkpointHashes': {name: sha256(args.checkpoint / name) for name in required},
        'parameters': {'device': args.device, 'attention': 'pytorch-sdpa',
                       'steps': args.steps, 'cfg': args.cfg, 'pitchShift': args.pitch_shift,
                       'seed': args.seed, 'threads': args.threads},
        'melodyAlignment': melody_alignment,
        'melodyFrontend': 'checkpoint-native',
        'melodyLock': melody_lock,
        'rawModelOutput': {'path': str(raw_path.resolve()), 'sha256': sha256(raw_path)},
        'runtime': {'torch': torch.__version__, 'python': sys.version.split()[0]},
        'inputs': [{'path': str(path.resolve()), 'sha256': sha256(path)} for path in inputs],
        'output': {'path': str(args.output.resolve()), 'sha256': sha256(args.output),
                   'sampleRate': 48000, 'seconds': generated.shape[-1] / 48000,
                   'peakBeforeGain': peak, 'gain': gain},
        'timing': {'initializationSeconds': initialized - started,
                   'inferenceSeconds': neural_finished - initialized,
                   'melodyLockSeconds': lock_finished - neural_finished,
                   'totalSeconds': finished - started},
        'review': 'Listening, intelligibility and identity review are still required.'}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'manifest': str(manifest_path),
                      'seconds': manifest['output']['seconds'], 'timing': manifest['timing']}))


if __name__ == '__main__':
    main()
