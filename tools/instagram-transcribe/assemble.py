import os
USER = os.environ.get('IG_USER', 'account')
import json, os, re, datetime
meta = json.load(open('meta.json'))
clips = json.load(open('clips.json'))
durmap = {c['key']: c['dur'] for c in clips}

HALLU = ['ご視聴ありがとうございました', 'ご視聴いただきありがとうございました', 'チャンネル登録',
         'おだいじに', 'Thanks for watching', 'ありがとうございました。ありがとうございました']

def clean(segs):
    """Drop low-confidence / hallucinated segments, collapse repeats."""
    out, prev = [], None
    for s in segs:
        t = s['t'].strip()
        if not t: continue
        if s.get('ns', 0) > 0.6: continue
        if s.get('lp', 0) < -1.0: continue
        if any(h in t for h in HALLU) and len(t) < 40: continue
        if t == prev: continue          # exact immediate repeat
        prev = t
        out.append(t)
    return out

JP = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
LAT = re.compile(r'[A-Za-z]')

def classify(texts):
    """Return (kind, texts). kind: 'speech' | 'bgm' | 'none'"""
    # drop degenerate repeats (e.g. ドゥドゥドゥ..., ラララ)
    keep = []
    for t in texts:
        core = re.sub(r'\s|、|。', '', t)
        if len(core) >= 6 and len(set(core)) <= 3:
            continue
        keep.append(t)
    joined = ''.join(keep)
    if len(re.sub(r'\s', '', joined)) < 15:
        return 'none', []
    jp, lat = len(JP.findall(joined)), len(LAT.findall(joined))
    if lat > jp:
        return 'bgm', []
    return 'speech', keep

posts = {}
for fn in sorted(os.listdir('out')):
    if not fn.endswith('.json'): continue
    d = json.load(open('out/'+fn))
    key = d['key']
    code = key.split('__')[0]
    part = int(key.split('__')[1]) if '__' in key else 0
    if 'error' in d:
        posts.setdefault(code, []).append((part, None, d['error']))
        continue
    kind, texts = classify(clean(d.get('segments', [])))
    posts.setdefault(code, []).append((part, texts if kind == 'speech' else ('BGM' if kind == 'bgm' else []), None))

# include every post, even ones with no audio at all
for c in meta:
    posts.setdefault(c, [])
order = sorted(posts.keys(), key=lambda c: -(meta.get(c, {}).get('taken_at') or 0))
lines = []
lines.append(f"# @{USER} 全投稿 音声文字起こし\n")
lines.append(f"対象: 全{len(meta)}投稿中、音声のある動画クリップ {sum(len(v) for v in posts.values())} 本\n")
lines.append("新しい投稿順。文字起こしは Whisper large-v3-turbo による自動生成のため、固有名詞などに誤りが含まれる場合があります。\n")
lines.append("\n---\n")

nspeech = 0
for code in order:
    m = meta.get(code, {})
    parts = sorted(posts[code])
    lines.append(f"\n## {m.get('date','?')}  [{code}]({m.get('url')})\n")
    ptype = 'リール' if m.get('product_type') == 'clips' else ('カルーセル' if m.get('media_type') == 8 else '動画')
    lines.append(f"*{ptype} ／ いいね {m.get('like_count')} ／ コメント {m.get('comment_count')}*\n")
    any_text = False
    if not parts:
        lines.append("\n> （音声トラックなし／静止画投稿）\n")
    for part, texts, err in parts:
        label = f"\n**［動画 {part}］**\n" if part else ""
        if err:
            lines.append(label + f"\n> ⚠ 処理エラー: {err}\n"); continue
        if texts == 'BGM':
            lines.append(label + "\n> （発話なし・BGM楽曲のみ）\n"); continue
        if not texts:
            lines.append(label + "\n> （発話なし・BGMのみ）\n"); continue
        any_text = True
        lines.append(label + "\n" + "\n".join(texts) + "\n")
    if any_text: nspeech += 1

open('ALL_TRANSCRIPTS.md','w').write("\n".join(lines))
print("posts with transcript files:", len(posts), "| posts containing speech:", nspeech)
print("output chars:", sum(len(l) for l in lines))
