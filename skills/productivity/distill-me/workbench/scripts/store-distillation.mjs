import { mkdir, readFile, rename, writeFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const sectionIds = new Set(['memory', 'practice', 'articles', 'treasure', 'topics']);
const defaultData = { source: '', focus: '', sections: [...sectionIds], fragments: [] };
const inputIndex = process.argv.indexOf('--input');
const inputPath = inputIndex >= 0 ? process.argv[inputIndex + 1] : null;
const dataIndex = process.argv.indexOf('--data');
const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const dataPath = dataIndex >= 0 ? path.resolve(process.argv[dataIndex + 1]) : path.resolve(scriptDirectory, '../data/twin.json');

if (!inputPath) throw new Error('Usage: node scripts/store-distillation.mjs --input <json-file>');

function normalize(value) { return value.trim().replace(/\s+/g, ' '); }

function validate(item) {
  if (!item || typeof item !== 'object') throw new Error('Each distillation must be an object');
  const title = typeof item.title === 'string' ? item.title.trim() : '';
  const body = typeof item.body === 'string' ? item.body.trim() : '';
  const sections = Array.isArray(item.sections) ? [...new Set(item.sections.filter((id) => sectionIds.has(id)))] : [];
  if (!title || !body || !sections.length) throw new Error('Each distillation needs title, body and at least one valid section');
  return { title, body, sections };
}

async function loadData() {
  try {
    const parsed = JSON.parse(await readFile(dataPath, 'utf8'));
    return { ...defaultData, ...parsed, fragments: Array.isArray(parsed.fragments) ? parsed.fragments : [] };
  } catch (error) {
    if (error.code === 'ENOENT') return structuredClone(defaultData);
    throw error;
  }
}

const raw = JSON.parse(await readFile(path.resolve(inputPath), 'utf8'));
const incoming = (Array.isArray(raw) ? raw : [raw]).map(validate);
const data = await loadData();
let added = 0;
let duplicate = 0;

for (const item of incoming) {
  const exists = data.fragments.some((fragment) => normalize(fragment.body) === normalize(item.body));
  if (exists) { duplicate += 1; continue; }
  data.fragments.unshift({ id: randomUUID(), ...item, date: new Date().toISOString(), origin: 'automatic' });
  added += 1;
}

await mkdir(path.dirname(dataPath), { recursive: true });
const temporaryPath = `${dataPath}.${process.pid}.tmp`;
await writeFile(temporaryPath, `${JSON.stringify(data, null, 2)}\n`, { mode: 0o600 });
await rename(temporaryPath, dataPath);
console.log(JSON.stringify({ added, duplicate, total: data.fragments.length, dataPath }));
