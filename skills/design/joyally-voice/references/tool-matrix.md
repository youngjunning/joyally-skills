# 人声工具矩阵

本表用于选型，不要求安装全部项目。能力、许可证和维护状态应在采用时从官方仓库与目标权重重新核对；代码开源不代表模型权重、训练数据、参考声音或生成结果自动可商用。

## 说话语音生成与克隆

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | 中文/多语言 TTS、预置音色、自然语言控制、零样本克隆；Apple Silicon 可结合 MLX-Audio | CustomVoice 与 Base/克隆模型职责不同；参考音频和文本需匹配 |
| [Ming-3.0-TTS](https://github.com/inclusionAI/Ming-3.0-tts) | 多语言、方言、音色设计、风格和副语言控制 | 各能力分属不同任务模式，先核对能否组合 |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | 参考音频驱动的零样本 TTS、研究和微调 | 目标语言、权重许可和部署设备分别核对 |
| [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | 多语言、跨语言、情绪与低延迟语音生成 | 官方主路径偏 CUDA/Linux 时，Mac 路径先做 POC |
| [IndexTTS](https://github.com/index-tts/index-tts) | 中文音色克隆、情绪和时长控制实验 | 专用模型许可与依赖链需单独评估 |

## 音色转换与歌声身份

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) | 少量数据训练后的说话/歌声音色转换和实时实验 | 主文档偏 CUDA；不从文字生成内容，模型和训练声音另行授权 |
| [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc) | Singing Voice Conversion 研究 | 上游归档且采用 AGPL；新生产链路优先评估仍维护方案 |
| [DDSP-SVC](https://github.com/yxlllc/DDSP-SVC) | 低延迟歌声音色转换、F0 与音色实验 | 示例仍以 CUDA 为主；目标音色和数据仍需授权 |
| [Seed-VC](https://github.com/Plachtaa/seed-vc) | 零样本说话/歌声转换实验 | 仓库维护状态和权重许可采用前复核 |

## 清理、分离、转写与验收

| 工具 | 适合 | 边界 |
| --- | --- | --- |
| [Demucs](https://github.com/facebookresearch/demucs) | 人声/伴奏与多 stem 分离 | 官方仓库已归档；分离产物含伪影，不能自动视为训练干声 |
| [Ultimate Vocal Remover GUI](https://github.com/Anjok07/ultimatevocalremovergui) | 图形化组合多种分离模型，官方说明支持 Apple Silicon MPS | 仓库元数据标 MIT，但顶层许可文本需在分发前确认；内置模型分别核权 |
| FFmpeg / ffprobe | 重采样、切分、响度、真峰值、拼接和格式检查 | 指标不能替代听感、可懂度与身份授权 |
| Whisper、WhisperX、Parakeet | 转写及句词级对齐 | 转写结果必须回读专名、数字和跨语言内容 |

## 选型原则

1. 预置音色能满足目标时，不引入克隆数据与身份风险。
2. 文本生成新内容选 TTS；保留原表演换音色选 VC/SVC；从音符和歌词生成歌声交给 `joyally-music`。
3. 本地设备优先原生支持路径；旧项目、归档项目和社区 fork 只在隔离环境验证。
4. 长期栏目选择稳定版本、固定参数和可回归样本，不按一次最好听的随机结果选型。
