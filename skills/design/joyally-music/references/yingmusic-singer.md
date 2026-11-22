# YingMusic-Singer V1 本地接入

用于从参考音色、参考逐字稿、目标歌词和 MIDI/旋律音频重新生成歌唱。保留现有演唱只换音色时选择 SVC；普通 TTS 不提供这里的旋律控制。人声身份和用途先按 Joyally Voice 确认。

## 固定版本与权利

- [官方代码](https://github.com/GiantAILab/YingMusic-Singer)：revision `6d7c453781cdaf286227ba7a51e79d57b19fad71`，MIT。
- [官方权重](https://huggingface.co/GiantAILab/YingMusic-Singer)：revision `8368debf7ec29754be883eda0ffb905ff098a18b`，模型卡标为 **CC-BY-NC-4.0**。代码许可不覆盖权重；本接入用于非商业实验，不把试验输出直接升级为商用可发布资源。
- 上游建议参考音频约 5–7 秒，参考加生成段落不超过 45 秒；本入口检查时长并拒绝覆盖已有结果。
- 参考音域与目标旋律差别较大时先调整调性，不能只靠提高 CFG 解决。

## 安装独立运行环境

需要 Python 3.12、uv、FFmpeg，以及中文发音处理使用的 eSpeak NG（macOS 可使用 `brew install espeak-ng`）。代码、环境和约 2.8 GB 权重保存在技能目录之外，避免进入 Git 或公开附件。

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

旋律音频模式把 `--midi melody.mid` 换成 `--melody-audio melody.wav`；优先干声旋律，混合伴奏可能干扰提取。`--pitch-shift` 以半音调整旋律。CUDA 环境可显式传 `--device cuda`；本入口使用 PyTorch SDPA，不要求 FlashAttention。

## 兼容性处理

上游 decoder 直接调用带 CUDA 断言的 FlashAttention，不能仅省略其安装就宣称 CPU 可运行。本入口在进程内替换该函数为 SDPA，保留输入布局、有效长度、scale 和因果遮罩，不改模型权重或上游工作区。数值契约测试使用实际 PyTorch 运算。

锁定的 LangSegment 0.2.0 包初始化器导出不存在的 `setLangfilters`，导致导入失败。入口仅在版本与异常匹配时加载该发行包原有实现模块，保留其 `setfilters`/`getTexts` 接口；其他导入错误继续报出。

Apple Silicon 先使用 CPU；上游含 float64/复数与 CUDA 特定代码，MPS 未验收，不把硬件支持 MPS 等同于整个模型支持。入口用 SoundFile 读取音频，再使用 torchaudio 重采样，保持上游的单声道化和 48 kHz 双声道输入约定，避开本机 TorchCodec 动态库加载失败；输入格式以 SoundFile 支持范围为准，其他格式先用 FFmpeg 转 WAV。

## 验收与产物

输出 48 kHz、24-bit WAV 和同名 `.manifest.json`。manifest 记录输入哈希、实际代码 revision、权重哈希、PyTorch/Python 版本、参数、耗时与峰值保护增益，状态保持 `technical-validation`。它可能包含私人输入路径，应与录音一起受控保存。

技术通过后，再与同一句的基线盲听比较歌词完整性、旋律、音色、呼吸与收尾；用官方样例跑通不能证明克隆像本人，也不证明整首歌自然。参考录音缺失时说明实际采用的参考身份，等待原始素材再完成个人音色验收。

## 本地验收范围（2026-11-22）

Apple Silicon、48 GB 内存、Python 3.12.13、PyTorch 2.9.1 上已实际生成 48 kHz 双声道 WAV：MIDI 输入 16/64 步得到约 5.4 秒短句，旋律音频输入 32 步得到约 5.48 秒短句。三段的离线 Whisper 检查均识别到完整目标歌词。适配器的注意力遮罩、scale、因果约束与音频预处理共 3 项数值测试通过。

这些结果仅证明技术链路和该短句的自动可懂度检查通过。MIDI 样本按输入音符时段做自动音高核对时出现数半音偏差，增加到 64 步未明显消除；额外降 6 个半音匹配参考音域的 32 步实验仍有偏差。旋律保持尚未验收，不能以“已出声”推断优于既有 SVC。自动音高检查也不能代替人工对齐与听校。本人音色相似度、自然度盲听、长句与整首歌、CUDA 和 MPS 均未在此记录中验收。
