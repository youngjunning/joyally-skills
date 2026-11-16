# Looseleaf 手绘主题来源

Joyally Design 的手绘主题采用 [Kevin Ngo 的 Looseleaf 官方仓库](https://github.com/kevintngo/looseleaf)作为 React Web 组件与视觉语法来源。2026-11-17 核对提交 `4bdb647940e2fefb3cebb394f3bad25c766a27d2`：官方 README 描述 123 个组件与 61 个页面 blocks；`registry.json` 中实际有 123 个 `registry:ui` 条目，`looseleaf` umbrella 项逐项依赖这 123 个组件，并同时带入纸张主题、Kevin Sans、ink engine 与所需 hooks/lib。

项目源码、组件、绘制素材与 Kevin Sans 使用 [MIT License](https://github.com/kevintngo/looseleaf/blob/main/LICENSE)，IBM Plex Mono 使用 SIL Open Font License 1.1。Joyally Design 不复制上游组件源码，只记录主题契约和语义 token 映射；实际项目通过 Looseleaf 官方 shadcn registry 获取本地源码，并保留上游版权和许可。后续使用前重新核对当前 registry、许可、React/Tailwind/Radix 兼容性及组件数量，不把本次提交快照当作永久最新版本。

Looseleaf 当前官方主题是浅色纸张体系；代码块另有局部深色 tone，但这不能证明整套组件已有深色主题。Joyally Design 因此只把浅色映射列为已提供样本，深色需在使用项目单独实现与验收。
