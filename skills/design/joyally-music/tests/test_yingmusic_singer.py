import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'yingmusic_singer.py'
spec = importlib.util.spec_from_file_location('yingmusic_adapter', SCRIPT)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


@unittest.skipUnless(importlib.util.find_spec('torch'), 'Run with the model environment')
class AttentionContract(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
