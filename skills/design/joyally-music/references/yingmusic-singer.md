# YingMusic-Singer V1 本地接入

用于从参考音色、参考逐字稿、目标歌词和 MIDI/旋律音频重新生成歌唱。保留现有演唱只换音色时选择 SVC；普通 TTS 不提供这里的旋律控制。人声身份和用途先按 Joyally Voice 确认。

## 固定版本与权利

- [官方代码](https://github.com/GiantAILab/YingMusic-Singer)：revision `6d7c453781cdaf286227ba7a51e79d57b19fad71`，MIT。
- [官方权重](https://huggingface.co/GiantAILab/YingMusic-Singer)：revision `8368debf7ec29754be883eda0ffb905ff098a18b`，模型卡标为 **CC-BY-NC-4.0**。代码许可不覆盖权重；本接入用于非商业实验，不把试验输出直接升级为商用可发布资源。
- 上游建议参考音频约 5–7 秒，参考加生成段落不超过 45 秒；本入口检查时长并拒绝覆盖已有结果。
- 参考音域与目标旋律差别较大时先调整调性，不能只靠提高 CFG 解决。

## 安装独立运行环境

需要 Python 3.12、uv、FFmpeg，以及中文发音处理使用的 eSpeak NG（macOS 可使用 `brew install espeak-ng`）。锁文件包含 PyWORLD 0.3.5，并固定 setuptools 80.9.0 以兼容它使用的 pkg_resources。代码、环境和约 2.8 GB 权重保存在技能目录之外，避免进入 Git 或公开附件。

以下 `music_skill_dir` 指当前加载的本 Skill 根目录；`singer_runtime` 是可自行指定的运行目录。

```bash
singer_runtime="$HOME/.local/share/joyally-music/yingmusic-singer-v1"
mkdir -p "$singer_runtime"
git clone https://github.com/GiantAILab/YingMusic-Singer.git "$singer_runtime/engine"
git -C "$singer_runtime/engine" checkout 6d7c453781cdaf286227ba7a51e79d57b19fad71
uv venv --python 3.12 "$singer_runtime/venv"
uv pip sync --python "$singer_runtime/venv/bin/python" "$music_skill_dir/references/yingmusic-singer.lock.txt"
```

只下载 V1 必需文件，排除 beta：

```bash
"$singer_runtime/venv/bin/python" - "$singer_runtime/weights" <<'PY'
import sys
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="GiantAILab/YingMusic-Singer",
    revision="8368debf7ec29754be883eda0ffb905ff098a18b",
    local_dir=sys.argv[1],
    allow_patterns=["README.md", "singer.v1.pt", "autoencoder_music_dsp1920.ckpt",
                    "stable_audio_1920_vae.json", "rmvpe.pt", "some.pt"],
)
PY
```

## 生成短样

参考逐字稿和歌词分别保存为 UTF-8 文本文件，参考音频使用干净的 WAV。首次用短句跑通，再扩展到 15–30 秒核心段。示例路径为占位文件，不是自带测试数据。

```bash
"$singer_runtime/venv/bin/python" "$music_skill_dir/scripts/yingmusic_singer.py" \
  --engine-root "$singer_runtime/engine" \
  --checkpoint "$singer_runtime/weights" \
  --reference reference.wav --reference-text-file reference.txt \
  --lyrics-file lyrics.txt --midi melody.mid \
  --device cpu --steps 32 --cfg 4 --seed 2025 \
  --output output/candidate.wav
```

旋律音频模式把 `--midi melody.mid` 换成 `--melody-audio melody.wav`；优先干声旋律，混合伴奏可能干扰提取。`--pitch-shift` 以半音调整旋律。CUDA 环境可显式传 `--device cuda`；本入口使用 PyTorch SDPA，不要求 FlashAttention。MIDI 当前只接受单声部、无非零 pitch-bend 的旋律；多声部和弯音先导出为旋律音频。

默认在神经模型生成后进行连续 F0 保音处理；传 `--no-melody-lock` 可生成不校音的对照。原始模型输出始终另存为 `.raw.wav`，不能把校音后的结果称为模型原生音准。

## 兼容性处理

上游 decoder 直接调用带 CUDA 断言的 FlashAttention，不能仅省略其安装就宣称 CPU 可运行。本入口在进程内替换该函数为 SDPA，保留输入布局、有效长度、scale 和因果遮罩，不改模型权重或上游工作区。数值契约测试使用实际 PyTorch 运算。

锁定的 LangSegment 0.2.0 包初始化器导出不存在的 `setLangfilters`，导致导入失败。入口仅在版本与异常匹配时加载该发行包原有实现模块，保留其 `setfilters`/`getTexts` 接口；其他导入错误继续报出。

Apple Silicon 先使用 CPU；上游含 float64/复数与 CUDA 特定代码，MPS 未验收，不把硬件支持 MPS 等同于整个模型支持。入口用 SoundFile 读取音频，再使用 torchaudio 重采样，保持上游的单声道化和 48 kHz 双声道输入约定，避开本机 TorchCodec 动态库加载失败；输入格式以 SoundFile 支持范围为准，其他格式先用 FFmpeg 转 WAV。

## 旋律保持

参考音频的 SOME 旋律序列、100 Hz MIDI 序列和 25 Hz VAE latent 不是同一时钟。分别将参考段和目标段对齐到各自的 latent 帧数，再加入 2 帧条件间隔，避免把不同长度单位拼接后整体缩放。输出裁掉参考与条件间隔，使目标时间零点与旋律输入一致。

冻结的 Singer 权重在裸 MIDI 条件下仍会出现系统音高偏移。单独修正 SOME 频带能改善读数，但实测没有消除 Singer 的生成偏移；运行保留 checkpoint-native 编码。生成后用 PyWORLD 分析候选的谱包络与非周期成分，再以目标旋律的连续 F0 重合成；音频导唱保留其滑音和颤音，MIDI 以音符为中心保留少量候选颤音。共同有声帧之外保留候选的清辅音与呼吸，不把所有时间点强行改为有声音。

该处理会重建中心声像的人声，不保证逐样本保留原立体声相位。超过 8 半音的修正只允许少量检测离群帧；超过共同有声帧的 5% 时拒绝继续，应先检查时间对齐和调性。音高约束不能保证音素起止、歌词完整性或本人音色相似度，仍须分别验收。

## 验收与产物

输出 48 kHz、24-bit WAV、32-bit float 原始人声 `.raw.wav` 和同名 `.manifest.json`。manifest 记录输入哈希、实际代码 revision、适配器哈希、权重哈希、PyTorch/Python 版本、参数、时间轴、保音方法及修正幅度，区分初始化、神经推理和保音耗时；状态保持 `technical-validation`。它可能包含私人输入路径，应与录音一起受控保存。

技术通过后，再与同一句的基线盲听比较歌词完整性、旋律、音色、呼吸与收尾；用官方样例跑通不能证明克隆像本人，也不证明整首歌自然。参考录音缺失时说明实际采用的参考身份，等待原始素材再完成个人音色验收。

## 本地验收范围（2026-11-22）

Apple Silicon、48 GB 内存、Python 3.12.13、PyTorch 2.9.1 上已实际生成 48 kHz 双声道 WAV：MIDI 输入 16/64 步得到约 5.4 秒短句，旋律音频输入 32 步得到约 5.48 秒短句。三段的离线 Whisper 检查均识别到完整目标歌词。适配器的注意力遮罩、scale、因果约束与音频预处理共 3 项数值测试通过。

初版裸 MIDI 的六音符短样中位音高偏差为约 448 音分；保音处理后，同一音符时段的中位偏差为约 0.9 音分。另一个授权参考录音生成的 18 秒副歌，以独立 RMVPE 比较共同有声帧：中位绝对偏差从约 75 音分降到 3.5 音分，约 99% 的比较帧在 100 音分内；最佳全局延迟为 0 ms。该比较只覆盖共同有声帧，不证明每个字都完全同拍，也不把两个不同样本的指标混为一次提升。

验收是“时间轴修复加生成后连续 F0 约束”的结果，原生神经模型的裸 MIDI 偏移没有被重新训练消除。本人音色相似度、自然度盲听、CUDA 和 MPS 尚未验收，成品仍需用户试听。自动检查不能代替听校。
