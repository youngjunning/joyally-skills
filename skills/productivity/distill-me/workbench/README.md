# Distill Me 本地工作台

通常不需要手动操作。先返回 [Distill Me 快速使用说明](../README.md)，复制“安装 Skill”和“初始化本地数字分身”两段提示词交给 Agent。

只有 Agent 无法代为初始化时，才在本目录执行：

```bash
npm install
npm run open
```

工作台使用 Next.js 16、React 19 与内置 Lucian 组件，图标统一使用 Lucide。数据只保存在当前浏览器，不需要部署、账号、数据库或服务端。

不要直接打开源码文件；本地页面需要通过以上命令启动。
