#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const designRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const imageEntry = resolve(designRoot, '../joyally-image/scripts/joyally-diagram.mjs');

if (!existsSync(imageEntry)) {
  console.error('The deprecated Joyally Design diagram command now requires joyally-image. Install joyally-image and migrate to its scripts/joyally-diagram.mjs entrypoint.');
  process.exit(2);
}

console.error('[deprecated] Joyally Design diagram commands moved to joyally-image/scripts/joyally-diagram.mjs. This compatibility forwarder will be removed after consumers migrate.');
const result = spawnSync(process.execPath, [imageEntry, ...process.argv.slice(2)], {
  cwd: process.cwd(),
  env: process.env,
  stdio: 'inherit',
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
