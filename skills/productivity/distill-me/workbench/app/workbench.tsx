'use client';

import { ToggleGroup } from 'radix-ui';
import { useEffect, useMemo, useState } from 'react';

type ThemeId = 'qingshan' | 'xihu' | 'maldives';
type SectionId = 'memory' | 'practice' | 'articles' | 'treasure' | 'topics';

type TwinSection = { id: SectionId; code: string; mark: string; name: string; meaning: string; promise: string; prompt: string };
type Fragment = { id: string; title: string; body: string; date: string; sections: SectionId[] };
type TwinData = { source: string; focus: string; sections: SectionId[]; fragments: Fragment[] };

const twinSections: TwinSection[] = [
  { id: 'memory', code: 'MEMORY', mark: '记', name: '个人记录', meaning: '经历、判断与变化', promise: '让人知道你从哪里来，也看见你如何成为现在的你。', prompt: '提炼可核对的经历、明确表达的判断，以及前后发生的变化。' },
  { id: 'practice', code: 'PRACTICE', mark: '做', name: '做事方式', meaning: '能力、协作与创造', promise: '不只展示结果，也让你的方法、边界和长处可以被理解。', prompt: '提炼反复出现的方法、协作习惯、能力证据与适用边界。' },
  { id: 'articles', code: 'ARTICLES', mark: '文', name: '文章', meaning: '持续写作与系统表达', promise: '把零散想法变成有观点、有依据、值得继续写的主题。', prompt: '整理可写的选题、核心观点、结构、证据与尚待确认的部分。' },
  { id: 'treasure', code: 'COLLECTION', mark: '藏', name: '百宝箱', meaning: '资源与知识笔记', promise: '收藏不止是链接，而是知道它为什么有用、何时再拿出来。', prompt: '保留资料名称、来源、摘要、用途与适合再次取用的场景。' },
  { id: 'topics', code: 'SUBJECTS', mark: '题', name: '关注主题', meaning: '长期兴趣与问题意识', promise: '看见你持续关注什么，以及这些主题如何连接经历、文章与收藏。', prompt: '提炼持续关注的主题、核心问题、相关经历与内容依据，避免只凭一次提及下结论。' },
];

const themes: { id: ThemeId; label: string }[] = [
  { id: 'qingshan', label: '青山湖' },
  { id: 'xihu', label: '西湖' },
  { id: 'maldives', label: '马尔代夫' },
];

const storageKey = 'distill-me-digital-twin-v2';
const themeKey = 'distill-me-workbench-theme';
const defaultData: TwinData = { source: '', focus: '', sections: twinSections.map((section) => section.id), fragments: [] };

function safeId() { return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`; }
function scrollTo(id: string) { document.getElementById(id)?.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
function formatDate(value: string) { return new Intl.DateTimeFormat('zh-CN', { month: 'long', day: 'numeric' }).format(new Date(value)); }

export default function Workbench() {
  const [data, setData] = useState<TwinData>(defaultData);
  const [theme, setTheme] = useState<ThemeId>('qingshan');
  const [ready, setReady] = useState(false);
  const [notice, setNotice] = useState('所有内容只在本机');

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey) || 'null') as Partial<TwinData> | null;
      if (stored) {
        const knownIds = new Set(twinSections.map((section) => section.id));
        setData({
          source: typeof stored.source === 'string' ? stored.source : '',
          focus: typeof stored.focus === 'string' ? stored.focus : '',
          sections: Array.isArray(stored.sections) ? stored.sections.filter((item): item is SectionId => knownIds.has(item as SectionId)) : defaultData.sections,
          fragments: Array.isArray(stored.fragments) ? stored.fragments : [],
        });
      }
      const storedTheme = localStorage.getItem(themeKey);
      if (themes.some((item) => item.id === storedTheme)) setTheme(storedTheme as ThemeId);
    } catch { setNotice('本地存储不可用，仍可复制或导出'); }
    finally { setReady(true); }
  }, []);

  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(storageKey, JSON.stringify(data));
      localStorage.setItem(themeKey, theme);
    } catch { setNotice('本地存储不可用，仍可复制或导出'); }
  }, [data, theme, ready]);

  const activeSections = twinSections.filter((section) => data.sections.includes(section.id));
  const latest = useMemo(() => data.fragments[0], [data.fragments]);
  const sectionCounts = useMemo(() => Object.fromEntries(twinSections.map((section) => [section.id, data.fragments.filter((fragment) => fragment.sections.includes(section.id)).length])), [data.fragments]);

  function chooseSection(id: SectionId) { setData((current) => ({ ...current, sections: [id] })); scrollTo('start'); }

  function saveFragment() {
    const body = data.source.trim();
    if (!body) { setNotice('先放入一段关于你的真实材料'); return; }
    if (!data.sections.length) { setNotice('至少选择一个要形成的栏目'); return; }
    const fragment: Fragment = {
      id: safeId(),
      title: data.focus.trim() || body.split(/\n|。/)[0].slice(0, 30) || '未命名片段',
      body,
      date: new Date().toISOString(),
      sections: data.sections,
    };
    setData((current) => ({ ...current, source: '', focus: '', fragments: [fragment, ...current.fragments] }));
    setNotice('新的分身片段已留在本机');
  }

  async function copyPrompt() {
    const sectionInstructions = activeSections.map((section) => `- ${section.name}：${section.prompt}`).join('\n');
    const prompt = [
      '请使用 distill-me，把下面的材料整理成我的数字分身内容。',
      `本次主题：${data.focus.trim() || '请根据材料概括'}`,
      '目标栏目：',
      sectionInstructions || '- 请先判断最适合的栏目，并说明理由',
      '',
      '共同要求：只写材料能支持的内容；区分事实、本人判断与 Agent 归纳；保留来源、不确定性和适用边界；先返回草稿，不发布、不部署、不跨站同步。',
      '',
      '原始材料：',
      data.source.trim() || '（请在这里粘贴材料）',
    ].join('\n');
    try { await navigator.clipboard.writeText(prompt); setNotice('已复制数字分身整理请求'); }
    catch { setNotice('复制失败，请手动选择文本'); }
  }

  function exportData() {
    const blob = new Blob([JSON.stringify({ exportedAt: new Date().toISOString(), ...data }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `distill-me-${new Date().toISOString().slice(0, 10)}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
    setNotice('数字分身数据已导出');
  }

  function removeFragment(id: string) { setData((current) => ({ ...current, fragments: current.fragments.filter((fragment) => fragment.id !== id) })); setNotice('已从本机移除这个片段'); }

  return (
    <div className={`site-shell theme-${theme}`}>
      <header className="site-header">
        <button className="site-identity" type="button" onClick={() => scrollTo('overview')} aria-label="返回首页"><span className="site-identity-mark" aria-hidden="true">D</span><span>Distill Me<small>YOUR DIGITAL TWIN</small></span></button>
        <nav className="site-nav" aria-label="数字分身栏目">{twinSections.map((section) => <button key={section.id} type="button" onClick={() => scrollTo(section.id)}>{section.name}</button>)}</nav>
        <div className="site-status" aria-live="polite"><span />{notice}</div><span className="header-rule" aria-hidden="true" />
      </header>

      <main className="site-workspace">
        <section className="identity-hero" id="overview" aria-labelledby="identity-title">
          <div className="identity-overline"><span>DISTILL ME</span><span>A DIGITAL TWIN THAT GROWS WITH YOU</span></div>
          <div className="identity-main">
            <div className="identity-copy"><span className="identity-kicker">从真实材料里，长出一个可以被认识的你</span><h1 id="identity-title">把散落的你，<span>整理成一个持续生长的数字分身。</span></h1><p className="identity-description">你的经历、做事方式、文章和收藏，本来就散落在聊天、笔记与项目里。Distill Me 把它们整理成可以阅读、可以追问、也可以继续更新的你。</p><div className="identity-actions"><button className="primary-button" type="button" onClick={() => scrollTo('start')}>开始建立我的分身 <span aria-hidden="true">→</span></button><button className="secondary-button" type="button" onClick={() => scrollTo('twin')}>看看它如何形成 <span aria-hidden="true">↗</span></button></div></div>
            <nav className="identity-route" aria-label="认识数字分身"><span>一个完整的数字分身</span><button type="button" onClick={() => scrollTo('memory')}><small>01 / 认识你</small><strong>有来处</strong><span aria-hidden="true">↗</span></button><button type="button" onClick={() => scrollTo('practice')}><small>02 / 理解你</small><strong>有方法</strong><span aria-hidden="true">↗</span></button><button type="button" onClick={() => scrollTo('topics')}><small>03 / 看见方向</small><strong>有关注</strong><span aria-hidden="true">↗</span></button></nav>
          </div>
          <div className="identity-bottom"><div className="identity-count"><span><strong>5</strong> 个核心栏目</span><span><strong>{data.fragments.length}</strong> 个本地片段</span><span><strong>0</strong> 次自动上传</span></div><div className="identity-skill"><div><span className="eyebrow">START WITH WHAT YOU ALREADY HAVE</span><h2>不用先写自我介绍</h2><p>给它一段聊天、一篇笔记或一个项目复盘，数字分身会从真实材料里慢慢长出来。</p></div><button className="compact-button" type="button" onClick={() => scrollTo('start')}>放入第一段材料 <span aria-hidden="true">→</span></button></div></div>
        </section>

        <section className="home-section twin-section" id="twin" aria-labelledby="twin-title">
          <div className="section-heading"><span>THE SHAPE OF A PERSON</span><div><h2 id="twin-title">一个人，值得从 5 个方向被认识</h2><p>这 5 个栏目来自一个长期生长的真实数字分身。它们不是资料分类，而是数字分身逐渐变得完整的五个侧面。</p></div></div>
          <div className="twin-map">{twinSections.map((section, index) => <article className="twin-card" id={section.id} key={section.id}><div className="twin-card-top"><span className="twin-index">{String(index + 1).padStart(2, '0')}</span><span className="twin-mark" aria-hidden="true">{section.mark}</span></div><span className="eyebrow">{section.code}</span><h3>{section.name}</h3><strong>{section.meaning}</strong><p>{section.promise}</p><button type="button" onClick={() => chooseSection(section.id)}>从这里开始 <span aria-hidden="true">↗</span></button></article>)}</div>
        </section>

        <section className="home-section start-section" id="start" aria-labelledby="start-title">
          <div className="section-heading"><span>FROM MATERIAL TO SELF</span><div><h2 id="start-title">从一段你已经拥有的材料开始</h2><p>不用填复杂档案。选择它要进入的栏目，把原始材料交给工作台；你可以先留在本地，也可以复制给 Agent 继续蒸馏。</p></div></div>
          <div className="start-grid"><div className="material-form"><label htmlFor="focus">它大概关于什么</label><input id="focus" value={data.focus} onChange={(event) => setData((current) => ({ ...current, focus: event.target.value }))} placeholder="例如：我为什么决定重做这个产品" /><label htmlFor="source">把真实材料放进来</label><textarea id="source" value={data.source} onChange={(event) => setData((current) => ({ ...current, source: event.target.value }))} placeholder="一段聊天、一篇笔记、一次复盘，或任何能代表你的内容。它只保存在当前浏览器。" /></div><aside className="destination-panel"><span className="eyebrow">WHERE IT BELONGS</span><h3>它会让哪一部分的你更完整？</h3><ToggleGroup.Root className="destination-list" type="multiple" value={data.sections} onValueChange={(value) => setData((current) => ({ ...current, sections: value as SectionId[] }))} aria-label="选择数字分身栏目">{twinSections.map((section) => <ToggleGroup.Item key={section.id} value={section.id} aria-label={section.name}><span className="destination-mark" aria-hidden="true">{section.mark}</span><span><strong>{section.name}</strong><small>{section.meaning}</small></span><span className="destination-state">{data.sections.includes(section.id) ? '已选择' : '选择'}</span></ToggleGroup.Item>)}</ToggleGroup.Root><div className="start-actions"><button className="primary-button" type="button" onClick={saveFragment}>留在我的分身里 <span aria-hidden="true">→</span></button><button className="secondary-button" type="button" onClick={copyPrompt}>交给 Agent 蒸馏</button></div></aside></div>
        </section>

        <section className="home-section forming-section" aria-labelledby="forming-title">
          <div className="section-heading section-heading-row"><span>THE TWIN TAKES SHAPE</span><div><h2 id="forming-title">你的分身，正在形成</h2><p>{latest ? `最近在 ${formatDate(latest.date)} 留下了“${latest.title}”。` : '还没有内容也没关系。一个可信的数字分身，本来就应该从真实材料开始。'}</p></div><button className="text-button" type="button" onClick={exportData}>导出我的数据 ↗</button></div>
          <div className="forming-grid">{twinSections.map((section) => <article key={section.id}><span className="forming-mark" aria-hidden="true">{section.mark}</span><div><strong>{section.name}</strong><small>{sectionCounts[section.id]} 个片段</small></div></article>)}</div>
          {data.fragments.length ? <div className="fragment-grid">{data.fragments.map((fragment) => <article className="fragment-card" key={fragment.id}><div className="fragment-meta"><time dateTime={fragment.date}>{formatDate(fragment.date)}</time><span>{fragment.sections.map((id) => twinSections.find((section) => section.id === id)?.name).filter(Boolean).join(' · ')}</span></div><h3>{fragment.title}</h3><p>{fragment.body}</p><button type="button" onClick={() => removeFragment(fragment.id)}>从本机移除</button></article>)}</div> : <div className="empty-state"><span>YOUR FIRST TRACE</span><h3>不用完整，先留下一段真实的你。</h3><button className="secondary-button" type="button" onClick={() => scrollTo('start')}>放入第一段材料 ↗</button></div>}
        </section>

        <section className="home-section trust-section" aria-labelledby="trust-title"><div className="trust-copy"><span className="eyebrow">LOCAL BY DEFAULT</span><h2 id="trust-title">数字分身属于你，边界也由你决定。</h2></div><div className="trust-points"><p><strong>只在本机</strong><span>没有账号、数据库或远程服务。</span></p><p><strong>先是草稿</strong><span>没有你的明确决定，不发布也不同步。</span></p><p><strong>始终有依据</strong><span>区分你的表达、事实来源和 Agent 归纳。</span></p></div></section>
        <footer className="page-footer">让数字分身从真实的你开始。<div><span>Distill Me · Your Digital Twin</span><span>Local first · No deployment</span></div></footer>
      </main>

      <aside className="theme-dock" aria-label="主题"><span>主题</span><ToggleGroup.Root type="single" value={theme} onValueChange={(value) => value && setTheme(value as ThemeId)} aria-label="切换主题">{themes.map((item) => <ToggleGroup.Item key={item.id} value={item.id} aria-label={item.label} title={item.label}><span aria-hidden="true" /></ToggleGroup.Item>)}</ToggleGroup.Root></aside>
    </div>
  );
}
