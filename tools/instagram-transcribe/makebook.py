import os
USER = os.environ.get('IG_USER', 'account')
import json, os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                HRFlowable, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
GO, MIN = 'HeiseiKakuGo-W5', 'HeiseiMin-W3'
PURPLE = colors.HexColor('#5d4a7e')
GREY   = colors.HexColor('#6b6b80')
LIGHT  = colors.HexColor('#d9d4e3')

cover_t = ParagraphStyle('ct', fontName=GO, fontSize=26, leading=38, alignment=1,
                         textColor=PURPLE, spaceAfter=6)
cover_s = ParagraphStyle('cs', fontName=GO, fontSize=12, leading=20, alignment=1,
                         textColor=GREY)
h_style = ParagraphStyle('h', fontName=GO, fontSize=14, leading=21, spaceAfter=3,
                         textColor=colors.HexColor('#1a1a2e'))
meta_s  = ParagraphStyle('m', fontName=GO, fontSize=8.5, leading=13, textColor=GREY)
link_s  = ParagraphStyle('l', fontName=GO, fontSize=7.5, leading=12,
                         textColor=colors.HexColor('#7a5fa8'))
body_s  = ParagraphStyle('b', fontName=MIN, fontSize=11, leading=20, spaceAfter=6)
note_s  = ParagraphStyle('n', fontName=GO, fontSize=9, leading=15, textColor=GREY)
toc_h   = ParagraphStyle('th', fontName=GO, fontSize=16, leading=24,
                         textColor=PURPLE, spaceAfter=8)

class Book(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if getattr(flowable, '_bookmark', None):
            key, text, date = flowable._bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f'{date}  {text}', key, level=0)

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def footer(canv, doc):
    canv.saveState()
    canv.setFont(GO, 8)
    canv.setFillColor(GREY)
    if doc.page > 1:
        canv.drawCentredString(A4[0]/2, 12*mm, str(doc.page - 1))
        canv.drawRightString(A4[0]-20*mm, A4[1]-12*mm, f'@{USER} 音声文字起こし集')
    canv.restoreState()

meta = json.load(open('meta.json'))
src = open('ALL_TRANSCRIPTS.md', encoding='utf-8').read()
blocks = src.split('\n## ')[1:]

posts = []
for b in blocks:
    lines = ('## ' + b).split('\n')
    m = re.match(r'## (\d{4}-\d{2}-\d{2})\s+\[([A-Za-z0-9_-]+)\]', lines[0])
    date, code = m.group(1), m.group(2)
    rest = [l for l in lines[1:] if l.strip()]
    info = rest[0].strip('*') if rest and rest[0].startswith('*') else ''
    speech = [l for l in rest[1:] if not l.startswith('>')]
    if speech:
        posts.append((date, code, info, speech))

flow = []
# ---- cover ----
flow += [Spacer(1, 55*mm),
         Paragraph(f'@{USER}', cover_t),
         Paragraph('全投稿 音声文字起こし集', cover_t),
         Spacer(1, 10*mm),
         HRFlowable(width='45%', thickness=0.8, color=LIGHT, hAlign='CENTER'),
         Spacer(1, 8*mm),
         Paragraph(f'{posts[-1][0]} 〜 {posts[0][0]}', cover_s),
         Paragraph(f'収録 {len(posts)} 投稿（全234投稿のうち発話のあるもの）', cover_s),
         Spacer(1, 30*mm),
         Paragraph('Instagram のリール動画の音声を自動文字起こししたものです。', cover_s),
         Paragraph('固有名詞などに誤変換が含まれる場合があります。', cover_s),
         PageBreak()]

# ---- table of contents ----
flow.append(Paragraph('目次', toc_h))
flow.append(Spacer(1, 3*mm))
rows = [[Paragraph('<b>投稿日</b>', meta_s), Paragraph('<b>冒頭</b>', meta_s)]]
for date, code, info, speech in posts:
    head = re.sub(r'^\d+[\.\、]\s*', '', speech[0])
    head = head[:34] + ('…' if len(head) > 34 else '')
    rows.append([Paragraph(date, meta_s),
                 Paragraph(f'<link href="#{code}">{esc(head)}</link>', meta_s)])
t = Table(rows, colWidths=[24*mm, 132*mm], repeatRows=1)
t.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,0), 0.6, LIGHT),
    ('LINEBELOW', (0,1), (-1,-2), 0.25, colors.HexColor('#eeebf3')),
]))
flow += [t, PageBreak()]

# ---- body ----
for i, (date, code, info, speech) in enumerate(posts):
    head = re.sub(r'^\d+[\.\、]\s*', '', speech[0])
    head = head[:30] + ('…' if len(head) > 30 else '')
    p = Paragraph(f'<a name="{code}"/>{esc(head)}', h_style)
    p._bookmark = (code, head, date)
    flow += [p,
             Paragraph(f'{date} ／ {esc(info)}', meta_s),
             Paragraph(f'<link href="{meta.get(code,{}).get("url","")}">'
                       f'{meta.get(code,{}).get("url","")}</link>', link_s),
             Spacer(1, 4*mm),
             HRFlowable(width='100%', thickness=0.5, color=LIGHT),
             Spacer(1, 4*mm)]
    for l in speech:
        flow.append(Paragraph(esc(l), body_s))
    if i != len(posts) - 1:
        flow.append(PageBreak())

doc = Book(f'{USER}_全文字起こし.pdf', pagesize=A4,
           leftMargin=22*mm, rightMargin=22*mm, topMargin=20*mm, bottomMargin=20*mm,
           title=f'@{USER} 全投稿 音声文字起こし集', author=USER)
doc.build(flow, onFirstPage=footer, onLaterPages=footer)
print('収録:', len(posts), '投稿')
