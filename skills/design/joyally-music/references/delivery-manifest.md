# 音乐交付清单

在项目约定的资产或交付目录保存 JSON/YAML manifest；没有约定时使用 `music-manifest.json`。只保存来源、权利范围和受控资产引用，不复制未获公开授权的歌词、录音、授权原文或凭据。

```json
{
  "version": 1,
  "status": "sample | technical-validation | publishable | published",
  "brief": {"purpose": "...", "durationSeconds": 0, "bpm": null, "key": null, "meter": null, "structure": []},
  "sources": [
    {"id": "melody-guide", "sha256": "...", "controlledRef": "...", "rights": "范围摘要"}
  ],
  "modelsAndTools": [
    {"name": "...", "version": "...", "weights": "...", "licenseCheckedAt": "YYYY-MM-DD", "parameters": {}}
  ],
  "melody": {"guide": "...wav", "midi": "...mid", "f0": null, "preservationReview": "pass | intentional-change | not-applicable"},
  "outputs": {
    "master": {"path": "...wav", "sha256": "...", "integratedLufs": 0, "truePeakDbtp": 0},
    "release": "...",
    "stems": [],
    "midi": [],
    "project": null
  },
  "review": {"composition": "pass | fail", "mix": "pass | fail", "targetPlayback": "pass | fail", "rights": "pass | fail", "reviewer": "...", "notes": "..."}
}
```

生成候选不能继承 `publishable` 状态；只有来源、听感、技术和目标播放器验收都通过后才升级。发布后记录真实发布入口或所属发布记录。
