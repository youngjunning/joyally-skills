# Distill Me 本地工作台

首次使用：

```bash
npm install
npm run open
```

浏览器会自动打开工作台。它只在本机运行，不需要部署、账号或服务端。

如需指定端口或让局域网设备访问，可改用：

```bash
npm run dev -- --host 127.0.0.1 --port 4173
```

不要直接双击 `index.html`；它是 Vite/React 的源码入口，必须通过以上命令启动。
