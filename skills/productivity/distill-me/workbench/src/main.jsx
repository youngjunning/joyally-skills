import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import './themes.css';

const presets = ['重要判断', '关键进展', '资料收藏', '待跟进', '文章草稿'];
const key = 'distill-me-workbench-v3';
const blank = () => ({ source: '', focus: '', columns: presets, items: [] });
function load() { try { return { ...blank(), ...JSON.parse(localStorage.getItem(key) || '{}') }; } catch { return blank(); } }

function App() {
  const [data, setData] = useState(load); const [newColumn, setNewColumn] = useState(''); const [notice, setNotice] = useState('本地草稿，未发送到任何服务'); const [theme, setTheme] = useState('qingshan');
  useEffect(() => { try { localStorage.setItem(key, JSON.stringify(data)); } catch { setNotice('浏览器禁止本地保存；仍可导出 JSON'); } }, [data]);
  const patch = value => setData(current => ({ ...current, ...value }));
  const add = () => { if (!data.source.trim()) return setNotice('先写下本次材料'); patch({ items: [...data.items, { id: crypto.randomUUID(), title: data.focus || '未命名蒸馏', body: data.source, date: Date.now(), columns: data.columns }] }); setNotice('已加入本地时间线'); };
  const prompt = `请用 distill-me 整理以下材料。\n\n栏目：${data.columns.join('、')}\n${data.focus ? `关注重点：${data.focus}\n` : ''}要求：只输出可编辑草稿；保留出处和不确定性；不要将你的建议归为我的事实；不要写入、发布或同步任何位置。\n\n材料：\n${data.source || '（待填写）'}`;
  const copy = async () => { try { await navigator.clipboard.writeText(prompt); setNotice('请求已复制，可粘贴给千问办公或 Codex'); } catch { setNotice('请手动复制请求'); } };
  const exportData = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })); a.download = 'distill-me.json'; a.click(); };
  return <main className={`theme-${theme}`}>
    <header><div><p className="eyebrow">DISTILL ME · LOCAL WORKBENCH</p><h1>让经历留下<br/><em>可续接的线索。</em></h1><p>本地整理，再决定是否交给 Agent 或保存。</p></div><aside><i/> {notice}<small>本地优先 · 可导入导出</small></aside></header>
    <div className="themes">{[['qingshan','青山湖'],['xihu','西湖'],['maldives','马尔代夫']].map(([id,label]) => <button className={theme === id ? 'selected' : ''} key={id} onClick={() => setTheme(id)}>{label}</button>)}</div><section className="board"><nav>{['收集材料', '选择栏目', '交给 Agent'].map((label, index) => <div className={index === 0 ? 'on' : ''} key={label}><b>0{index + 1}</b>{label}</div>)}</nav>
      <section className="panel compose"><p className="kicker">THIS SESSION</p><h2>把原始材料放在这里</h2><label>本次重点<input value={data.focus} onChange={event => patch({ focus: event.target.value })} placeholder="例如：提炼可写成文章的观察"/></label><label>材料<textarea value={data.source} onChange={event => patch({ source: event.target.value })} placeholder="粘贴聊天片段、会议记录、阅读摘录或随手笔记……"/></label><div className="buttons"><button className="primary" onClick={add}>加入本地草稿</button><button onClick={() => patch({ source: '', focus: '' })}>清空输入</button></div></section>
      <section className="panel lenses"><p className="kicker">YOUR LENSES</p><h2>这次要看什么</h2><p className="hint">预设可删、可改、可加；文章草稿只生成选题与提纲。</p><div className="chips">{data.columns.map(name => <button key={name} onClick={() => patch({ columns: data.columns.filter(item => item !== name) })}>{name} ×</button>)}</div><div className="adder"><input value={newColumn} onChange={event => setNewColumn(event.target.value)} placeholder="新增一个栏目"/><button onClick={() => { if (newColumn.trim()) { patch({ columns: [...data.columns, newColumn.trim()] }); setNewColumn(''); } }}>添加</button></div><div className="buttons"><button className="primary" onClick={copy}>复制给 Agent 的请求</button><button onClick={exportData}>导出 JSON</button></div></section>
    </section>
    <section className="trail"><div><p className="kicker">LOCAL TRAIL</p><h2>已经留下的草稿</h2></div>{data.items.length ? <ol>{[...data.items].reverse().map((item, index) => <li key={item.id}><time>{new Intl.DateTimeFormat('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(item.date)}</time><b>{String(data.items.length - index).padStart(2, '0')}</b><article><h3>{item.title}</h3><small>{item.columns.join(' · ')}</small><button onClick={() => patch({ items: data.items.filter(candidate => candidate.id !== item.id) })}>移除</button><p>{item.body}</p></article></li>)}</ol> : <div className="empty">还没有草稿。把一次材料加入工作台，它会在这里形成可回看的时间线。</div>}</section>
    <footer>需要真实保存时，请明确指定文件位置与写入授权。</footer>
  </main>;
}

createRoot(document.getElementById('root')).render(<App/>);
