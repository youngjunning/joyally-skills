# Distill Me 本地数字分身

首次使用：

```bash
npm install
npm run open
```

浏览器会自动打开工作台。它使用与硅基紫升一致的 Next.js 16、React 19 首页结构，只采用 Radix UI 一套组件库；数据只在本机运行，不需要部署、账号或服务端。

如需指定端口或让局域网设备访问，可改用：

```bash
npm run dev -- --host 127.0.0.1 --port 4173
```

不要直接打开源码文件；Next.js 工作台必须通过以上命令启动。
