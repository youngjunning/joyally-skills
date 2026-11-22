# Changelog

## 2026-11-22

10. `joyally-report` 的收尾技能清单改为逐项附带本轮具体作用，避免只罗列技能名而无法判断各技能实际贡献。
9. 将 `distill-zisheng` 迁至独立仓库维护；本仓库保留外部入口，不再重复发布本地副本。
8. 删除重复维护的 `joyally-git`；Git 交付能力统一迁移到独立 [JoyStack `joy-git`](https://github.com/youngjunning/joystack/tree/main/skills/engineering/joy-git)，并同步更新仍在使用的跨 Skill 引用。
5. 优化 YingMusic-Singer 的旋律保持：分段对齐参考、目标与 VAE 时间轴，裁掉条件间隔；增加连续 F0 保音、原始人声对照、修正范围门禁与产物记录。固定 MIDI 短样和授权导唱副歌的自动音高校验通过，保留对原生模型偏移、音色与自然度验收的边界。
4. 接入 `joyally-music` 与 YingMusic-Singer V1 本地试验入口，固定代码、权重与依赖版本，补充 CPU 注意力和音频读取适配及产物记录；MIDI、旋律音频与不同采样参数已实际出声。短句歌词检查通过，旋律保持和本人音色尚未验收；官方权重为 CC-BY-NC-4.0，不将试验能力标为成品质量。
1. 将 `joyally-media-reading` 更名为 `joyally-media`，同步目录、Skill 名称、安装入口、UI 元数据与公开索引；能力与触发范围保持不变。

## 2026-11-21

7. 优化 `joyally-git` 的并行交付：脏工作区、无关 staged 内容和分支分叉优先转入基于目标 ref 的隔离 worktree，复验任务补丁后 fast-forward push；只有任务语义无法拆分、真实冲突或目标不明时才停止请求决定。
6. 新增 `joyally-media-reading`：从 B 站、微信视频号和公众号视频等托管页面、直接媒体链接及本地音视频提取字幕、转写、时间线和关键画面；显式报告覆盖范围与证据来源，并把结构化材料交给后续写作、小说或视频工作流。
5. 将 `top-architect` 更名为 `joyally-arch`；吸收 arch-grower 的局部决策切片、显式待定与储备状态、Walking Skeleton、稳定子图折叠及失败路径学习机制，同时保留现有业务、产品、AI 架构和交付主线，不复制其 CLI、图 schema 或强制二选一/子代理策略。
4. 新增 `joyally-voice`：覆盖录音、人声修复、TTS、配音、声音克隆、说话/歌声音色转换、转写对齐及授权与质量验收；配音作为 Voice 分支统一维护。
3. 新增 `joyally-music`：独立维护作曲、写歌、音乐与歌声生成、分轨、音频转 MIDI、混音和母带；与 `joyally-voice` 按歌曲整体和人声身份分工。
2. 新增 `joyally-motion`：基于 20 个官方开源项目建立产品动效、网页动画、代码视频、角色、2D/3D、物理与粒子选型矩阵，统一 motion intent、单一时钟、reduced motion、性能和真实交付验收；保留许可证与第三方资产边界。
1. 将 `joyally-test-quality` 更名为 `joyally-test`，融合 10 个 AI Native 测试 Skill 的差异化机制，扩展为 TDD、性质/fuzz/mutation、Web/E2E/辅助技术、API 契约、AI/Agent evals、失败诊断与套件治理的统一入口；保留按真实回归判断测试价值的核心标准与来源许可边界。

## 2026-11-20

2. 将 `zisheng-site-sync` 的双站共同能力与定向内容同步流程合入 `distill-zisheng`：按方向审查接收受众，使用私有审核账本和只读规划器，分别验收与报告功能、内容流向及交付状态。
1. `distill-zisheng` 明确：本人标为个人隐私的材料不得进入公司目标，即使已有公开原稿或技术价值；重新分类时按撤回移除当前源稿及派生引用，不将拒收原因留在公司仓库。

## 2026-11-18

3. 新增 `joyally-git`：在任务收尾时先核对授权、改动归属、验证、分支、远端和发布副作用，再判断提交并推送、只提交、保留改动或请求确认；只暂存本任务文件，区分 Git 交付与部署、发布及真实业务结果。
2. 细化三技能协作：Joyally Design 主导图像的视觉方向、构图、版式、品牌与设计验收，Joyally image 主导像素落成、身份连续性与图像技术验收；使用任一技能时，对缺失的另两个技能给出一次非阻塞的可选安装建议。
1. 统一 Joyally Design、Joyally writting 与 Joyally image 的协作边界：三者均可独立使用，联合任务只设一个主导 Skill；分别对交互/布局、事实/文案和栅格图像负责，跨域变更回到责任 Skill，避免支持阶段互相改写成果。

## 2026-11-16

2. 删除不再维护的 `qoderwork-cup` 与 `qwenwork-cup`，同步清理公开目录和索引。
1. 新增 `joyally-browser-extension-dev`：沉淀 Agent 驱动浏览器扩展的四层职责边界、语义变体处理、受保护工具设计、MV3 生命周期回归与交付验收，避免把按钮文案和业务流程写死在扩展脚本中。

## 2026-11-14

1. 新增 `joyally-theme-creation`，以同内容对比检验主题的结构差异；要求组件具备主题自己的层级、细节和完整状态，不能只给 shadcn/ui 基础控件换色。Joyally Design 增加主题制作入口。

## 2026-11-13

2. 将 `joyally-imagegen` 更名为 `joyally-image`，同步目录、安装名和技能间引用；Joyally Image 与 Joyally Design 各自保留小界、小萌、小南的全身、上半身与头像参考素材。
1. 新增 `joyally-midway`：面向常驻 Midway Web 应用的开发与排障，整理依赖注入作用域、Middleware、配置、生命周期和完整 HTTP 链路验收；明确排除 FaaS。

## 2026-11-12

3. 新增 `joyally-test-quality`：按真实回归与维护成本审查测试，支持判断 AI 生成测试是否值得保留；记录上游启发来源，不复制无许可文本。
2. 将报告技能统一命名为 `joyally-report`，保留从简短进度到完整工程交付的按需汇报能力；同步安装入口、元数据与索引。
1. 新增 product-demo-media：从真实产品操作制作文章截图和落地页演示录屏，提供 OCR 候选扫描、确定性遮盖与马赛克渲染，并要求逐帧覆盖和发布前复核。

## 2026-11-11

1. Joyally Design、Joyally imagegen 和 Joyally writting 统一使用 `joyally-design`、`joyally-imagegen` 和 `joyally-writting` 作为安装及调用名。原 `better-imagegen` 和 `writting-skill` 的目录、项目引用和 CI 路径已迁移。

## 2026-11-09

1. 将 `memory-distill` 更名为 `distill-me`，同步 Skill 入口、调用提示、目录索引与 CI 校验路径。

## 2026-11-08

5. 将 `personal-records-reader` 的只读查询与接口文档合入 `memory-distill`，移除独立技能入口；查询不触发蒸馏写入，站点读取包继续复用同字节脚本。
1. 按常见问题和五个类别重排技能入口，保留 `catalog.json` 与原安装方式；校验 README 中的技能路径与目录一致。
2. 将 report-skill 更名为 report-for-human，覆盖简短进展、完成反馈、交付、排障与评审；按读者需要调整篇幅，并同步目录、元数据和引用。
3. 在 top-architect 的系统边界与评审中增加高内聚、低耦合的可检查信号：同一业务变化的归属、跨边界契约、变更传播与循环依赖。
4. 移除独立的 `polyglot-service-deploy`；多运行时服务的部署与排障规则合并回内部开发技能，不再维护公开副本。

## 2026-11-05

1. 补齐 top-architect 的 AI 技术与交付专项：覆盖 Skill 资产生命周期、模型与上下文/数据/工具、Agent 运行协作、数字员工职责与运营，以及分层评测和版本化发布；同步入口、评审、决策模板及示例，按任务选择相关深度。
1. 整体重构 top-architect：由技术架构入口扩展为业务判断、产品取舍、技术设计与稳定交付的统一决策流程；覆盖行业价值链、使用者与付费者、产品采用、完整结果成本及继续或停止投入的条件。
2. 新增业务产品与系统交付参考，重写决策、评审、讨论模板并同步技能元数据和目录；保留 Web、CLI、运行时性能与开源框架专项资料，小型技术问题按需处理。
3. 通过三名独立 GPT-6.1 Sol 评估者演练六个合成场景，覆盖产品机会、拆分、Agent 恢复、CLI、内存诊断和窄技术问题；只验证推理与范围，未执行真实业务或目标平台验收。

## 2026-11-02

1. 将 Qingshan Design 与 Lake Report Design 合并为 Joyally Design，统一跨平台入口、语义 token 契约和安装名；保留原生平台、React、HTML 报告及 Archify 能力。
2. 原生示例和报告脚本统一 Joyally 命名，旧项目采用迁移说明更新；内部服务与上传配置继续留在使用项目。

## 2026-11-01

1. 补充项目级来源复核，迁入维护改编的 macOS 开发技能；保留 SwiftUI 资料 MIT 署名，并以原创检查清单替换未获分发许可的参考正文。

1. 完成第二轮脱敏审查，新增记忆蒸馏、个人资料读取、两种桌面 Chat 验收、可移植报告设计，以及多运行时部署的通用工作流。
2. 私有目标、主机规则、身份和部署适配器留在使用项目或本机配置；报告包移除私有上传实现与角色素材，保留带原始许可的第三方图表和排版 runtime。

1. 将 9 个独立技能仓库与通用浏览器性能审查技能整合到 4 类目录，保留既有技能名。
2. 统一安装说明、目录、维护约定和校验入口，新增可先预览且自动备份冲突的本地链接工具。
3. 将小说站点示例中的广告账号、Pixel ID、个人路径与站点配置替换为占位与项目配置；原始历史只保留在私有迁移备份。
