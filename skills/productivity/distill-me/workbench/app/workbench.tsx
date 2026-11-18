'use client';

import { ToggleGroup } from 'radix-ui';
import { useEffect, useMemo, useState } from 'react';

type ThemeId = 'qingshan' | 'xihu' | 'maldives';

type Draft = {
  id: string;
  title: string;
  body: string;
  date: string;
  columns: string[];
};

type WorkbenchData = {
  source: string;
  focus: string;
  columns: string[];
  items: Draft[];
};

const columns = [
  { id: 'judgment', code: '01', name: '重要判断', description: '明确表达的取舍、原则与变化。' },
  { id: 'progress', code: '02', name: '关键进展', description: '可回查的结果、阻塞和下一步。' },
  { id: 'reference', code: '03', name: '资料收藏', description: '值得回看的资料、用途与出处。' },
  { id: 'follow-up', code: '04', name: '待跟进', description: '尚未完成且需要继续推进的事项。' },
  { id: 'article', code: '05', name: '文章草稿', description: '选题、角度、提纲与证据，不自动发布。' },
];

const themes: { id: ThemeId; label: string }[] = [
  { id: 'qingshan', label: '青山湖' },
  { id: 'xihu', label: '西湖' },
  { id: 'maldives', label: '马尔代夫' },
];

const storageKey = 'distill-me-workbench-v3';
const themeKey = 'distill-me-workbench-theme';
const defaultData: WorkbenchData = {
  source: '',
  focus: '',
  columns: columns.map((column) => column.name),
  items: [],
};

function safeId() {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({
    behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    block: 'start',
  });
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('zh-CN', { month: 'long', day: 'numeric' }).format(new Date(value));
}

export default function Workbench() {
  const [data, setData] = useState<WorkbenchData>(defaultData);
  const [theme, setTheme] = useState<ThemeId>('qingshan');
  const [ready, setReady] = useState(false);
  const [notice, setNotice] = useState('只保存在这台设备');

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey) || 'null') as Partial<WorkbenchData> | null;
      if (stored) {
        setData({
          source: typeof stored.source === 'string' ? stored.source : '',
          focus: typeof stored.focus === 'string' ? stored.focus : '',
          columns: Array.isArray(stored.columns) ? stored.columns.filter((item): item is string => typeof item === 'string') : defaultData.columns,
          items: Array.isArray(stored.items) ? stored.items : [],
        });
      }
      const storedTheme = localStorage.getItem(themeKey);
      if (themes.some((item) => item.id === storedTheme)) setTheme(storedTheme as ThemeId);
    } catch {
      setNotice('本地存储不可用，仍可复制或导出');
    } finally {
      setReady(true);
    }
  }, []);

  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(storageKey, JSON.stringify(data));
    } catch {
      setNotice('本地存储不可用，仍可复制或导出');
    }
  }, [data, ready]);

  useEffect(() => {
    if (!ready) return;
    localStorage.setItem(themeKey, theme);
  }, [theme, ready]);

  const latest = useMemo(() => data.items[0], [data.items]);
  const enabledColumns = columns.filter((column) => data.columns.includes(column.name));

  function update<K extends keyof WorkbenchData>(key: K, value: WorkbenchData[K]) {
    setData((current) => ({ ...current, [key]: value }));
  }

  function saveDraft() {
    const body = data.source.trim();
    if (!body) {
      setNotice('先放入一段对话、笔记或资料');
      return;
    }
    const draft: Draft = {
      id: safeId(),
      title: data.focus.trim() || body.split(/\n|。/)[0].slice(0, 28) || '未命名蒸馏',
      body,
      date: new Date().toISOString(),
      columns: data.columns,
    };
    setData((current) => ({ ...current, source: '', focus: '', items: [draft, ...current.items] }));
    setNotice('草稿已留在本机');
  }

  async function copyPrompt() {
    const prompt = [
      '请使用 distill-me 整理下面的材料。',
      `本次重点：${data.focus.trim() || '请根据材料判断'}`,
      `启用栏目：${data.columns.join('、') || '不预设栏目，请先给建议'}`,
      '要求：保留来源和不确定性，先返回草稿，不要发布或同步。',
      '',
      data.source.trim() || '（请在这里粘贴材料）',
    ].join('\n');
    try {
      await navigator.clipboard.writeText(prompt);
      setNotice('已复制给 Agent 的请求');
    } catch {
      setNotice('复制失败，请手动选择文本');
    }
  }

  function exportData() {
    const blob = new Blob([JSON.stringify({ exportedAt: new Date().toISOString(), ...data }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `distill-me-${new Date().toISOString().slice(0, 10)}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
    setNotice('已导出本地备份');
  }

  function removeDraft(id: string) {
    setData((current) => ({ ...current, items: current.items.filter((item) => item.id !== id) }));
    setNotice('已从本机移除草稿');
  }

  return (
    <div className={`site-shell theme-${theme}`}>
      <header className="site-header">
        <button className="site-identity" type="button" onClick={() => scrollTo('overview')} aria-label="返回总览">
          <span className="site-identity-mark" aria-hidden="true">D</span>
          <span>Distill Me<small>本地数字分身</small></span>
        </button>
        <nav className="site-nav" aria-label="主导航">
          <button type="button" onClick={() => scrollTo('growth')}>近况</button>
          <button type="button" onClick={() => scrollTo('columns')}>栏目</button>
          <button type="button" onClick={() => scrollTo('compose')}>蒸馏</button>
          <button type="button" onClick={() => scrollTo('drafts')}>草稿</button>
        </nav>
        <div className="site-status" aria-live="polite"><span />{notice}</div>
        <span className="header-rule" aria-hidden="true" />
      </header>

      <main className="site-workspace">
        <section className="identity-hero" id="overview" aria-labelledby="identity-title">
          <div className="identity-overline"><span>DISTILL ME</span><span>LOCAL DIGITAL TWIN</span></div>
          <div className="identity-main">
            <div className="identity-copy">
              <span className="identity-kicker">材料、判断与持续生长的草稿</span>
              <h1 id="identity-title">你好，这是你的本地数字分身。<span>这里记录你如何走到今天。</span></h1>
              <p className="identity-description">把对话、笔记和资料整理成可继续使用的判断与草稿。内容只在本机保存，你决定何时交给 Agent、导出或带到别处。</p>
              <div className="identity-actions">
                <button className="primary-button" type="button" onClick={() => scrollTo('compose')}>开始一次蒸馏 <span aria-hidden="true">→</span></button>
                <button className="secondary-button" type="button" onClick={() => scrollTo('drafts')}>读本地草稿 <span aria-hidden="true">↗</span></button>
              </div>
            </div>
            <nav className="identity-route" aria-label="从这里开始">
              <span>从这里开始</span>
              <button type="button" onClick={() => scrollTo('compose')}><small>01 / 放入上下文</small><strong>收集材料</strong><span aria-hidden="true">↗</span></button>
              <button type="button" onClick={() => scrollTo('columns')}><small>02 / 自由取舍</small><strong>选择栏目</strong><span aria-hidden="true">↗</span></button>
              <button type="button" onClick={() => scrollTo('drafts')}><small>03 / 留在本机</small><strong>继续整理</strong><span aria-hidden="true">↗</span></button>
            </nav>
          </div>
          <div className="identity-bottom">
            <div className="identity-count">
              <span><strong>{data.items.length}</strong> 份本地草稿</span>
              <span><strong>{data.columns.length}</strong> 个启用栏目</span>
              <span><strong>0</strong> 次自动同步</span>
            </div>
            <div className="identity-skill">
              <div><span className="eyebrow">CONTINUE WITH AN AGENT</span><h2>交给 Agent 继续整理</h2><p>复制一段带栏目与边界的请求，千问办公、Codex 或其他宿主都可以接着做。</p></div>
              <button className="compact-button" type="button" onClick={copyPrompt}>复制请求 <span aria-hidden="true">→</span></button>
            </div>
          </div>
        </section>

        <section className="home-section" id="growth" aria-labelledby="growth-title">
          <div className="section-heading"><span>THIS WEEK</span><div><h2 id="growth-title">本地在生长</h2><p>最近留下的材料、栏目与草稿，都是这个数字分身正在形成的部分。</p></div></div>
          <div className="growth-grid">
            <article><span>草稿</span><strong>{data.items.length}</strong><p>{latest ? `最近更新于 ${formatDate(latest.date)}` : '还没有草稿，从一段材料开始。'}</p></article>
            <article><span>栏目</span><strong>{data.columns.length}<small> / 5</small></strong><p>{enabledColumns.map((item) => item.name).join('、') || '本次暂不预设栏目。'}</p></article>
            <article><span>边界</span><strong>本地</strong><p>不登录、不上传、不部署，也不自动同步到任何站点。</p></article>
          </div>
        </section>

        <section className="home-section" id="columns" aria-labelledby="columns-title">
          <div className="section-heading"><span>THE SHAPE OF YOUR MEMORY</span><div><h2 id="columns-title">精选栏目 · 只留这 5 个</h2><p>这是公开版与硅基紫升首页唯一的内容差异。栏目只是起点，可按本次材料自由取舍。</p></div></div>
          <ToggleGroup.Root className="column-grid" type="multiple" value={data.columns} onValueChange={(value) => update('columns', value)} aria-label="选择本次蒸馏栏目">
            {columns.map((column) => (
              <ToggleGroup.Item className="column-card" key={column.id} value={column.name} aria-label={column.name}>
                <span className="column-code">{column.code}</span>
                <strong>{column.name}</strong>
                <p>{column.description}</p>
                <span className="column-state">{data.columns.includes(column.name) ? '已启用' : '未启用'}</span>
              </ToggleGroup.Item>
            ))}
          </ToggleGroup.Root>
        </section>

        <section className="home-section compose-section" id="compose" aria-labelledby="compose-title">
          <div className="section-heading"><span>IN THE MOMENT</span><div><h2 id="compose-title">开始一次蒸馏</h2><p>先把当下的上下文留下。工作台不调用模型，只负责组织、保存和交接。</p></div></div>
          <div className="compose-grid">
            <div className="compose-form">
              <label htmlFor="focus">这次最想留下什么</label>
              <input id="focus" value={data.focus} onChange={(event) => update('focus', event.target.value)} placeholder="例如：这次产品讨论中真正改变的判断" />
              <label htmlFor="source">对话、笔记或资料</label>
              <textarea id="source" value={data.source} onChange={(event) => update('source', event.target.value)} placeholder="把材料粘贴到这里。它只会保存在当前浏览器。" />
              <div className="form-actions">
                <button className="primary-button" type="button" onClick={saveDraft}>留为本地草稿 <span aria-hidden="true">→</span></button>
                <button className="secondary-button" type="button" onClick={copyPrompt}>复制给 Agent</button>
                <button className="text-button" type="button" onClick={() => setData((current) => ({ ...current, source: '', focus: '' }))}>清空输入</button>
              </div>
            </div>
            <aside className="compose-aside">
              <span className="eyebrow">CURRENT DISTILLATION</span>
              <h3>{data.focus.trim() || '一次还没有命名的蒸馏'}</h3>
              <p>{data.source.trim() ? `${data.source.trim().length} 个字符已留在输入区。` : '材料还没有放进来。可以先选栏目，也可以直接开始写。'}</p>
              <div className="enabled-list">{enabledColumns.map((column) => <span key={column.id}>{column.name}</span>)}</div>
              <button className="export-button" type="button" onClick={exportData}>导出全部本地数据 <span aria-hidden="true">↓</span></button>
            </aside>
          </div>
        </section>

        <section className="home-section" id="drafts" aria-labelledby="drafts-title">
          <div className="section-heading section-heading-row"><span>THE WRITTEN RECORD</span><div><h2 id="drafts-title">最近留下的草稿</h2><p>它们不是已发布内容，只是你可以继续修改、交给 Agent 或导出的本地记录。</p></div><button className="text-button" type="button" onClick={exportData}>导出 JSON ↗</button></div>
          {data.items.length ? (
            <div className="draft-grid">{data.items.map((item, index) => (
              <article className="draft-card" key={item.id}>
                <div className="draft-meta"><span>{String(index + 1).padStart(2, '0')}</span><time dateTime={item.date}>{formatDate(item.date)}</time></div>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
                <div className="draft-footer"><div>{item.columns.map((column) => <span key={column}>{column}</span>)}</div><button type="button" onClick={() => removeDraft(item.id)}>移除</button></div>
              </article>
            ))}</div>
          ) : (
            <div className="empty-state"><span>NO DRAFTS YET</span><h3>第一份草稿，从一段真实材料开始。</h3><button className="secondary-button" type="button" onClick={() => scrollTo('compose')}>去开始蒸馏 ↗</button></div>
          )}
        </section>

        <footer className="page-footer">让每一次判断，都能回到实践。<div><span>Distill Me · 本地数字分身</span><span>数据留在你的浏览器</span></div></footer>
      </main>

      <aside className="theme-dock" aria-label="主题">
        <span>主题</span>
        <ToggleGroup.Root type="single" value={theme} onValueChange={(value) => value && setTheme(value as ThemeId)} aria-label="切换主题">
          {themes.map((item) => <ToggleGroup.Item key={item.id} value={item.id} aria-label={item.label} title={item.label}><span aria-hidden="true" /></ToggleGroup.Item>)}
        </ToggleGroup.Root>
      </aside>
    </div>
  );
}
