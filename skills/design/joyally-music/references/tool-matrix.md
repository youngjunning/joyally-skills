# 音乐工具矩阵

本矩阵用于选型，不要求安装全部项目。采用前从官方仓库和目标权重核对维护状态、许可证、设备和输出条款；仓库 Star、开源代码和免费试用都不是商用授权。

## 音乐与音效生成

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [AudioCraft](https://github.com/facebookresearch/audiocraft) | MusicGen、AudioGen、EnCodec 的研究与本地实验 | 代码为 MIT，但官方模型权重为 CC-BY-NC 4.0；不能把代码许可推广到商用生成 |
| [stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools) | 训练、微调和推理生成式音频模型 | 工具代码为 MIT；下载权重、数据集和生成服务条款分别核对 |
| [Jukebox](https://github.com/openai/jukebox) | 研究早期端到端音乐生成和条件建模 | 仓库归档、推理很慢且采用 Noncommercial Use License；只作历史研究参考 |

## 歌声合成与音色

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [DiffSinger](https://github.com/openvpi/DiffSinger) | 歌词、音符/MIDI 驱动的可控歌声合成 | 声库、数据集和模型的许可独立于框架 |
| [YingMusic-Singer](https://github.com/GiantAILab/YingMusic-Singer) | 参考音色、歌词与 MIDI/旋律音频驱动的零样本歌声合成 | V1 代码 MIT、官方权重 CC-BY-NC-4.0；本地适配与运行方法见 [接入说明](yingmusic-singer.md)，声音相似度与自然度仍需短样盲听 |
| [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) | 已有演唱的音色转换 | 不负责作曲、歌词或旋律生成；音色身份由 `joyally-voice` 授权 |
| [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc) | Singing Voice Conversion 研究与旧工程回看 | 仓库归档且 AGPL；新项目优先评估仍维护方案 |
| [DDSP-SVC](https://github.com/yxlllc/DDSP-SVC) | 低延迟歌声转换、F0 与音色实验 | 目标音色授权和分离质量决定可用性 |

## 分轨、转录与可编辑素材

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [Demucs](https://github.com/facebookresearch/demucs) | 人声、鼓、贝斯和其他 stems 分离 | 官方仓库已归档；分离结果需听伪影与串音 |
| [Ultimate Vocal Remover GUI](https://github.com/Anjok07/ultimatevocalremovergui) | 通过 GUI 比较和组合多种分离模型，官方说明支持 Apple Silicon MPS | 仓库元数据标 MIT 但顶层许可文本需确认；内置模型也分别核权 |
| [Basic Pitch](https://github.com/spotify/basic-pitch) | 轻量音频转 MIDI、音高与 pitch bend 提取 | 转录是可编辑起点，不保证复原复杂多音轨编曲 |

## 组合建议

1. 配乐探索：生成模型做多个短候选，选定主题后用 DAW 或可编辑 stems 完成结构与混音。
2. 虚拟歌手：歌词与 MIDI 先进入 DiffSinger 类 SVS；如需授权音色，再由 Voice Conversion 处理。
3. Remix：优先原始 multitrack；只有拿不到时用 Demucs/UVR 分离，并在独奏和全混中复听伪影。
4. 旋律回收：Basic Pitch 生成 MIDI 后人工校正节奏、音高、连音和 pitch bend，再重配器。
5. 历史研究：Jukebox、归档 SVC 项目用于理解路线，不作为默认生产依赖。
