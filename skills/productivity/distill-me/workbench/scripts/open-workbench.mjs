import { spawn } from 'node:child_process';
import { request } from 'node:http';
import process from 'node:process';

const port = process.env.PORT || '4173';
const url = `http://127.0.0.1:${port}`;
const nextBin = process.platform === 'win32' ? 'node_modules\\.bin\\next.cmd' : 'node_modules/.bin/next';
const server = spawn(nextBin, ['dev', '--hostname', '127.0.0.1', '--port', port], { stdio: 'inherit' });

function openBrowser() {
  const command = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'cmd' : 'xdg-open';
  const args = process.platform === 'win32' ? ['/c', 'start', '', url] : [url];
  spawn(command, args, { detached: true, stdio: 'ignore' }).unref();
}

let attempts = 0;
const timer = setInterval(() => {
  attempts += 1;
  const check = request(url, () => {
    clearInterval(timer);
    openBrowser();
  });
  check.on('error', () => {
    if (attempts > 80) clearInterval(timer);
  });
  check.end();
}, 250);

server.on('exit', (code) => {
  clearInterval(timer);
  process.exitCode = code ?? 0;
});
