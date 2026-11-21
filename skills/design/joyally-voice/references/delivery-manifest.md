# 人声交付清单

在项目约定的资产或交付目录保存一个 JSON/YAML manifest；没有约定时使用 `voice-manifest.json`。它用于复现和验收，不保存私密参考音频、授权原文或凭据，只保存受控位置的引用和范围摘要。

```json
{
  "version": 1,
  "status": "sample | technical-validation | publishable | published",
  "operation": "recording | tts | voice-clone | voice-conversion | singing-voice-conversion | restoration | transcription",
  "inputs": [
    {"id": "ref-voice", "sha256": "...", "controlledRef": "授权存储中的稳定引用", "transcript": "文本文件路径或 null"}
  ],
  "authorization": {
    "subject": "本人、权利人或虚构音色",
    "scope": "允许的用途、渠道、期限、训练与再授权范围摘要",
    "evidenceRef": "受控授权记录引用"
  },
  "voiceProfile": {
    "voiceId": "history-narrator",
    "version": 1,
    "promptArtifact": {"controlledRef": "受控位置", "sha256": "...", "format": "模型专用格式或 null"},
    "referenceAudioSha256": "...",
    "referenceTranscriptSha256": "...",
    "identityInputsFrozen": true
  },
  "model": {"name": "...", "codeVersion": "...", "weights": "...", "licenseCheckedAt": "YYYY-MM-DD"},
  "generation": {"seed": null, "parameters": {}, "textNormalization": "规则或文件路径"},
  "outputs": [
    {"path": "...wav", "sha256": "...", "durationSeconds": 0, "integratedLufs": 0, "truePeakDbtp": 0}
  ],
  "timing": {"transcript": "...", "words": "...json", "subtitles": "...srt"},
  "review": {"content": "pass | fail", "performance": "pass | fail", "identity": "pass | fail | not-applicable", "audio": "pass | fail", "reviewer": "...", "notes": "..."},
  "consistency": {
    "profileReloadedInFreshProcess": false,
    "regressionSet": "固定回归文本与基线输出的受控引用",
    "result": "pass | fail | not-run",
    "comparedWithVersion": "history-narrator@v0 或 null"
  }
}
```

字段未知时写 `null` 或明确状态，不编造。克隆任务只有在 prompt/profile 已保存并从新进程回载生成后，才能把 `profileReloadedInFreshProcess` 写为 `true`；仅重新读取同一进程内对象不算。重新生成后更新输出摘要和 review；已发布状态还需记录真实发布入口或所属发布记录。
