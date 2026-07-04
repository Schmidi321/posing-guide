# -*- coding: utf-8 -*-
"""Build the Posen-Guide PDF cheat sheet, embedding the generated pose illustrations."""

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
from reportlab.lib.utils import ImageReader

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
styles.add(ParagraphStyle('PoseTitle', fontName='Helvetica-Bold', fontSize=10.5, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle('PoseText', fontName='Helvetica', fontSize=9, textColor=GREY, leading=12))
styles.add(ParagraphStyle('PlanPhase', fontName='Helvetica-Bold', fontSize=11, textColor=GOLD))
styles.add(ParagraphStyle('PlanText', fontName='Helvetica', fontSize=9.5, textColor=DARK, leading=12.5))
styles.add(ParagraphStyle('Intro', fontName='Helvetica', fontSize=10.5, textColor=DARK, leading=15, spaceAfter=8))

CATEGORY_LABELS = {
    'stehend': 'Stehend', 'gehen': 'Gehen & Bewegung', 'naehe': 'Nähe & Emotion',
    'candid': 'Lachen & Candid', 'kreativ': 'Kreativ', 'aufstellung': 'Aufstellung',
    'grossgruppe': 'Großgruppe', 'kinder': 'Kinder', 'sitzend': 'Sitzend',
    'detail': 'Details', 'bewegung': 'Bewegung',
}

# id, title, instruction
POSES = {
 'couple': {
  'stehend': [
   ('c01', 'Klassisch frontal', 'Beide zugewandt, Hände auf Hüfte/Brust des Partners. "Schaut euch tief in die Augen."'),
   ('c02', 'Drei-Viertel-Ansicht', 'Paar leicht seitlich zueinander, vorderer Fuß zur Kamera.'),
   ('c03', 'Stirn an Stirn', 'Stirnen berühren sich, Augen geschlossen, tief durchatmen lassen.'),
   ('c04', 'Rückenlehnen', 'Eine Person lehnt sich an den Rücken der anderen.'),
   ('c05', 'Dip / Tanzhaltung', 'Eine Person lässt die andere leicht nach hinten sinken.'),
  ],
  'gehen': [
   ('c06', 'Hand in Hand gehen', 'Paar geht einen Weg entlang, Hände verschränkt.'),
   ('c07', 'Auf die Kamera zu', 'Beide laufen direkt auf dich zu, am Ende lachen/anhalten lassen.'),
   ('c08', 'Wegdrehen & zurückschauen', 'Ein paar Schritte weggehen, dann gemeinsam umdrehen.'),
   ('c09', 'Drehung / Twirl', 'Eine Person dreht die andere einmal um die eigene Achse.'),
   ('c10', 'Verfolgungsspiel', 'Eine Person läuft lachend voraus, andere folgt.'),
  ],
  'naehe': [
   ('c11', 'Umarmung von hinten', 'Von hinten umarmen, Kinn auf der Schulter.'),
   ('c12', 'Flüstern ins Ohr', 'Etwas ins Ohr flüstern, echtes Lachen provozieren.'),
   ('c13', 'Kuss auf die Stirn', 'Geküsste Person schließt Augen und lächelt.'),
   ('c14', 'Hand am Gesicht', 'Hand sanft an die Wange legen, Blickkontakt.'),
   ('c15', 'Der Kuss', 'Klassischer Kuss, Kopf leicht geneigt.'),
  ],
  'candid': [
   ('c16', 'Privater Witz', 'Nach lustiger Erinnerung fragen, echtes Lachen einfangen.'),
   ('c17', 'Kitzeln / Necken', 'Spielerisch necken, Reaktion einfangen (Serienbild).'),
   ('c18', 'Gemeinsam auf etwas schauen', 'Beide schauen auf Ring/Handy/Landschaft, natürlich reagieren.'),
  ],
  'kreativ': [
   ('c19', 'Silhouette', 'Vor helle Lichtquelle stellen, gegen das Licht belichten.'),
   ('c20', 'Spiegelung', 'Pfütze/Fenster/Spiegel nutzen, Kamera tief halten.'),
   ('c21', 'Weitwinkel mit Umgebung', 'Paar klein im Bild, Location dominiert.'),
   ('c22', 'Requisite', 'Vorhandene Requisite einbauen (Schirm, Rad, Blumen).'),
  ],
 },
 'family': {
  'aufstellung': [
   ('f01', 'Klassische Reihen', 'Große Personen hinten/außen, kleine vorne/mittig.'),
   ('f02', 'Halbkreis um Brautpaar', 'Brautpaar mittig, Familie im Halbkreis, leicht erhöht.'),
   ('f03', 'Kernfamilie', 'Nur Eltern + Brautpaar, eng zusammenstehen.'),
   ('f04', 'Je eine Seite', 'Erst nur Familie Braut, dann nur Familie Bräutigam.'),
  ],
  'grossgruppe': [
   ('f05', 'Alle Gäste', 'Ganze Gesellschaft auf Stufen/Hügel, klar ansagen.'),
   ('f06', 'Von oben fotografiert', 'Gruppe liegt im Kreis, du fotografierst erhöht.'),
   ('f07', 'Wurf-Moment', 'Konfetti/Hüte werfen lassen, Countdown "3-2-1-Wurf!".'),
  ],
  'candid': [
   ('f08', 'Lachen provozieren', '"Winkt eurem schlimmsten Feind zu" – Unsinn sagen.'),
   ('f09', 'Gespräch im Kreis', 'Natürlich reden lassen, unauffällig von der Seite.'),
   ('f10', 'Umarmung spontan', 'Kurze Umarmung, mittendrin auslösen.'),
  ],
  'kinder': [
   ('f11', 'Kinder auf Schultern', 'Huckepack oder auf Schultern tragen.'),
   ('f12', 'Kinder rennen lassen', 'Kurze Strecke zu den Eltern rennen lassen.'),
   ('f13', 'Großeltern mit Enkeln', 'Enkel auf dem Schoß, ruhige Anweisungen.'),
  ],
 },
 'single': {
  'stehend': [
   ('s01', 'Klassisches Portrait', 'Drei-Viertel-Drehung, Gewicht auf hinteres Bein.'),
   ('s02', 'Hand in der Tasche', 'Eine Hand locker in der Tasche, wirkt lässig.'),
   ('s03', 'Blick über die Schulter', 'Rücken zur Kamera, Kopf zurückdrehen.'),
   ('s04', 'An Wand/Baum gelehnt', 'Locker anlehnen, ein Bein angewinkelt.'),
  ],
  'sitzend': [
   ('s05', 'Auf Stufen sitzend', 'Ellenbogen auf Knien, von leicht unten fotografieren.'),
   ('s06', 'Auf Bank/Stuhl', 'Seitlich sitzen, ein Arm über die Lehne.'),
   ('s07', 'Kleid drapiert', 'Vorsichtig hinsetzen, Kleid großzügig drapieren.'),
  ],
  'bewegung': [
   ('s08', 'Gehen auf die Kamera zu', 'Locker laufen, Arme natürlich schwingen lassen.'),
   ('s09', 'Drehung im Kleid', 'Einmal um die eigene Achse drehen, im Schwung auslösen.'),
   ('s10', 'Haar/Schleier im Wind', 'Gegen den Wind fotografieren.'),
  ],
  'detail': [
   ('s11', 'Ringe', 'Nahaufnahme der Hände, weiches Seitenlicht.'),
   ('s12', 'Kleid-Detail', 'Spitze/Knöpfe/Stoffstruktur nahaufnehmen.'),
   ('s13', 'Schuhe', 'Einzeln oder am Fuß in Szene setzen.'),
  ],
 },
}

PLANS = {
 'couple': {'label': 'Brautpaar', 'minutes': 30, 'phases': [
    ('Ankommen & Lockerung', 0, 5, 'Lachen & Candid'),
    ('Klassische Posen', 5, 14, 'Stehend'),
    ('Bewegung', 14, 20, 'Gehen & Bewegung'),
    ('Nähe & Emotion', 20, 28, 'Nähe & Emotion'),
    ('Kreativ / Abschluss', 28, 31, 'Kreativ'),
 ]},
 'family': {'label': 'Familie & Gruppen', 'minutes': 20, 'phases': [
    ('Große Gruppe formal', 0, 6, 'Großgruppe / Aufstellung'),
    ('Kernfamilie', 6, 11, 'Aufstellung'),
    ('Candid & Lachen', 11, 16, 'Lachen & Candid'),
    ('Kinder einbeziehen', 16, 20, 'Kinder'),
 ]},
 'single': {'label': 'Einzelperson', 'minutes': 15, 'phases': [
    ('Stehend', 0, 5, 'Stehend'),
    ('Sitzend / Ruhig', 5, 9, 'Sitzend'),
    ('Bewegung', 9, 13, 'Bewegung'),
    ('Details', 13, 15, 'Details'),
 ]},
}


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


def pose_row(pose_id, title, instr):
    text = Paragraph(f"<b>{title}</b><br/>{instr}", styles['PoseText'])
    t = Table([[pose_thumb(pose_id), text]], colWidths=[28 * mm, 118 * mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


story = []

story.append(Spacer(1, 55 * mm))
story.append(Paragraph('Posen-Guide', styles['CoverTitle']))
story.append(Paragraph('Spickzettel für Hochzeits- & Event-Fotografie', styles['CoverSub']))
story.append(Spacer(1, 18 * mm))
story.append(HRFlowable(width='40%', color=GOLD, thickness=1, hAlign='CENTER'))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph(
    'Ablaufpläne, Posen-Ideen und Illustrationen für Brautpaar-, Familien- und '
    'Einzelshootings. Passend zur Mini-App „Posen-Guide" für unterwegs.',
    ParagraphStyle('CoverNote', parent=styles['CoverSub'], fontSize=10, textColor=GREY)))
story.append(PageBreak())

for key in ['couple', 'family', 'single']:
    plan = PLANS[key]
    story.append(Paragraph(plan['label'], styles['SectionTitle']))
    story.append(Paragraph(
        f"Beispiel-Ablaufplan für ca. {plan['minutes']} Minuten. Zeiten sind Richtwerte – flexibel anpassen.",
        styles['Intro']))

    plan_rows = [[Paragraph('Zeit', styles['PlanPhase']), Paragraph('Phase', styles['PlanPhase']), Paragraph('Fokus', styles['PlanPhase'])]]
    for name, start, end, focus in plan['phases']:
        plan_rows.append([
            Paragraph(f'{start}–{end} Min', styles['PlanText']),
            Paragraph(name, styles['PlanText']),
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

    for cat, poses in POSES[key].items():
        story.append(Paragraph(CATEGORY_LABELS[cat], styles['CatTitle']))
        for pose_id, title, instr in poses:
            story.append(pose_row(pose_id, title, instr))
        story.append(Spacer(1, 3 * mm))
    story.append(PageBreak())

doc = SimpleDocTemplate(
    str(BASE / 'Posen-Guide-Spickzettel.pdf'),
    pagesize=A4,
    topMargin=16 * mm, bottomMargin=16 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    title='Posen-Guide Spickzettel',
)
doc.build(story[:-1])
print('done')
