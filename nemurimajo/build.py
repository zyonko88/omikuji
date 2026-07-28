# -*- coding: utf-8 -*-
"""@nemurimajo 全投稿ビューアのビルドスクリプト

source/ の文字起こし4ファイルを読み、1枚の index.html（サーバー不要）を生成する。

    python3 build.py
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
OUT = HERE / "index.html"

POST_RE = re.compile(
    r"^## (\d{4}-\d{2}-\d{2})\s+\[([^\]]+)\]\(([^)]+)\)\s*$"
)
META_RE = re.compile(
    r"^\*(\S+)\s*／\s*いいね\s*([\d,]+)\s*／\s*コメント\s*([\d,]+)\*\s*$"
)

# 項目（テーマ）の定義。キーワードは (語, 重み)。
# 全項目を採点し、いちばん点の高い項目に入れる（同点なら定義の早いほう）。
# 重み 3 = その項目にしか出てこない語、1 = よそでも出るがヒントになる語。
THEMES = [
    ("kotoba", "ことばと現実", "🌙",
     "口にした言葉が、そのまま暮らしになる",
     [("アファ", 3), ("アフォ", 3), ("引き寄せ", 3), ("潜在意識", 3),
      ("自己暗示", 3), ("鏡の前", 3), ("宇宙は", 3), ("唱え", 2),
      ("言葉と行動", 3), ("発する言葉", 3), ("想像", 2), ("現実化", 3),
      ("言葉", 1), ("願い", 1)]),
    ("kyoukai", "境界線と人間関係", "🕊",
     "近づく相手と、離れる相手を自分で選ぶ",
     [("境界線", 3), ("人間関係", 3), ("合わせ鏡", 3), ("不機嫌", 3),
      ("因果応報", 3), ("悪口", 3), ("批評", 2), ("離れる", 2),
      ("立ち去る", 3), ("付き合", 2), ("傷つく", 2), ("傷つけ", 2),
      ("相手", 1), ("他人", 1)]),
    ("jibun", "自分を大切にする", "🤍",
     "いちばん先に、自分を丁寧にあつかう",
     [("自分を大切", 3), ("自己愛", 3), ("自分を愛", 3), ("自己肯定", 3),
      ("自分の価値", 3), ("粗末", 3), ("自分を守", 3), ("インナー", 3),
      ("アダルトチルド", 3), ("本音", 2), ("自分の気持ち", 2),
      ("自分に話しかけ", 3), ("自分自身の体", 2), ("自分と向き合", 2)]),
    ("kokoro", "こころの整え方", "🌿",
     "揺れた日に、静かさを取り戻すために",
     [("メンタル", 3), ("感情", 2), ("不安", 2), ("穏やか", 2),
      ("沈黙", 3), ("心が折れ", 3), ("自尊心", 3), ("ストア", 3),
      ("落ち込", 2), ("怒り", 2), ("悲しみ", 2), ("疲れ", 1), ("焦", 1)]),
    ("tebanasu", "手放す・委ねる", "🍃",
     "力を抜いたところから、流れが動きだす",
     [("手放", 3), ("委ね", 3), ("執着", 3), ("コントロール", 3),
      ("固執", 3), ("受け入れ", 2), ("流れに", 2), ("過去", 1)]),
    ("koudou", "行動と習慣", "✦",
     "変化は、決意ではなく行動から始まる",
     [("習慣", 3), ("好転", 3), ("早起き", 3), ("ルーティン", 3),
      ("決断", 2), ("挑戦", 2), ("成長", 2), ("行動", 1), ("選択", 1),
      ("努力", 1), ("続け", 1)]),
    ("yutakasa", "豊かさとお金", "🌾",
     "すでに在るものに気づくところから",
     [("お金", 3), ("豊かさ", 3), ("足るを知", 3), ("樽を知", 3),
      ("収入", 3), ("感謝", 2), ("受け取る力", 3), ("すでに持って", 2),
      ("仕事", 1), ("成功", 1)]),
    ("karada", "からだと暮らし", "🌱",
     "月のリズム、食べるもの、住む場所",
     [("満月", 3), ("新月", 3), ("月周期", 3), ("月の暦", 3), ("生理", 3),
      ("ホルモン", 3), ("畑", 3), ("野菜", 3), ("種まき", 3), ("菜食", 3),
      ("薬味", 3), ("食事", 3), ("睡眠", 3), ("温泉", 3), ("掃除", 3),
      ("健康", 2), ("暮らし", 1), ("環境", 1)]),
    ("onna", "女性としての生き方", "🌸",
     "誰かの正しさではなく、自分の順番で",
     [("女性は", 3), ("女性たち", 3), ("私たち女性", 3), ("シングルマザー", 3),
      ("レディーファースト", 3), ("愛嬌", 3), ("結婚", 2), ("出産", 2),
      ("母親", 2), ("女性解放", 3)]),
]
OTHER = ("sonota", "そのほか", "◦", "どの項目にも入りきらなかった一編")

NO_VOICE_MARK = "（発話なし"
NO_AUDIO_MARK = "（音声トラックなし"


def classify(body: str) -> str:
    best, best_score = OTHER[0], 0
    for key, _, _, _, words in THEMES:
        score = sum(w * body.count(t) for t, w in words)
        if score > best_score:
            best, best_score = key, score
    return best


def make_title(body: str) -> str:
    """本文の冒頭から、一覧に出す見出しを作る。"""
    first = ""
    for line in body.split("\n"):
        s = line.strip()
        if s and not s.startswith(">"):
            first = s
            break
    if not first:
        return "（音声なしの投稿）"
    # 文の切れ目で区切って、一覧で1〜2行に収まる長さの見出しにする
    for sep in ("。", "、", "　", " "):
        pos = first.find(sep)
        while pos != -1:
            if 10 <= pos <= 24:
                return first[:pos]
            pos = first.find(sep, pos + 1)
    return first if len(first) <= 24 else first[:23] + "…"


def parse_file(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    posts = []
    cur = None
    for line in lines:
        m = POST_RE.match(line)
        if m:
            if cur:
                posts.append(cur)
            cur = {"date": m.group(1), "id": m.group(2), "url": m.group(3),
                   "kind": "", "like": 0, "cmt": 0, "lines": []}
            continue
        if cur is None:
            continue
        mm = META_RE.match(line)
        if mm and not cur["kind"]:
            cur["kind"] = mm.group(1)
            cur["like"] = int(mm.group(2).replace(",", ""))
            cur["cmt"] = int(mm.group(3).replace(",", ""))
            continue
        cur["lines"].append(line)
    if cur:
        posts.append(cur)
    return posts


def main():
    raw = []
    for path in sorted(SRC.glob("*_文字起こし_*of4.md")):
        raw.extend(parse_file(path))

    entries = []
    for p in raw:
        body = "\n".join(p["lines"]).strip("\n")
        while "\n\n\n" in body:
            body = body.replace("\n\n\n", "\n\n")
        body = body.strip()
        has_voice = not (body.startswith(">") and
                         (NO_VOICE_MARK in body or NO_AUDIO_MARK in body))
        entries.append({
            "d": p["date"],
            "u": p["url"],
            "k": p["kind"],
            "l": p["like"],
            "c": p["cmt"],
            "v": 1 if has_voice else 0,
            "t": make_title(body) if has_voice else "（音声なしの投稿）",
            "b": body,
            "th": classify(body) if has_voice else OTHER[0],
        })

    entries.sort(key=lambda e: e["d"], reverse=True)
    voiced = [e for e in entries if e["v"]]

    themes = [{"k": k, "n": n, "i": i, "s": s} for k, n, i, s, _ in THEMES]
    themes.append({"k": OTHER[0], "n": OTHER[1], "i": OTHER[2], "s": OTHER[3]})

    data = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    th_json = json.dumps(themes, ensure_ascii=False, separators=(",", ":"))

    html = (TEMPLATE
            .replace("__DATA__", data)
            .replace("__THEMES__", th_json)
            .replace("__TOTAL__", str(len(entries)))
            .replace("__VOICED__", str(len(voiced))))
    OUT.write_text(html, encoding="utf-8")

    counts = {}
    for e in voiced:
        counts[e["th"]] = counts.get(e["th"], 0) + 1
    print(f"OK: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"全{len(entries)}件 / 本文あり{len(voiced)}件")
    for t in themes:
        print(f"  {t['n']}: {counts.get(t['k'], 0)}")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>眠り魔女のことば｜項目べつアーカイブ</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;600&family=Zen+Maru+Gothic:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#faf6f3; --card:#fffdfc; --ink:#4a3f42; --soft:#8b7a7e;
  --rose:#b3697f; --rose-deep:#96506a; --rose-pale:#f7e7ec; --rose-mist:#fcf3f6;
  --gold:#c0a173; --line:#eeded9;
  --serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho",serif;
  --sans:"Zen Maru Gothic","Hiragino Maru Gothic ProN","Hiragino Kaku Gothic ProN",sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.9;
  background-image:radial-gradient(ellipse 90% 45% at 50% -8%, #f6e6ec 0%, transparent 62%)}
.wrap{max-width:660px;margin:0 auto;padding:0 18px 90px}

header{text-align:center;padding:32px 0 14px}
.moon{display:inline-flex;align-items:center;justify-content:center;width:54px;height:54px;
  border:1.5px solid var(--rose);border-radius:50%;background:var(--card);
  font-size:22px;margin-bottom:10px}
h1{font-family:var(--serif);font-weight:500;font-size:23px;letter-spacing:.12em}
.tagline{font-size:11.5px;color:var(--soft);letter-spacing:.2em;margin-top:6px}
.tagline::before,.tagline::after{content:"—";margin:0 9px;color:var(--gold)}

nav{position:sticky;top:0;z-index:20;background:rgba(250,246,243,.93);backdrop-filter:blur(8px);
  display:flex;gap:6px;justify-content:center;flex-wrap:wrap;padding:10px 0 13px;margin-bottom:6px}
nav button{font-family:var(--sans);font-size:13px;letter-spacing:.06em;color:var(--soft);
  background:var(--card);border:1px solid var(--line);border-radius:999px;
  padding:8px 16px;cursor:pointer;transition:all .2s}
nav button.on{background:var(--rose);border-color:var(--rose);color:#fff;
  box-shadow:0 3px 10px rgba(179,105,127,.28)}

.label{font-size:11.5px;letter-spacing:.24em;color:var(--rose);text-align:center;margin:22px 0 14px}
.label::before,.label::after{content:"·";margin:0 11px;color:var(--gold)}
.hint{text-align:center;font-size:12.5px;color:var(--soft);margin:24px 0;line-height:2}

/* 項目カード */
.themes{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(min-width:540px){.themes{grid-template-columns:1fr 1fr 1fr}}
.theme{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 12px;
  text-align:center;cursor:pointer;transition:all .2s}
.theme:hover{border-color:var(--rose);box-shadow:0 5px 16px rgba(179,105,127,.13);transform:translateY(-2px)}
.theme .ic{font-size:19px;display:block;margin-bottom:5px}
.theme .nm{font-family:var(--serif);font-size:14.5px;color:var(--rose-deep);letter-spacing:.03em}
.theme .ct{font-size:10.5px;color:var(--gold);margin-top:3px;letter-spacing:.08em}
.theme .ds{font-size:10.5px;color:var(--soft);margin-top:6px;line-height:1.65}

/* 一覧の行 */
.row{display:flex;align-items:flex-start;gap:13px;background:var(--card);border:1px solid var(--line);
  border-radius:13px;padding:13px 16px;margin-bottom:8px;cursor:pointer;transition:all .15s}
.row:hover{border-color:var(--rose);transform:translateY(-1px)}
.row .dt{font-family:var(--serif);font-size:12px;color:var(--gold);min-width:62px;
  letter-spacing:.03em;padding-top:3px}
.row .tx{flex:1;font-size:14px;line-height:1.7}
.row .tx .sub{display:block;font-size:10.5px;color:var(--soft);margin-top:3px;letter-spacing:.06em}
.row .bk{color:var(--rose);font-size:14px;padding-top:2px}

/* 本文 */
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;
  box-shadow:0 4px 18px rgba(120,80,85,.06);padding:26px 24px;margin-bottom:14px}
.post .meta{text-align:center;font-family:var(--serif);font-size:12.5px;color:var(--soft);
  letter-spacing:.1em;margin-bottom:6px}
.post h2{font-family:var(--serif);font-weight:500;font-size:19px;line-height:1.75;text-align:center;
  color:var(--rose-deep);margin:2px 0 10px;letter-spacing:.03em}
.post .chip{display:block;text-align:center;font-size:10.5px;color:var(--soft);letter-spacing:.13em;
  margin-bottom:16px}
.post .rule{width:54px;height:1px;background:var(--gold);margin:0 auto 22px;opacity:.6}
.post .body{font-family:var(--serif);font-size:15.5px;line-height:2.2;letter-spacing:.02em}
.post .body p{margin-bottom:1.3em}
.post .body ol{padding-left:1.5em;margin-bottom:1.3em}
.post .body ol li{margin-bottom:.5em}
.post .body blockquote{color:var(--soft);font-size:14px;text-align:center;font-family:var(--sans)}
.post .link{display:block;text-align:center;font-size:11.5px;color:var(--gold);
  letter-spacing:.08em;margin-top:24px;text-decoration:none}
.post .link:hover{color:var(--rose)}

.pager{display:flex;justify-content:space-between;align-items:center;gap:9px;margin-top:6px}
.pager button{font-family:var(--sans);font-size:12.5px;color:var(--rose-deep);background:var(--card);
  border:1px solid var(--line);border-radius:999px;padding:9px 16px;cursor:pointer}
.pager button:disabled{opacity:.3;cursor:default}
.mark{font-size:12.5px;border-radius:999px;border:1px solid var(--rose-pale);background:var(--rose-mist);
  color:var(--rose-deep);padding:9px 16px;cursor:pointer;font-family:var(--sans)}
.mark.on{background:var(--rose);color:#fff;border-color:var(--rose)}

.back{display:inline-block;font-size:12.5px;color:var(--rose-deep);cursor:pointer;margin-bottom:12px;
  background:none;border:none;font-family:var(--sans)}
.head{text-align:center;margin-bottom:14px}
.head .nm{font-family:var(--serif);font-size:20px;color:var(--rose-deep);letter-spacing:.08em}
.head .ds{font-size:12px;color:var(--soft);margin-top:3px}

.search{display:flex;margin-bottom:16px}
.search input{flex:1;font-family:var(--sans);font-size:15px;padding:12px 18px;border:1px solid var(--line);
  border-radius:999px;background:var(--card);color:var(--ink);outline:none}
.search input:focus{border-color:var(--rose)}

.omakase{display:block;margin:2px auto 0;background:none;border:none;color:var(--gold);
  font-size:11.5px;letter-spacing:.13em;cursor:pointer;font-family:var(--sans);padding:8px}
.omakase:hover{color:var(--rose)}
footer{text-align:center;font-size:10.5px;color:var(--soft);letter-spacing:.1em;margin-top:38px;line-height:2}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="moon">🌙</div>
    <h1>眠り魔女のことば</h1>
    <div class="tagline">項目べつに読みかえす、自分のためのアーカイブ</div>
  </header>

  <nav>
    <button id="t-home" class="on">項目から</button>
    <button id="t-all">ぜんぶ</button>
    <button id="t-search">さがす</button>
    <button id="t-mark">しおり</button>
  </nav>

  <main id="view"></main>

  <footer>
    Instagram @nemurimajo の全__TOTAL__投稿（本文のあるもの __VOICED__ 件）<br>
    音声を自動文字起こししたものです。固有名詞などに誤りが含まれる場合があります。
  </footer>
</div>

<script id="data" type="application/json">__DATA__</script>
<script id="themes" type="application/json">__THEMES__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const THEMES = JSON.parse(document.getElementById('themes').textContent);
const TH = Object.fromEntries(THEMES.map(t => [t.k, t]));
const view = document.getElementById('view');
const $ = s => document.querySelector(s);

const KEY = 'nemurimajo_marks';
const load = () => { try { return new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); } catch (e) { return new Set(); } };
const save = s => localStorage.setItem(KEY, JSON.stringify([...s]));
let marks = load();

let state = { tab: 'home', theme: null, q: '', open: null };

function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function jpDate(d){ const [y,m,dd] = d.split('-'); return `${y}.${+m}.${+dd}`; }

function mdToHtml(md){
  const blocks = [];
  let cur = [];
  for (const line of md.split('\n')) {
    if (line.trim() === '') { if (cur.length) { blocks.push(cur); cur = []; } }
    else cur.push(line);
  }
  if (cur.length) blocks.push(cur);

  let html = '';
  for (const b of blocks) {
    const first = b[0].trim();
    if (first.startsWith('>')) {
      html += `<blockquote>${esc(b.map(l => l.replace(/^>\s*/, '')).join(''))}</blockquote>`;
      continue;
    }
    if (/^\d+[.．、]\s*/.test(first)) {
      const items = b.filter(l => /^\d+[.．、]\s*/.test(l.trim()))
        .map(l => `<li>${esc(l.trim().replace(/^\d+[.．、]\s*/, ''))}</li>`).join('');
      const rest = b.filter(l => !/^\d+[.．、]\s*/.test(l.trim()));
      html += `<ol>${items}</ol>`;
      if (rest.length) html += `<p>${rest.map(esc).join('<br>')}</p>`;
      continue;
    }
    html += `<p>${b.map(esc).join('<br>')}</p>`;
  }
  return html;
}

function postCard(e){
  const t = TH[e.th];
  const i = DATA.indexOf(e);
  const on = marks.has(e.u);
  return `
  <div class="card post">
    <div class="meta">${jpDate(e.d)}　${esc(e.k)}</div>
    <h2>${esc(e.t)}</h2>
    <span class="chip">${t.i}　${esc(t.n)}</span>
    <div class="rule"></div>
    <div class="body">${mdToHtml(e.b)}</div>
    <a class="link" href="${e.u}" target="_blank" rel="noopener">元の投稿をInstagramで見る →</a>
  </div>
  <div class="pager">
    <button ${i >= DATA.length - 1 ? 'disabled' : ''} onclick="openAt(${i + 1})">← 前の投稿</button>
    <button class="mark ${on ? 'on' : ''}" onclick="toggle('${e.u}')">${on ? 'しおりを挟んだ 🔖' : 'しおりを挟む'}</button>
    <button ${i <= 0 ? 'disabled' : ''} onclick="openAt(${i - 1})">次の投稿 →</button>
  </div>`;
}

function row(e){
  const t = TH[e.th];
  const bk = marks.has(e.u) ? '<span class="bk">🔖</span>' : '';
  const i = DATA.indexOf(e);
  return `<div class="row" onclick="openAt(${i})">
    <span class="dt">${jpDate(e.d)}</span>
    <span class="tx">${esc(e.t)}<span class="sub">${t.i} ${esc(t.n)}</span></span>${bk}</div>`;
}

function setTab(tab){
  state.tab = tab; state.open = null; state.theme = null;
  for (const [k, id] of Object.entries({home:'t-home', all:'t-all', search:'t-search', mark:'t-mark'})) {
    document.getElementById(id).classList.toggle('on', k === tab);
  }
  render(); window.scrollTo({ top: 0 });
}
function openAt(i){
  if (i < 0 || i >= DATA.length) return;
  state.open = i; render(); window.scrollTo({ top: 0, behavior: 'smooth' });
}
function toggle(u){
  marks.has(u) ? marks.delete(u) : marks.add(u);
  save(marks); render();
}
function backName(){
  if (state.theme) return TH[state.theme].n + 'の一覧';
  return { home:'項目の一覧', all:'ぜんぶの一覧', search:'検索結果', mark:'しおり' }[state.tab];
}
function goBack(){ state.open = null; render(); window.scrollTo({ top: 0 }); }

function render(){
  if (state.open !== null) {
    view.innerHTML = `<button class="back" onclick="goBack()">‹ ${backName()}にもどる</button>`
      + postCard(DATA[state.open]);
    return;
  }
  if (state.tab === 'home') {
    if (state.theme) {
      const t = TH[state.theme];
      const list = DATA.filter(e => e.th === state.theme && e.v);
      view.innerHTML = `<button class="back" onclick="state.theme=null;render();window.scrollTo({top:0})">‹ 項目の一覧にもどる</button>
        <div class="head"><div class="nm">${t.i}　${esc(t.n)}</div><div class="ds">${esc(t.s)}　／　${list.length}件</div></div>
        ${list.map(row).join('')}`;
    } else {
      const cards = THEMES.map(t => {
        const n = DATA.filter(e => e.th === t.k && e.v).length;
        if (!n) return '';
        return `<div class="theme" onclick="state.theme='${t.k}';render();window.scrollTo({top:0})">
          <span class="ic">${t.i}</span><div class="nm">${esc(t.n)}</div>
          <div class="ct">${n}件</div><div class="ds">${esc(t.s)}</div></div>`;
      }).join('');
      const pool = DATA.filter(e => e.v);
      view.innerHTML = `<div class="label">読みたい項目をえらぶ</div><div class="themes">${cards}</div>
        <button class="omakase" onclick="openAt(DATA.indexOf(POOL[Math.floor(Math.random()*POOL.length)]))">✦ 今日の気分で、おまかせの一編をひらく</button>`;
      window.POOL = pool;
    }
    return;
  }
  if (state.tab === 'all') {
    const list = DATA.filter(e => e.v);
    view.innerHTML = `<div class="label">新しい順に ${list.length}件</div>` + list.map(row).join('');
    return;
  }
  if (state.tab === 'search') {
    view.innerHTML = `<div class="search"><input id="q" type="search" placeholder="ことばで さがす" value="${esc(state.q)}"></div><div id="res"></div>`;
    const input = $('#q');
    input.addEventListener('input', () => { state.q = input.value; results(); });
    results(); input.focus();
    return;
  }
  if (state.tab === 'mark') {
    const list = DATA.filter(e => marks.has(e.u));
    view.innerHTML = list.length
      ? `<div class="label">しおりを挟んだ ${list.length}件</div>` + list.map(row).join('')
      : '<p class="hint">まだ、しおりはありません。<br>気になった一編をひらいて「しおりを挟む」を押すと、ここに集まります。</p>';
  }
}

function results(){
  const q = state.q.trim();
  const box = $('#res');
  if (!box) return;
  if (!q) {
    box.innerHTML = '<p class="hint">本文のことばで探せます。<br>例：「境界線」「お金」「呼吸」「月」</p>';
    return;
  }
  const hits = DATA.filter(e => e.v && (e.t.includes(q) || e.b.includes(q)));
  box.innerHTML = hits.length
    ? `<div class="label">${hits.length}件 見つかりました</div>` + hits.map(row).join('')
    : '<p class="hint">見つかりませんでした。<br>別のことばでお試しください。</p>';
}

document.getElementById('t-home').onclick = () => setTab('home');
document.getElementById('t-all').onclick = () => setTab('all');
document.getElementById('t-search').onclick = () => setTab('search');
document.getElementById('t-mark').onclick = () => setTab('mark');
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
