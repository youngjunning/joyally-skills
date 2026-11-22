#!/usr/bin/env python3
"""Run upstream YingMusic-Singer with a portable attention backend and local inputs."""
import argparse
import hashlib
import json
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
    if args.output.exists() or manifest_path.exists():
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
        waveform = singer.inference(
            timbre_audio_path=str(args.reference.resolve()),
            timbre_audio_content=args.reference_text_file.read_text().strip(),
            lyrics=args.lyrics_file.read_text().strip(),
            melody_audio_path=str(args.melody_audio.resolve()) if args.melody_audio else None,
            midi_file=str(args.midi.resolve()) if args.midi else None,
            cfg_strength=args.cfg, nfe_steps=args.steps, pitch_shift=args.pitch_shift,
            seed=args.seed)
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
    sf.write(args.output, (generated * gain).T, 48000, subtype='PCM_24')
    finished = time.perf_counter()
    revision = subprocess.check_output(['git', '-C', str(args.engine_root),
                                        'rev-parse', 'HEAD'], text=True).strip()
    manifest = {
        'status': 'technical-validation', 'model': 'GiantAILab/YingMusic-Singer V1',
        'codeRevision': revision, 'weightsLicense': 'CC-BY-NC-4.0',
        'checkpointHashes': {name: sha256(args.checkpoint / name) for name in required},
        'parameters': {'device': args.device, 'attention': 'pytorch-sdpa',
                       'steps': args.steps, 'cfg': args.cfg, 'pitchShift': args.pitch_shift,
                       'seed': args.seed, 'threads': args.threads},
        'runtime': {'torch': torch.__version__, 'python': sys.version.split()[0]},
        'inputs': [{'path': str(path.resolve()), 'sha256': sha256(path)} for path in inputs],
        'output': {'path': str(args.output.resolve()), 'sha256': sha256(args.output),
                   'sampleRate': 48000, 'seconds': generated.shape[-1] / 48000,
                   'peakBeforeGain': peak, 'gain': gain},
        'timing': {'initializationSeconds': initialized - started,
                   'inferenceSeconds': finished - initialized},
        'review': 'Listening, intelligibility and identity review are still required.'}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'manifest': str(manifest_path),
                      'seconds': manifest['output']['seconds'], 'timing': manifest['timing']}))


if __name__ == '__main__':
    main()
