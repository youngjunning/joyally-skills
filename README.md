# 俊宁的 Agent Skills

集中维护日常使用的工程、设计、写作与站点建设技能。每个技能保留独立的 `SKILL.md`、参考资料和辅助脚本，可按需安装，更新集中在一个仓库。

俊宁，阿里高级工程师、AI 开发者，拥有 10 年研发经验，现专注 AI 应用、AI 浏览器、Agent、AI Infra 与软件工程。

## 安装

选择需要的技能：

```bash
npx skills add youngjunning/joyally-skills
```

安装单个技能：

```bash
npx skills add youngjunning/joyally-skills --skill joyally-arch -g
```

`skills` CLI 的 Agent 选择与目标位置以安装时显示的选项为准。安装第三方工具不代表本仓库提供其服务、账号或额度。

维护者也可以使用同一个 checkout，通过软链接安装；以后 `git pull` 即可更新源文件：

```bash
git clone https://github.com/youngjunning/joyally-skills.git
cd skills
python3 scripts/link-skills.py --dest ~/.codex/skills --dry-run
python3 scripts/link-skills.py --dest ~/.codex/skills
```

已有同名安装时脚本默认停止；明确需要替换时加 `--replace`，旧内容会先移入本机备份目录。其他 Agent 可显式指定其技能目录，例如 `--dest ~/.claude/skills`。同一个 Agent 使用一种安装方式，避免重复加载。

## 按问题找技能

| 你要解决的问题 | 从这里开始 |
| --- | --- |
| 判断产品方向、渐进推演系统边界或设计 AI Agent 方案 | [joyally-arch](skills/engineering/joyally-arch/SKILL.md) |
| 开发或评审 Agent 驱动的浏览器扩展，避免脚本写死业务流程 | [joyally-browser-extension-dev](skills/engineering/joyally-browser-extension-dev/SKILL.md) |
| 向人说明进展、交付、排障或评审结论 | [joyally-report](skills/engineering/joyally-report/SKILL.md) |
| 设计、实现、运行或治理测试与 AI/Agent evals，判断证据能否挡住真实回归 | [joyally-test](skills/engineering/joyally-test/SKILL.md) |
| 判断 Git 改动是否应自动提交和推送，并安全收尾 | [JoyStack joy-git](https://github.com/youngjunning/joystack/tree/main/skills/engineering/joy-git) |
| 让独立 reviewer 自动复查、修正并复验实质代码改动 | [JoyStack joy-loop](https://github.com/youngjunning/joystack/tree/main/skills/engineering/joy-loop) |
| 生成图像、漫画或静态架构图片 | [Joyally image](skills/design/joyally-image/SKILL.md) |
| 自动留存关键操作截图、找回写作素材或制作脱敏演示 | [Joyally Spotlight](skills/design/joyally-spotlight/SKILL.md) |
| 统一设计、制作 HTML 报告、HTML PPT 或交互图表 | [Joyally Design](skills/design/joyally-design/SKILL.md) |
| 设计、实现或评审产品动效、网页动画、代码视频与 2D/3D 运动 | [Joyally Motion](skills/design/joyally-motion/SKILL.md) |
| 录音、配音、人声修复、TTS、声音克隆、音色转换或转写对齐 | [Joyally Voice](skills/design/joyally-voice/SKILL.md) |
| 作曲、写歌、音乐生成、歌声合成、分轨、混音或母带 | [Joyally Music](skills/design/joyally-music/SKILL.md) |
| 为产品制作或重做整套主题，避免只换配色 | [Joyally 主题制作](skills/design/joyally-theme-creation/SKILL.md) |
| 写文章、绘本或建设内容站点 | [Joyally Writing](skills/writing/joyally-writing/SKILL.md)、[Joyally Fiction](skills/writing/joyally-fiction/SKILL.md)、[adsense-site-builder](skills/publishing/adsense-site-builder/SKILL.md) |
| 从 B 站、微信等视频链接或音视频文件提取字幕、时间点与结构化内容 | [Joyally Media](skills/productivity/joyally-media/SKILL.md) |
| 本地整理对话、笔记和资料，不部署也可使用 | [distill-me](https://github.com/youngjunning/distill-me) |
| 维护硅基紫升与硅基俊宁的资料、项目方案、工作脉络与定向同步 | [distill-zisheng](https://github.com/youngjunning/distill-zisheng) |

Joyally Writing、Joyally Design 和 Joyally image 可分别独立完成写作、交互/版式设计和栅格图像任务，也可联合交付。联合任务只设一个整体主导 Skill：写作负责读者、事实、论证与准确文案，设计负责视觉方向、构图、信息层级、版式、品牌与审美验收，图像负责像素落成、身份连续性与图像技术验收。图像任务可由 Joyally image 主导整体交付，其中的设计阶段仍由 Joyally Design 主导。跨域变更回到责任 Skill，支持 Skill 不改写上游成果。使用任一 Skill 时，会对当前环境缺失的另两个 Skill 给出一次可选安装建议，不阻塞当前任务。

## 分类索引

### Engineering

| 技能 | 用途 |
| --- | --- |
| [joyally-arch](skills/engineering/joyally-arch/SKILL.md) | 渐进式业务产品判断、AI 架构与 Skill、Agent、数字员工交付 |
| [joyally-browser-extension-dev](skills/engineering/joyally-browser-extension-dev/SKILL.md) | Agent 驱动浏览器扩展的 runtime、页面观察、业务 Skill 与受保护工具边界 |
| [joyally-report](skills/engineering/joyally-report/SKILL.md) | 向人解释进展、结果、证据与下一步 |
| [joyally-test](skills/engineering/joyally-test/SKILL.md) | TDD、测试策略与执行、Web/API 目标环境、AI/Agent evals、失败诊断与质量治理 |
| [tauri-skills](skills/engineering/tauri-skills/SKILL.md) | Tauri 2 安全边界与 Node.js sidecar |
| [browser-performance-audit](skills/engineering/browser-performance-audit/SKILL.md) | 加载、资源与长会话性能审查 |
| [joyally-macos](skills/engineering/joyally-macos/SKILL.md) | 原生 macOS、SwiftUI 与 Instruments 工作流（含许可改编） |

### Design

| 技能 | 用途 |
| --- | --- |
| [Joyally image](skills/design/joyally-image/SKILL.md) | 栅格图像的像素生成与编辑、漫画制作、身份连续性与图像技术验收 |
| [Joyally Spotlight](skills/design/joyally-spotlight/SKILL.md) | 关键操作截图私有归档与检索；真实演示素材扫描、遮盖与成品复核 |
| [Joyally Design](skills/design/joyally-design/SKILL.md) | 跨平台界面、HTML 交付、可探索图表与图像设计，主导视觉方向、构图、版式、交互与设计验收 |
| [Joyally Motion](skills/design/joyally-motion/SKILL.md) | 产品动效、网页动画、代码视频、2D/3D 与物理效果的意图、选型、实现和验收 |
| [Joyally Voice](skills/design/joyally-voice/SKILL.md) | 人声录制、修复、合成、配音、克隆、音色转换、转写对齐与授权验收 |
| [Joyally Music](skills/design/joyally-music/SKILL.md) | 音乐创作、生成、歌声合成、分轨、音频转 MIDI、混音与母带验收 |
| [Joyally 主题制作](skills/design/joyally-theme-creation/SKILL.md) | 从参考素材提炼构图与交互，设计有区分度的布局、自有组件和语义 token |

### Writing

| 技能 | 用途 |
| --- | --- |
| [Joyally Writing](skills/writing/joyally-writing/SKILL.md) | 中英文章、书稿与绘本写作，主导读者、事实、论证、叙事与准确文案 |
| [Joyally Fiction](skills/writing/joyally-fiction/SKILL.md) | 小说创作与阅读站点建设 |

### Publishing

| 技能 | 用途 |
| --- | --- |
| [adsense-site-builder](skills/publishing/adsense-site-builder/SKILL.md) | AdSense 站点规划、建设与就绪审查 |

### Productivity

| 技能 | 用途 |
| --- | --- |
| [Joyally Media](skills/productivity/joyally-media/SKILL.md) | B 站、微信等视频链接和音视频文件的字幕、时间线、关键画面与证据化内容提取 |
| [distill-me](https://github.com/youngjunning/distill-me) | 用零部署本地工作台整理材料与草稿，栏目可自由取舍 |
| [distill-zisheng](https://github.com/youngjunning/distill-zisheng) | 独立维护硅基紫升与硅基俊宁的资料、项目方案、工作脉络与定向内容同步 |

Joyally Design、Joyally Motion、Joyally Voice、Joyally Music、Joyally 主题制作、Joyally image、Joyally Writing、Joyally Fiction 和 Joyally Media 的安装与调用标识分别为 `joyally-design`、`joyally-motion`、`joyally-voice`、`joyally-music`、`joyally-theme-creation`、`joyally-image`、`joyally-writing`、`joyally-fiction` 和 `joyally-media`。机器可读目录见 [catalog.json](catalog.json)。

## 使用与维护

按 Agent 支持的方式调用技能，例如 `$joyally-arch`，或描述任务让 Agent 按匹配条件选择。部分技能依赖浏览器、Computer Use、图像服务或额外工具，具体前提见对应入口；静态校验不代表这些外部能力已完成验收。

```bash
python3 scripts/validate.py
```

新增技能放在 `skills/<category>/<name>/`，更新目录与说明，运行相关脚本测试后提交。涉及行为变化的更新记录到 [CHANGELOG.md](CHANGELOG.md)。发布边界和贡献要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。
每个自有技能的 `SKILL.md` frontmatter 必须保留 `metadata.author: 杨俊宁` 与 `metadata.email: luozhu2021@gmail.com`；仓库校验会检查这两个字段。

## 公开范围与来源

通用技能在这里维护；依赖私有业务、内部系统、未公开协议或敏感数据的技能保留在各自私有仓库。目标地址、账号、密钥、个人安装记录应留在使用项目或本机配置中。

已安装的第三方技能继续跟随上游，不因本机安装而收录为原创。已有借鉴与改编的署名、许可和 `NOTICE` 随技能保留，参见 [THIRD_PARTY.md](THIRD_PARTY.md)。

目录组织与统一维护方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。本仓库使用分类目录、统一安装入口与本地链接，不要求额外控制服务或发布平台。

## 许可

MIT。根目录许可适用于本仓库新增的自有内容；各技能已有的 `LICENSE`、署名和第三方声明继续有效。
