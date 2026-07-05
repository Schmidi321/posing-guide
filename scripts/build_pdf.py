# -*- coding: utf-8 -*-
"""Build the Posen-Guide PDF cheat sheet from data.js, embedding pose illustrations."""

import re
from pathlib import Path
from io import BytesIO
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
)

BASE = Path(r'C:\RufloWorkspace\posing-guide')
ILLUSTRATIONS = BASE / 'illustrations'

GOLD = colors.HexColor('#8f6f37')
DARK = colors.HexColor('#26231f')
GREY = colors.HexColor('#5a5348')
LIGHT_BG = colors.HexColor('#f6f1e9')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=28, textColor=GOLD, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=13, textColor=DARK, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle('SectionTitle', fontName='Helvetica-Bold', fontSize=20, textColor=GOLD, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle('CatTitle', fontName='Helvetica-Bold', fontSize=13, textColor=DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle('PoseText', fontName='Helvetica', fontSize=9, textColor=GREY, leading=12))
styles.add(ParagraphStyle('PlanPhase', fontName='Helvetica-Bold', fontSize=11, textColor=GOLD))
styles.add(ParagraphStyle('PlanText', fontName='Helvetica', fontSize=9.5, textColor=DARK, leading=12.5))
styles.add(ParagraphStyle('Intro', fontName='Helvetica', fontSize=10.5, textColor=DARK, leading=15, spaceAfter=8))

# ---------------- Parse data.js ----------------
DATA_JS = (BASE / 'data.js').read_text(encoding='utf-8')


def block_between(text, start_marker, end_marker):
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


shoot_types_block = block_between(DATA_JS, 'const SHOOT_TYPES = [', '\n];')
SHOOT_TYPES = re.findall(r"key:\s*'(\w+)',\s*label:\s*'([^']+)'", shoot_types_block)

category_labels_block = block_between(DATA_JS, 'const CATEGORY_LABELS = {', '\n};')
CATEGORY_LABELS = dict(re.findall(r"(\w+):\s*'([^']+)'", category_labels_block))

poses_block = block_between(DATA_JS, 'const POSES = [', '\n];')
POSE_RE = re.compile(
    r"\{\s*id:\s*'([^']+)',\s*shootType:\s*'([^']+)',\s*category:\s*'([^']+)',"
    r"\s*title:\s*'([^']*)',\s*instruction:\s*'([^']*)',\s*tip:\s*'([^']*)'\s*\}"
)
ALL_POSES = [
    {'id': m[0], 'shootType': m[1], 'category': m[2], 'title': m[3], 'instruction': m[4], 'tip': m[5]}
    for m in POSE_RE.findall(poses_block)
]

phase_plans_block = block_between(DATA_JS, 'const PHASE_PLANS = {', '\n};')
PHASE_PLANS = {}
for shoot_key, phases_block in re.findall(r"(\w+):\s*\[(.*?)\n  \],", phase_plans_block, re.S):
    phases = []
    for name, fraction, cats in re.findall(
        r"name:\s*'([^']+)',\s*fraction:\s*([\d.]+),\s*categories:\s*\[([^\]]*)\]",
        phases_block,
    ):
        cat_list = re.findall(r"'([^']+)'", cats)
        phases.append({'name': name, 'fraction': float(fraction), 'categories': cat_list})
    PHASE_PLANS[shoot_key] = phases

DEMO_MINUTES = {'couple': 30, 'family': 20, 'single': 15, 'kommunion': 25}

# ---------------- Rendering helpers ----------------
_thumb_cache = {}


def pose_thumb(pose_id, width=26 * mm, target_px=360):
    path = ILLUSTRATIONS / f'{pose_id}.png'
    if not path.exists():
        return Paragraph('', styles['PoseText'])
    if pose_id not in _thumb_cache:
        img = PILImage.open(path).convert('RGB')
        ratio = target_px / max(img.size)
        new_size = (max(1, int(img.width * ratio)), max(1, int(img.height * ratio)))
        img = img.resize(new_size, PILImage.LANCZOS)
        buf = BytesIO()
        img.save(buf, format='JPEG', quality=82)
        buf.seek(0)
        _thumb_cache[pose_id] = (buf.getvalue(), img.width, img.height)
    data, iw, ih = _thumb_cache[pose_id]
    height = width * ih / iw
    return Image(BytesIO(data), width=width, height=height)


def pose_row(pose):
    text = Paragraph(f"<b>{pose['title']}</b><br/>{pose['instruction']}", styles['PoseText'])
    t = Table([[pose_thumb(pose['id']), text]], colWidths=[28 * mm, 118 * mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


# ---------------- Build story ----------------
story = []

story.append(Spacer(1, 55 * mm))
story.append(Paragraph('Posen-Guide', styles['CoverTitle']))
story.append(Paragraph('Spickzettel für Hochzeits- & Event-Fotografie', styles['CoverSub']))
story.append(Spacer(1, 18 * mm))
story.append(HRFlowable(width='40%', color=GOLD, thickness=1, hAlign='CENTER'))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph(
    'Ablaufpläne, Posen-Ideen und Illustrationen für Brautpaar-, Familien-, Einzel- '
    'und Kommunion-/Konfirmationsshootings. Passend zur Mini-App „Posen-Guide" für unterwegs.',
    ParagraphStyle('CoverNote', parent=styles['CoverSub'], fontSize=10, textColor=GREY)))
story.append(PageBreak())

for shoot_key, shoot_label in SHOOT_TYPES:
    poses_for_type = [p for p in ALL_POSES if p['shootType'] == shoot_key]
    minutes = DEMO_MINUTES.get(shoot_key, 20)
    phases = PHASE_PLANS.get(shoot_key, [])

    story.append(Paragraph(shoot_label, styles['SectionTitle']))
    story.append(Paragraph(
        f"Beispiel-Ablaufplan für ca. {minutes} Minuten. Zeiten sind Richtwerte – flexibel anpassen.",
        styles['Intro']))

    plan_rows = [[Paragraph('Zeit', styles['PlanPhase']), Paragraph('Phase', styles['PlanPhase']), Paragraph('Fokus', styles['PlanPhase'])]]
    elapsed = 0
    for phase in phases:
        start = elapsed
        elapsed += max(1, round(phase['fraction'] * minutes))
        focus = ' / '.join(CATEGORY_LABELS.get(c, c) for c in phase['categories'])
        plan_rows.append([
            Paragraph(f"{start}–{elapsed} Min", styles['PlanText']),
            Paragraph(phase['name'], styles['PlanText']),
            Paragraph(focus, styles['PlanText']),
        ])
    t = Table(plan_rows, colWidths=[28 * mm, 55 * mm, 60 * mm])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d8cdb8')),
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BG),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))
    story.append(PageBreak())

    categories_in_order = list(dict.fromkeys(p['category'] for p in poses_for_type))
    for cat in categories_in_order:
        story.append(Paragraph(CATEGORY_LABELS.get(cat, cat), styles['CatTitle']))
        for pose in [p for p in poses_for_type if p['category'] == cat]:
            story.append(pose_row(pose))
        story.append(Spacer(1, 3 * mm))
    story.append(PageBreak())

doc = SimpleDocTemplate(
    str(BASE / 'Posen-Guide-Spickzettel.pdf'),
    pagesize=A4,
    topMargin=16 * mm, bottomMargin=16 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    title='Posen-Guide Spickzettel',
)
doc.build(story[:-1])
print(f'done — {len(ALL_POSES)} poses across {len(SHOOT_TYPES)} shoot types')
