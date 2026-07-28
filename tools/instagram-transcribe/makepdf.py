import os
USER = os.environ.get('IG_USER', 'account')
import json, os, re, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
GO, MIN = 'HeiseiKakuGo-W5', 'HeiseiMin-W3'

title_s = ParagraphStyle('t', fontName=GO, fontSize=15, leading=22, spaceAfter=4,
                         textColor=colors.HexColor('#1a1a2e'))
meta_s  = ParagraphStyle('m', fontName=GO, fontSize=8.5, leading=13,
                         textColor=colors.HexColor('#6b6b80'))
link_s  = ParagraphStyle('l', fontName=GO, fontSize=8, leading=12,
                         textColor=colors.HexColor('#7a5fa8'))
body_s  = ParagraphStyle('b', fontName=MIN, fontSize=11.5, leading=21, spaceAfter=7)
note_s  = ParagraphStyle('n', fontName=GO, fontSize=10, leading=18,
                         textColor=colors.HexColor('#8a8a9a'))

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

meta = json.load(open('meta.json'))
doc_src = open('ALL_TRANSCRIPTS.md', encoding='utf-8').read()
blocks = doc_src.split('\n## ')[1:]

os.makedirs('pdf', exist_ok=True)
made, skipped = 0, 0
index = []
for b in blocks:
    lines = ('## ' + b).split('\n')
    head = lines[0]
    m = re.match(r'## (\d{4}-\d{2}-\d{2})\s+\[([A-Za-z0-9_-]+)\]', head)
    date, code = m.group(1), m.group(2)
    rest = [l for l in lines[1:] if l.strip()]
    info = rest[0].strip('*') if rest and rest[0].startswith('*') else ''
    body = [l for l in rest[1:]]
    speech = [l for l in body if not l.startswith('>')]
    if not speech:
        skipped += 1
        continue
    mm_ = meta.get(code, {})
    fn = f'pdf/{date}_{code}.pdf'
    d = SimpleDocTemplate(fn, pagesize=A4,
                          leftMargin=22*mm, rightMargin=22*mm,
                          topMargin=20*mm, bottomMargin=18*mm,
                          title=f'{date} @{USER}', author=USER)
    # headline = first line of transcript, trimmed
    head_txt = re.sub(r'^\d+[\.\、]\s*', '', speech[0])[:28]
    flow = [Paragraph(esc(head_txt) + ('…' if len(speech[0]) > 28 else ''), title_s),
            Paragraph(f'@{USER} ／ {date} ／ {esc(info)}', meta_s),
            Paragraph(f'<link href="{mm_.get("url","")}">{mm_.get("url","")}</link>', link_s),
            Spacer(1, 5*mm),
            HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#d9d4e3')),
            Spacer(1, 5*mm)]
    for l in speech:
        flow.append(Paragraph(esc(l), body_s))
    flow += [Spacer(1, 6*mm),
             HRFlowable(width='100%', thickness=0.4, color=colors.HexColor('#e5e1ec')),
             Spacer(1, 2*mm),
             Paragraph('動画音声の自動文字起こし（Whisper large-v3-turbo）。誤変換が含まれる場合があります。', note_s)]
    d.build(flow)
    made += 1
    index.append((date, code, head_txt, os.path.basename(fn)))

print(f'PDF作成: {made}件 / 発話なしのためスキップ: {skipped}件')
json.dump(index, open('pdf_index.json','w'), ensure_ascii=False)
