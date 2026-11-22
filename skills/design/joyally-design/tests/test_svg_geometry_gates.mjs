import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const edge = '<path class="reader-connection" data-edge-id="route" data-edge-from="start" data-edge-to="end" data-composition-points="154,136;154,180;600,180" d="M154 136 V104 H600" />';
const title = (y) => `<text class="group-title" x="56" y="${y}">入口与任务路径</text>`;
const svg = (body, attrs = '') => `<svg viewBox="0 0 700 240" data-layout-contract="readable-v2" ${attrs}>${body}</svg>`;
const plate = (fill) => svg('<path class="reader-connection" data-edge-id="route" d="M40 104 H600" />' +
  `<g data-edge-id="route"><rect class="c-mask" x="150" y="85" width="240" height="44" fill="${fill}"/><text x="160" y="113">实际标签底板</text></g>`);
// Synthetic geometry only: no private business labels, SPM codes or user data.
const scenes = {
  collision: svg(edge + title(117)),
  clear: svg(edge + title(86)),
  transformed: svg(`<g transform="translate(12 8) scale(.9)">${edge}${title(117)}</g>`),
  caption: svg('<path data-edge-id="caption-route" class="reader-connection" d="M40 104 H600" />' + '<text class="caption" x="160" y="113">无关系标签的说明</text>'),
  masked: plate('white'),
  transparent: plate('rgba(255,255,255,.2)'),
  unmeasured: svg('<path class="reader-connection" data-edge-id="empty-route" d="" />' + title(86)),
  hidden: svg(edge + title(117), 'style="display:none"'),
};

test('final SVG gates measure CSS text and actual paths, with coverage and opaque-mask handling', { skip: !existsSync(chrome) && 'Chrome is required for real browser geometry' }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'joyally-svg-gates-'));
  const html = join(dir, 'fixture.html');
  const output = join(dir, 'evidence');
  await writeFile(html, `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="description" content="Synthetic geometry regression"><title>SVG geometry regression</title><style>body{margin:24px;background:white;color:black}svg{width:700px;height:240px}text{font:17px sans-serif;fill:black}.reader-connection{stroke:black;stroke-width:2.5;fill:none}</style></head><body><main id="scene"></main><script>const scenes=${JSON.stringify(scenes)};document.getElementById('scene').innerHTML=scenes[new URLSearchParams(location.search).get('state')];</script></body></html>`, 'utf8');
  const run = spawnSync(process.execPath, [join(root, 'scripts/shoot.mjs'), html,
    '--size', 'desktop', '--states', Object.keys(scenes).join(','), '--no-sheet', '--gates', '--out', output],
    { encoding: 'utf8', timeout: 240000 });
  assert.ifError(run.error);
  assert.equal(run.status, 1, run.stdout + run.stderr);
  const reports = JSON.parse(await readFile(join(output, 'report.json'), 'utf8'));
  const result = (state) => {
    const entry = reports.find((row) => row.state === state);
    assert.ok(entry && !entry.failed, `Missing browser result: ${state}\n${run.stdout}\n${run.stderr}`);
    return entry;
  };
  for (const state of ['collision', 'transformed', 'caption', 'transparent']) {
    const entry = result(state);
    assert.ok(entry.lint.some((finding) => finding.rule === 'svgTextCollision' && finding.tier === 'floor' && finding.status === 'open'), state);
    assert.equal(entry.gates.passed, false, state);
    assert.equal(entry.svgGeometry[0].measuredTexts, 1, state);
    assert.equal(entry.svgGeometry[0].measuredPaths, 1, state);
    assert.ok(entry.lint.some((finding) => finding.examples.some((example) => example.includes(state === 'caption' ? 'caption-route' : 'route'))), state);
  }
  const clear = result('clear');
  assert.equal(clear.gates.passed, true);
  assert.equal(clear.svgGeometry[0].checkedPairs, 1);
  assert.equal(clear.svgGeometry[0].status, 'passed');
  const masked = result('masked');
  assert.equal(masked.gates.passed, true);
  assert.equal(masked.svgGeometry[0].maskedPairs, 1);
  const unmeasured = result('unmeasured');
  assert.ok(unmeasured.lint.some((finding) => finding.rule === 'svgGeometryUnmeasured' && finding.tier === 'floor'));
  assert.equal(unmeasured.gates.passed, false);
  assert.equal(unmeasured.svgGeometry[0].measuredPaths, 0);
  assert.equal(unmeasured.svgGeometry[0].status, 'failed');
  assert.equal(result('hidden').gates.passed, true);
  assert.deepEqual(result('hidden').svgGeometry, []);
});
