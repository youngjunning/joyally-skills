# 社区音频项目核对：声音克隆、歌声转换与素材处理

核对日期：2026-11-21。范围来自用户提供的十张项目截图。状态、用途和许可只依据各项目官方 GitHub 仓库、官方 README、许可证文件与官方模型卡；截图中的 stars、许可和“一句话定位”不作为事实来源。

## 先说结论

这十个项目不是十个“声音克隆方案”。它们分属五条不同链路：

- **音色转换 / 歌声转换**：RVC、so-vits-svc、DDSP-SVC。输入必须先有说话或演唱音频，它们把音色迁移到训练出的目标音色；不是输入文字直接生成声音的 TTS。
- **歌声合成**：DiffSinger。由歌词、音符等条件合成歌声，适合虚拟歌手，不等于日常说话声音克隆。
- **人声与伴奏分离**：Ultimate Vocal Remover、Demucs。用于准备训练素材和后期清理，不生成或克隆声音。
- **音乐/音频生成与转录**：AudioCraft、stable-audio-tools、Jukebox、Basic Pitch。它们分别面向音乐/音效生成或 audio-to-MIDI，不是目标说话人克隆。

因此，`joyally-voice` 应把“说话声音克隆 TTS”和“已有音频的音色转换”拆成两个模式，再把音源分离作为前处理。仅依靠这十个仓库无法完整解决高质量中文说话声音克隆；需要另选专门的 speech TTS / zero-shot voice cloning 模型。

## 逐项核对

| 项目 | 官方定位与当前状态 | 许可核对 | 与声音克隆的关系 | 采用建议与风险 |
| --- | --- | --- | --- | --- |
| [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) | 官方描述是可用不超过约 10 分钟语音训练 voice conversion 模型；仓库未归档，2026-08 仍有提交。当前安装主文档明显以 NVIDIA CUDA 为主。 | 代码 [MIT](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)；训练数据、下载模型和输出音频仍各自受权利约束。 | **直接相关，但属于 VC**：适合把现有说话/歌声音频转换成目标音色，不是文字转语音。 | 可作为 `convert` 候选；先验证 Apple Silicon 实际后端和实时率，不能因 WebUI 可启动就宣称可用。只允许授权声音与数据。 |
| [svc-develop-team/so-vits-svc](https://github.com/svc-develop-team/so-vits-svc) | 官方明确是 Singing Voice Conversion，并明确“不支持 TTS”；仓库已归档，默认分支最后推送于 2023-11。 | [AGPL-3.0](https://github.com/svc-develop-team/so-vits-svc/blob/4.1-Stable/LICENSE)。README 还要求处理训练数据授权，并对公开视频标明输入源。 | **直接相关，但只适合 SVC**。保留原音高与语调，把演唱转换到训练音色。 | 只作为兼容/研究候选，不作为新工作流默认；归档状态与 AGPL 会提高长期维护和分发成本。 |
| [Anjok07/ultimatevocalremovergui](https://github.com/Anjok07/ultimatevocalremovergui) | 官方 README 将其定义为用深度模型移除/分离人声的 GUI；未归档，支持 Apple Silicon 的 MPS 加速和 macOS 安装包。 | GitHub 仓库元数据识别为 MIT，但官方树中未发现可回读的顶层 LICENSE 文件；在重新分发代码或打包前应视为**许可文本待确认**。内置/下载分离模型也可能有各自许可。 | **前处理**：从歌曲中提取人声或伴奏，为合法授权的数据清理和后期制作服务。 | 可作为本机 GUI 辅助，但自动化技能优先调用可复现的 CLI；不要把分离结果误称为干声或无版权素材。 |
| [facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft) | AudioGen、MusicGen、EnCodec、MAGNeT、JASCO 等音频生成/编解码研究库；未归档，2026-03 仍有提交。 | 代码 [MIT](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE)，官方 README 明确模型权重为 [CC-BY-NC 4.0](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights)。 | **不属于声音克隆**。可生成音乐/音效或提供 codec 研究能力。 | 不作为 `joyally-voice` 核心；权重非商业许可会直接限制商业视频使用，代码许可不能替代权重许可。 |
| [facebookresearch/demucs](https://github.com/facebookresearch/demucs) | 官方定位为音乐源分离，可拆 vocals、drums、bass、other；仓库已归档，最后推送于 2024-04。 | [MIT](https://github.com/facebookresearch/demucs/blob/main/LICENSE)；训练数据与输入音乐的权利另行判断。 | **前处理**：可提取人声用于授权数据清理或混音。 | 可作为稳定 CLI 兼容层，但官方仓库已归档；新集成可优先比较仍维护的 UVR/分离后端。 |
| [openvpi/DiffSinger](https://github.com/openvpi/DiffSinger) | 高保真、可控的 Singing Voice Synthesis，支持音高、能量、气声等控制；未归档，2026-11-19 仍有提交。 | [Apache-2.0](https://github.com/openvpi/DiffSinger/blob/main/LICENSE)。README 明确禁止未经同意生成他人声音。 | **歌声合成相关**：从乐谱/歌词等生成演唱，不是普通旁白克隆。 | 可作为未来 `sing` 专项，不进入首版说话克隆主路径；训练、数据准备和发音字典成本高。 |
| [Stability-AI/stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools) | 条件音频生成模型的训练与推理工具箱；未归档，2026-11 仍有提交。 | 代码 [MIT](https://github.com/Stability-AI/stable-audio-tools/blob/main/LICENSE)；官方示例权重 `stable-audio-open-1.0` 是受限访问模型，必须另行接受模型条款。 | **不属于声音克隆**，主要服务音乐/声音生成模型。 | 不放进首版；必须把“代码许可”和“具体模型许可/访问条款”分开验收。 |
| [spotify/basic-pitch](https://github.com/spotify/basic-pitch) | 轻量 Automatic Music Transcription，把音频转成带 pitch bend 的 MIDI；未归档，最后推送于 2025-11。官方说明单一乐器效果最好，并提供 CoreML、TFLite、ONNX 等运行时。 | [Apache-2.0](https://github.com/spotify/basic-pitch/blob/main/LICENSE)。 | **不属于声音克隆**。可从旋律素材提取 MIDI，辅助歌声/音乐工作流。 | 作为可选 `analyze` 工具收藏，不进入声音克隆核心依赖。 |
| [openai/jukebox](https://github.com/openai/jukebox) | 研究型音乐生成模型；README 明确标注 Archive，仓库也已归档，不再预期更新。官方示例称 V100 上生成 20 秒可能需要约 3 小时。 | [Noncommercial Use License](https://github.com/openai/jukebox/blob/master/LICENSE)，软件和生成内容均不得商用。 | **不属于声音克隆**；歌词条件音乐生成也不能等价为可控目标音色克隆。 | 只保留历史研究价值，不纳入实际技能执行路径；归档、旧 CUDA/PyTorch 栈、极慢推理和非商用限制均不适合当前生产。 |
| [yxlllc/DDSP-SVC](https://github.com/yxlllc/DDSP-SVC) | 官方定位为实时、端到端 Singing Voice Conversion；未归档，2026-11 仍有提交。README 表示其硬件需求低于 so-vits-svc，但当前示例训练配置仍以 RTX 4060/CUDA 为参照。 | [MIT](https://github.com/yxlllc/DDSP-SVC/blob/6.3/LICENSE)；README 要求只使用合法授权数据。 | **直接相关，但属于 SVC**：适合低延迟歌声/变声，不是 TTS。 | 可作为 `convert` 的轻量研究候选；Apple Silicon 与实时采集链路仍需本机实测，不能照搬 CUDA 结论。 |

## 对 `joyally-voice` 的直接约束

1. **先按任务分流**：`clone-tts`（文字生成目标说话人）、`convert`（已有音频改音色）、`sing`（歌声合成/转换）、`separate`（人声伴奏分离）、`evaluate`（相似度、可懂度、伪影和性能）。
2. **首版聚焦中文说话声音克隆**：截图十项只作为资源库和周边能力；RVC 可做转换对照，UVR/Demucs 可做素材前处理，但不能替代专门的 zero-shot TTS。
3. **许可按四层验收**：代码、模型权重、训练/参考音频、生成结果分别核对；“GitHub 免费”与“代码 MIT”都不自动授权克隆真人声音或商用输出。
4. **默认使用本人或明确授权声音**：保存授权范围与样本来源；公开人物、同事、客户等声音必须有可回查授权。输出保留 AI 合成标记和模型/样本追溯。
5. **本机验收不能只看启动**：至少核对中文可懂度、音色相似度、长文本一致性、数字/地名读法、实时系数、峰值内存、是否联网、是否会上传声音，以及重新生成的可复现性。

## 官方来源

- [RVC README](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI#readme) 与 [MIT License](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)
- [so-vits-svc README](https://github.com/svc-develop-team/so-vits-svc/tree/4.1-Stable#readme) 与 [AGPL-3.0](https://github.com/svc-develop-team/so-vits-svc/blob/4.1-Stable/LICENSE)
- [Ultimate Vocal Remover README](https://github.com/Anjok07/ultimatevocalremovergui#readme)
- [AudioCraft README](https://github.com/facebookresearch/audiocraft#readme)、[代码许可](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE) 与 [权重许可](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights)
- [Demucs README](https://github.com/facebookresearch/demucs#readme) 与 [MIT License](https://github.com/facebookresearch/demucs/blob/main/LICENSE)
- [DiffSinger README](https://github.com/openvpi/DiffSinger#readme) 与 [Apache-2.0](https://github.com/openvpi/DiffSinger/blob/main/LICENSE)
- [stable-audio-tools README](https://github.com/Stability-AI/stable-audio-tools#readme)、[MIT License](https://github.com/Stability-AI/stable-audio-tools/blob/main/LICENSE) 与 [Stable Audio Open 模型页](https://huggingface.co/stabilityai/stable-audio-open-1.0)
- [Basic Pitch README](https://github.com/spotify/basic-pitch#readme) 与 [Apache-2.0](https://github.com/spotify/basic-pitch/blob/main/LICENSE)
- [Jukebox README](https://github.com/openai/jukebox#readme) 与 [Noncommercial Use License](https://github.com/openai/jukebox/blob/master/LICENSE)
- [DDSP-SVC README](https://github.com/yxlllc/DDSP-SVC/tree/6.3#readme) 与 [MIT License](https://github.com/yxlllc/DDSP-SVC/blob/6.3/LICENSE)
