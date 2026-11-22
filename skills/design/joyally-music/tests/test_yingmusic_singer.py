import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'yingmusic_singer.py'
spec = importlib.util.spec_from_file_location('yingmusic_adapter', SCRIPT)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


@unittest.skipUnless(importlib.util.find_spec('torch'), 'Run with the model environment')
class AttentionContract(unittest.TestCase):
    def test_reference_target_and_gap_use_independent_clocks(self):
        import torch
        reference = torch.full((1, 582), 50.)
        target = torch.cat([torch.full((1, 200), 60.), torch.full((1, 200), 64.)], dim=1)
        actual = adapter.align_melody_segments(reference, target, 169, 100)
        expected = torch.tensor([[50.] * 169 + [0.] * 2 + [60.] * 50 + [64.] * 50])
        torch.testing.assert_close(actual, expected)

    def test_reference_duration_does_not_move_target_notes(self):
        import torch
        reference = torch.full((1, 860), 50.)
        target = torch.tensor([[0., 60., 64., 0.]]).repeat_interleave(100, dim=1)
        for reference_frames in (13, 250):
            actual = adapter.align_melody_segments(reference, target, reference_frames,
                                                    100, pitch_shift=-2)
            expected = torch.tensor([[0.] * 25 + [58.] * 25 + [62.] * 25 + [0.] * 25])
            torch.testing.assert_close(actual[:, reference_frames + 2:], expected)

    def test_audio_loader_downmixes_and_resamples_for_the_vae(self):
        import tempfile
        import numpy as np
        import soundfile as sf
        import torch
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'stereo.wav'
            samples = np.stack([np.full(2400, .2), np.full(2400, .8)], axis=1)
            sf.write(path, samples, 24000, subtype='FLOAT')
            audio, rate = adapter.portable_load_audio(path, 48000)
        self.assertEqual(rate, 48000)
        self.assertEqual(tuple(audio.shape), (2, 4800))
        torch.testing.assert_close(audio[0], audio[1])
        torch.testing.assert_close(audio[:, 100:-100],
                                   torch.full((2, 4600), .5), rtol=.005, atol=.002)

    def test_matches_masked_softmax_in_float32(self):
        import torch
        torch.manual_seed(29)
        q = torch.randn(2, 3, 2, 4)
        k = torch.randn(2, 5, 2, 4)
        v = torch.randn(2, 5, 2, 4)
        lengths = torch.tensor([5, 2])
        queries = torch.tensor([3, 1])
        actual = adapter.portable_attention(q, k, v, k_lens=lengths,
                                             q_lens=queries, q_scale=.8,
                                             softmax_scale=.4)
        scores = torch.einsum('bqhd,bkhd->bhqk', q * .8, k) * .4
        valid = torch.arange(5)[None, :] < lengths[:, None]
        scores = scores.masked_fill(~valid[:, None, None, :], float('-inf'))
        expected = torch.einsum('bhqk,bkhd->bqhd', scores.softmax(-1), v)
        expected[1, 1:] = 0
        torch.testing.assert_close(actual, expected)
        self.assertEqual(actual.dtype, torch.float32)

    def test_causal_keys_are_not_visible_in_the_future(self):
        import torch
        q = torch.zeros(1, 3, 1, 2)
        k = q.clone()
        v = torch.tensor([[[[2., 2.]], [[4., 4.]], [[12., 12.]]]])
        actual = adapter.portable_attention(q, k, v, causal=True,
                                             k_lens=torch.tensor([3]))
        torch.testing.assert_close(actual[0, :, 0, 0], torch.tensor([2., 3., 6.]))


@unittest.skipUnless(importlib.util.find_spec('torch') and importlib.util.find_spec('pyworld'),
                     'Requires the music runtime')
class MelodyLockContract(unittest.TestCase):
    def test_midi_changes_pitch_without_changing_duration(self):
        import tempfile
        import numpy as np
        import pretty_midi
        import torch
        sr = 48000
        t = np.arange(sr * 2) / sr
        source = sum(np.sin(2 * np.pi * 220 * k * t) / k for k in range(1, 9)) * .15
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'target.mid'
            score = pretty_midi.PrettyMIDI()
            inst = pretty_midi.Instrument(0)
            inst.notes.append(pretty_midi.Note(100, 62, 0., 2.))
            score.instruments.append(inst)
            score.write(str(path))
            output, info = adapter.lock_pitch_to_melody(torch.tensor(source[None]).float(),
                                                       sr, midi=path)
        self.assertEqual(tuple(output.shape), (1, len(source)))
        center = output.numpy()[0, sr // 2:sr * 3 // 2]
        spectrum = abs(np.fft.rfft(center * np.hanning(len(center))))
        frequency = np.fft.rfftfreq(len(center), 1 / sr)[np.argmax(spectrum)]
        self.assertLess(abs(frequency - 293.665), 2.)
        self.assertEqual(info['spectralEnvelopeSource'], 'generated-candidate')

    def test_polyphonic_midi_is_rejected(self):
        import tempfile
        import numpy as np
        import pretty_midi
        import torch
        sr = 48000
        t = np.arange(sr) / sr
        audio = sum(np.sin(2 * np.pi * 220 * k * t) / k for k in range(1, 9)) * .15
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chord.mid'
            score = pretty_midi.PrettyMIDI()
            inst = pretty_midi.Instrument(0)
            inst.notes = [pretty_midi.Note(100, n, 0., 1.) for n in (60, 64)]
            score.instruments.append(inst)
            score.write(str(path))
            with self.assertRaisesRegex(ValueError, 'monophonic'):
                adapter.lock_pitch_to_melody(torch.tensor(audio[None]).float(), sr, midi=path)


if __name__ == '__main__':
    unittest.main()
