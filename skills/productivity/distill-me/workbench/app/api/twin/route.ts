import { mkdir, readFile, rename, writeFile } from 'node:fs/promises';
import path from 'node:path';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const sectionIds = new Set(['memory', 'practice', 'articles', 'treasure', 'topics']);
const defaultData = { source: '', focus: '', sections: [...sectionIds], fragments: [] };
const dataPath = path.join(process.cwd(), 'data', 'twin.json');

function sanitize(data: unknown) {
  if (!data || typeof data !== 'object') return defaultData;
  const value = data as Record<string, unknown>;
  const fragments = Array.isArray(value.fragments)
    ? value.fragments.filter((item) => item && typeof item === 'object').map((item) => {
        const fragment = item as Record<string, unknown>;
        return {
          id: typeof fragment.id === 'string' ? fragment.id : crypto.randomUUID(),
          title: typeof fragment.title === 'string' ? fragment.title : '未命名片段',
          body: typeof fragment.body === 'string' ? fragment.body : '',
          date: typeof fragment.date === 'string' ? fragment.date : new Date().toISOString(),
          sections: Array.isArray(fragment.sections) ? fragment.sections.filter((id) => typeof id === 'string' && sectionIds.has(id)) : [],
          origin: fragment.origin === 'automatic' ? 'automatic' : 'manual',
        };
      }).filter((item) => item.body && item.sections.length)
    : [];
  return {
    source: typeof value.source === 'string' ? value.source : '',
    focus: typeof value.focus === 'string' ? value.focus : '',
    sections: Array.isArray(value.sections) ? value.sections.filter((id) => typeof id === 'string' && sectionIds.has(id)) : [...sectionIds],
    fragments,
  };
}

async function loadData() {
  try { return sanitize(JSON.parse(await readFile(dataPath, 'utf8'))); }
  catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') return defaultData;
    throw error;
  }
}

export async function GET() {
  return Response.json(await loadData(), { headers: { 'Cache-Control': 'no-store' } });
}

export async function PUT(request: Request) {
  const data = sanitize(await request.json());
  await mkdir(path.dirname(dataPath), { recursive: true });
  const temporaryPath = `${dataPath}.${process.pid}.tmp`;
  await writeFile(temporaryPath, `${JSON.stringify(data, null, 2)}\n`, { mode: 0o600 });
  await rename(temporaryPath, dataPath);
  return Response.json(data);
}
