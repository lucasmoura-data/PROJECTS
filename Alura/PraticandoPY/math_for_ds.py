"""
Artigo Academico — Matematica para Data Science & Machine Learning
Design profissional: fundo cinza escuro, tons pasteis, interativo com bookmarks
"""

import math
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Paragraph, Spacer, PageBreak, Table, TableStyle,
                                 HRFlowable, KeepTogether)
from reportlab.platypus.flowables import AnchorFlowable, Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ═══════════════════════════════════════════════════════════════════════════════
# PALETA DE CORES — Dark Profesional com Pasteis
# ═══════════════════════════════════════════════════════════════════════════════
P = {
    # Fundos
    'bg_page':    colors.HexColor('#1C1C1E'),   # fundo da pagina (cinza quase preto)
    'bg_card':    colors.HexColor('#252528'),   # card / bloco de conteudo
    'bg_card2':   colors.HexColor('#2C2C30'),   # card alternativo
    'bg_code':    colors.HexColor('#1A1A1F'),   # fundo codigo
    'bg_math':    colors.HexColor('#22222A'),   # fundo expressao matematica
    'bg_cover':   colors.HexColor('#141416'),   # capa

    # Pasteis / Texto
    'text_main':  colors.HexColor('#E8E6E0'),   # texto principal
    'text_muted': colors.HexColor('#8A8A8E'),   # texto secundario
    'text_dim':   colors.HexColor('#5A5A5E'),   # texto muito discreto
    'white':      colors.HexColor('#F2F0EC'),   # quase branco

    # Acentos pastel
    'blue':       colors.HexColor('#7EB3D4'),   # azul pastel
    'blue_l':     colors.HexColor('#1E2D38'),   # azul escuro
    'coral':      colors.HexColor('#D4907E'),   # coral pastel
    'coral_l':    colors.HexColor('#301E1A'),   # coral escuro
    'teal':       colors.HexColor('#6EC4A7'),   # teal pastel
    'teal_l':     colors.HexColor('#163028'),   # teal escuro
    'amber':      colors.HexColor('#D4B07E'),   # ambar pastel
    'amber_l':    colors.HexColor('#2E2318'),   # ambar escuro
    'violet':     colors.HexColor('#A99BD4'),   # violeta pastel
    'violet_l':   colors.HexColor('#201C34'),   # violeta escuro
    'green':      colors.HexColor('#8EC47E'),   # verde pastel
    'green_l':    colors.HexColor('#1A2E18'),   # verde escuro
    'rose':       colors.HexColor('#C49EB4'),   # rosa pastel

    # Linhas
    'border':     colors.HexColor('#3A3A3E'),
    'border_l':   colors.HexColor('#4A4A50'),
    'accent':     colors.HexColor('#7EB3D4'),
}

W, H = A4
MARGIN_L = 18 * mm
MARGIN_R = 18 * mm
MARGIN_T = 16 * mm
MARGIN_B = 18 * mm
CW = W - MARGIN_L - MARGIN_R  # content width = 174mm

# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS
# ═══════════════════════════════════════════════════════════════════════════════
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9.5, textColor=P['text_main'],
             leading=15, alignment=TA_LEFT, spaceAfter=0, spaceBefore=0,
             backColor=None)
    d.update(kw)
    return ParagraphStyle(name, **d)

ST = {
    # Capa
    'cov_inst':    S('ci', fontSize=8, textColor=P['text_muted'], alignment=TA_CENTER),
    'cov_title':   S('ct', fontName='Helvetica-Bold', fontSize=22,
                     textColor=P['white'], leading=28, alignment=TA_CENTER),
    'cov_sub':     S('cs', fontSize=11, textColor=P['blue'], alignment=TA_CENTER),
    'cov_meta':    S('cm', fontSize=8,  textColor=P['text_muted'], alignment=TA_CENTER),
    'cov_abs':     S('ca', fontSize=9,  textColor=P['text_main'], leading=14,
                     alignment=TA_JUSTIFY),
    'cov_kw':      S('ck', fontSize=8, textColor=P['text_muted'], alignment=TA_LEFT),

    # Cabecalhos
    'ch_num':      S('hn', fontName='Helvetica-Bold', fontSize=9,
                     textColor=P['blue'], spaceAfter=2),
    'ch_title':    S('ht', fontName='Helvetica-Bold', fontSize=15,
                     textColor=P['white'], leading=20, spaceAfter=6),
    'h2':          S('h2', fontName='Helvetica-Bold', fontSize=11,
                     textColor=P['white'], leading=15, spaceAfter=4, spaceBefore=6),
    'h3':          S('h3', fontName='Helvetica-Bold', fontSize=9.5,
                     textColor=P['blue'], spaceAfter=3, spaceBefore=4),

    # Corpo
    'body':        S('body', fontSize=9, leading=15, alignment=TA_JUSTIFY,
                     textColor=P['text_main'], spaceAfter=5),
    'body_sm':     S('bsm', fontSize=8.5, leading=13, textColor=P['text_main'],
                     alignment=TA_JUSTIFY),
    'caption':     S('cap', fontSize=7.5, textColor=P['text_muted'],
                     alignment=TA_CENTER, spaceAfter=4),
    'nota':        S('nota', fontSize=8, textColor=P['amber'],
                     leading=13, alignment=TA_JUSTIFY),

    # Codigo
    'code':        S('code', fontName='Courier', fontSize=7.5,
                     textColor=colors.HexColor('#C8C8C8'), leading=11.5),
    'code_kw':     S('ckw', fontName='Courier-Bold', fontSize=7.5,
                     textColor=colors.HexColor('#B5A0E8'), leading=11.5),
    'code_lang':   S('cl', fontName='Helvetica-Bold', fontSize=7,
                     textColor=P['text_muted']),

    # Matematica
    'math_expr':   S('me', fontName='Courier-Bold', fontSize=9,
                     textColor=P['violet'], leading=14, alignment=TA_LEFT),
    'math_expl':   S('mx', fontSize=8.5, textColor=P['text_main'], leading=13,
                     alignment=TA_JUSTIFY),

    # Niveis
    'lvl_badge':   S('lb', fontName='Helvetica-Bold', fontSize=8.5, textColor=P['white']),
    'lvl_body':    S('lbd', fontSize=9, leading=15, textColor=P['text_main'],
                     alignment=TA_JUSTIFY),

    # TOC
    'toc_part':    S('tp', fontName='Helvetica-Bold', fontSize=10,
                     textColor=P['white'], leading=16),
    'toc_item':    S('ti', fontSize=9, textColor=P['text_muted'], leading=14),
    'toc_pg':      S('tpg', fontSize=9, textColor=P['blue'], alignment=TA_RIGHT),

    # Glossario
    'glos_term':   S('gt', fontName='Helvetica-Bold', fontSize=9,
                     textColor=P['teal'], leading=14),
    'glos_def':    S('gd', fontSize=8.5, textColor=P['text_main'], leading=13,
                     alignment=TA_JUSTIFY),
    'glos_math':   S('gm', fontName='Courier', fontSize=8,
                     textColor=P['violet'], leading=12),
    'nota_math':   S('nm', fontName='Courier-Bold', fontSize=9,
                     textColor=P['amber'], leading=13),
    'nota_sym':    S('ns', fontName='Helvetica-Bold', fontSize=9,
                     textColor=P['rose'], leading=13),

    # Footer / header
    'hdr':         S('hdr', fontSize=7, textColor=P['text_dim']),
    'ftr':         S('ftr', fontSize=7, textColor=P['text_dim'], alignment=TA_CENTER),
}

# ═══════════════════════════════════════════════════════════════════════════════
# ANCHOR COM LABEL (para bookmarks interativos)
# ═══════════════════════════════════════════════════════════════════════════════
class LabeledAnchor(AnchorFlowable):
    def __init__(self, name, label, level=0):
        super().__init__(name)
        self._label = label
        self._rl_level = level

# ═══════════════════════════════════════════════════════════════════════════════
# FLOWABLE: Fundo de Pagina Escuro
# ═══════════════════════════════════════════════════════════════════════════════
class DarkPageBackground(Flowable):
    """Desenha retangulo de fundo escuro — usado no onPage callback."""
    pass

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def sp(n=6):  return Spacer(1, n)
def para(txt, sty='body'): return Paragraph(txt, ST[sty])

def hr(col=None, thick=0.4, before=4, after=4):
    return HRFlowable(width='100%', thickness=thick,
                      color=col or P['border'], spaceAfter=after, spaceBefore=before)

def section_rule(color):
    return HRFlowable(width='100%', thickness=1.5, color=color, spaceAfter=6, spaceBefore=0)

def colored_bar(text, bg_color, text_color=None, fontsize=13, pad_v=10, pad_h=14):
    tc = text_color or P['white']
    data = [[Paragraph(text, ParagraphStyle('_cb', fontName='Helvetica-Bold',
                        fontSize=fontsize, textColor=tc, leading=fontsize+4))]]
    t = Table(data, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg_color),
        ('TOPPADDING',    (0,0),(-1,-1), pad_v),
        ('BOTTOMPADDING', (0,0),(-1,-1), pad_v),
        ('LEFTPADDING',   (0,0),(-1,-1), pad_h),
        ('RIGHTPADDING',  (0,0),(-1,-1), pad_h),
        ('ROUNDEDCORNERS',(0,0),(-1,-1), [5,5,5,5]),
    ]))
    return t

def card(content_rows, bg=None, left_accent=None, pad=10):
    """Envolve linhas numa tabela estilizada tipo card."""
    bg = bg or P['bg_card']
    data = [[row] for row in content_rows]
    t = Table(data, colWidths=[CW - (2 if left_accent else 0)])
    style = [
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), pad),
        ('BOTTOMPADDING', (0,0),(-1,-1), pad),
        ('LEFTPADDING',   (0,0),(-1,-1), pad),
        ('RIGHTPADDING',  (0,0),(-1,-1), pad),
        ('ROWBACKGROUNDS',(0,0),(-1,-1), [bg]),
    ]
    t.setStyle(TableStyle(style))
    if left_accent:
        wrap = Table([[t]], colWidths=[CW])
        wrap.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), left_accent),
            ('TOPPADDING',    (0,0),(-1,-1), 0),
            ('BOTTOMPADDING', (0,0),(-1,-1), 0),
            ('LEFTPADDING',   (0,0),(-1,-1), 3),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
        ]))
        return wrap
    return t

def math_table(items):
    """items: list of (expr_str, explanation_str)"""
    rows = []
    for expr, expl in items:
        rows.append([
            Paragraph(expr, ST['math_expr']),
            Paragraph(expl, ST['math_expl']),
        ])
    t = Table(rows, colWidths=[CW * 0.40, CW * 0.60])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['bg_math']),
        ('ROWBACKGROUNDS',(0,0),(-1,-1), [P['bg_math'], colors.HexColor('#26262E')]),
        ('LINEAFTER',     (0,0),(0,-1),  1.5, P['violet']),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(0,-1),  10),
        ('LEFTPADDING',   (1,0),(1,-1),  10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('GRID',          (0,0),(-1,-1), 0.3, P['border']),
        ('ROUNDEDCORNERS',(0,0),(-1,-1), [4,4,4,4]),
    ]))
    return t

def code_block(code_text, lang='python'):
    bg = P['bg_code']
    lang_color = colors.HexColor('#B5A0E8') if lang == 'python' else colors.HexColor('#6EC4A7')
    label_row = Table([[
        Paragraph(lang.upper(), ParagraphStyle('_cl', fontName='Helvetica-Bold',
                  fontSize=7, textColor=lang_color)),
        Paragraph('— clique para copiar', ParagraphStyle('_cr', fontSize=6.5,
                  textColor=P['text_dim'], alignment=TA_RIGHT)),
    ]], colWidths=[CW * 0.5, CW * 0.5])
    label_row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#141418')),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ]))
    code_p = Paragraph(
        code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'),
        ST['code'])
    code_data = Table([[code_p]], colWidths=[CW])
    code_data.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ]))
    wrap = Table([[label_row], [code_data]], colWidths=[CW])
    wrap.setStyle(TableStyle([
        ('LINEABOVE',     (0,0),(-1,0),  1.5, P['violet']),
        ('LINEBEFORE',    (0,0),(0,-1),  1.5, P['violet']),
        ('LINEBELOW',     (0,-1),(-1,-1),0.5, P['border']),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 0),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    return [wrap, sp(10)]

def sql_block(sql_text):
    lang_color = P['teal']
    label_row = Table([[
        Paragraph('SQL', ParagraphStyle('_sl', fontName='Helvetica-Bold',
                  fontSize=7, textColor=lang_color)),
        Paragraph('— consulta demonstrativa', ParagraphStyle('_sr', fontSize=6.5,
                  textColor=P['text_dim'], alignment=TA_RIGHT)),
    ]], colWidths=[CW * 0.5, CW * 0.5])
    label_row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#141418')),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ]))
    sql_p = Paragraph(
        sql_text.replace('\n', '<br/>').replace(' ', '&nbsp;'),
        ST['code'])
    sql_data = Table([[sql_p]], colWidths=[CW])
    sql_data.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['bg_code']),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ]))
    wrap = Table([[label_row], [sql_data]], colWidths=[CW])
    wrap.setStyle(TableStyle([
        ('LINEABOVE',     (0,0),(-1,0),  1.5, P['teal']),
        ('LINEBEFORE',    (0,0),(0,-1),  1.5, P['teal']),
        ('LINEBELOW',     (0,-1),(-1,-1),0.5, P['border']),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 0),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    return [wrap, sp(10)]

def level_section(name, accent, bg, body_text, math_items=None, py_code=None, sql_code=None):
    items = []
    badge = Table([[Paragraph(f'  {name.upper()}  ',
                   ParagraphStyle('_b', fontName='Helvetica-Bold', fontSize=8,
                                  textColor=P['bg_page']))]], colWidths=[80])
    badge.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), accent),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('ROUNDEDCORNERS',(0,0),(-1,-1), [3,3,0,0]),
    ]))
    items.append(badge)

    inner = [Paragraph(body_text, ST['lvl_body'])]

    if math_items:
        inner += [sp(8), Paragraph('Expressoes Matematicas', ST['h3']), sp(3),
                  math_table(math_items)]
    if py_code:
        inner += [sp(8), Paragraph('Implementacao em Python', ST['h3']), sp(3)]
        inner += code_block(py_code, 'python')
    if sql_code:
        inner += [sp(4), Paragraph('Consulta SQL Ilustrativa', ST['h3']), sp(3)]
        inner += sql_block(sql_code)

    content_rows = [[i] for i in inner]
    body_t = Table(content_rows, colWidths=[CW - 28])
    body_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    outer = Table([[body_t]], colWidths=[CW])
    outer.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 12),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),
        ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ('LINEBEFORE',    (0,0),(0,-1),  2.5, accent),
        ('LINEBELOW',     (0,-1),(-1,-1),0.4, P['border']),
        ('ROUNDEDCORNERS',(0,0),(-1,-1), [0,0,4,4]),
    ]))
    items.append(outer)
    items.append(sp(12))
    return items

# ═══════════════════════════════════════════════════════════════════════════════
# MAP FLOWABLE
# ═══════════════════════════════════════════════════════════════════════════════
class MathMap(Flowable):
    def __init__(self, w, h):
        Flowable.__init__(self)
        self.width = w
        self.height = h

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        cx, cy = w / 2, h / 2 - 10

        # Background
        c.setFillColor(P['bg_math'])
        c.roundRect(0, 0, w, h, 8, fill=1, stroke=0)

        def rbox(x, y, bw, bh, fill, stroke, title, sub=None, r=6):
            c.setFillColor(fill)
            c.setStrokeColor(stroke)
            c.setLineWidth(0.8)
            c.roundRect(x - bw/2, y - bh/2, bw, bh, r, fill=1, stroke=1)
            c.setFillColor(P['white'])
            if sub:
                c.setFont('Helvetica-Bold', 8)
                c.drawCentredString(x, y + 5, title)
                c.setFont('Helvetica', 6.5)
                c.setFillColor(P['text_muted'])
                c.drawCentredString(x, y - 7, sub)
            else:
                c.setFont('Helvetica-Bold', 9)
                c.drawCentredString(x, y - 3, title)

        def arrow(x1, y1, x2, y2, col):
            c.setStrokeColor(col)
            c.setLineWidth(0.8)
            c.setDash(3, 2)
            c.line(x1, y1, x2, y2)
            c.setDash()
            dx, dy = x2-x1, y2-y1
            ln = math.sqrt(dx*dx+dy*dy)
            if ln == 0: return
            ux, uy = dx/ln, dy/ln; px, py = -uy, ux
            sz = 4.5
            c.setFillColor(col); c.setStrokeColor(col)
            p = c.beginPath()
            p.moveTo(x2, y2)
            p.lineTo(x2 - sz*ux + sz*0.35*px, y2 - sz*uy + sz*0.35*py)
            p.lineTo(x2 - sz*ux - sz*0.35*px, y2 - sz*uy - sz*0.35*py)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        # Centro
        rbox(cx, cy, 90, 40, P['violet_l'], P['violet'], 'Machine', 'Learning', 10)

        nodes = [
            (cx-130, cy+90,  P['blue_l'],  P['blue'],  'Algebra Linear',   'Vetores · Matrizes · PCA'),
            (cx+130, cy+90,  P['coral_l'], P['coral'], 'Calculo',           'Derivadas · Gradiente'),
            (cx-130, cy-90,  P['teal_l'],  P['teal'],  'Estatistica',       'Probabilidade · Bayes'),
            (cx+130, cy-90,  P['amber_l'], P['amber'], 'Otimizacao',        'Gradient Descent · Adam'),
            (cx,     cy-135, P['green_l'], P['green'], 'Teoria da Info.',   'Entropia · Cross-entropy'),
        ]

        for nx, ny, fl, st, lbl, sub in nodes:
            dx, dy = cx-nx, cy-ny
            ln = math.sqrt(dx*dx+dy*dy)
            ux, uy = dx/ln, dy/ln
            arrow(nx + ux*65, ny + uy*22, cx - ux*50, cy - uy*22, st)
            rbox(nx, ny, 122, 36, fl, st, lbl, sub, 5)

        # Titulo do mapa
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(P['text_muted'])
        c.drawCentredString(cx, h - 12,
            'Figura 1 — Os Cinco Pilares Matematicos do Machine Learning')
        c.setFont('Helvetica', 7)
        c.setFillColor(P['text_dim'])
        c.drawCentredString(cx, 8, 'Setas indicam como cada pilar fundamenta o aprendizado de maquina')

# ═══════════════════════════════════════════════════════════════════════════════
# DOC CLASS COM BOOKMARKS E OUTLINES
# ═══════════════════════════════════════════════════════════════════════════════
class AcademicDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, LabeledAnchor):
            self.canv.addOutlineEntry(
                flowable._label, flowable._name,
                level=flowable._rl_level, closed=(flowable._rl_level > 0))

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CALLBACKS
# ═══════════════════════════════════════════════════════════════════════════════
_section_info = {'current': 'Matematica para Data Science & ML'}

def draw_page_background(c, w, h):
    c.setFillColor(P['bg_page'])
    c.rect(0, 0, w, h, fill=1, stroke=0)

def on_cover(c, doc):
    draw_page_background(c, W, H)
    # Gradient visual stripe left
    c.setFillColor(P['violet_l'])
    c.rect(0, 0, 4, H, fill=1, stroke=0)

def on_page(c, doc):
    draw_page_background(c, W, H)
    # Top bar
    c.setFillColor(P['bg_card'])
    c.rect(0, H - MARGIN_T, W, MARGIN_T, fill=1, stroke=0)
    c.setStrokeColor(P['border'])
    c.setLineWidth(0.4)
    c.line(MARGIN_L, H - MARGIN_T, W - MARGIN_R, H - MARGIN_T)
    # Header text
    c.setFont('Helvetica', 7)
    c.setFillColor(P['text_dim'])
    c.drawString(MARGIN_L, H - MARGIN_T + 4.5,
                 'Matematica para Data Science & Machine Learning — Guia Progressivo')
    c.drawRightString(W - MARGIN_R, H - MARGIN_T + 4.5,
                      f'Pagina {doc.page}')
    # Left stripe
    c.setFillColor(P['violet_l'])
    c.rect(0, 0, 3, H, fill=1, stroke=0)
    # Bottom bar
    c.setFillColor(P['bg_card'])
    c.rect(0, 0, W, MARGIN_B - 4, fill=1, stroke=0)
    c.setStrokeColor(P['border'])
    c.line(MARGIN_L, MARGIN_B - 4, W - MARGIN_R, MARGIN_B - 4)
    c.setFont('Helvetica', 7)
    c.setFillColor(P['text_dim'])
    c.drawCentredString(W/2, 6,
        'Departamento de Ciencia da Computacao — Guia de Fundamentacao Matematica')

# ═══════════════════════════════════════════════════════════════════════════════
# CONTEUDO — GLOSSARIO DE NOTACOES
# ═══════════════════════════════════════════════════════════════════════════════
NOTATION_GLOSSARY = [
    # (simbolo, nome, descricao, exemplo)
    ('SUM / SIGMA',  'Somatorio',
     'Soma de termos de uma sequencia. SUM_{i=1}^{n} x_i soma todos os x de i=1 ate n.',
     'SUM_{i=1}^{3} i = 1 + 2 + 3 = 6'),
    ('PROD',         'Produtorio',
     'Produto de termos. PROD_{i=1}^{n} x_i multiplica todos os x de i=1 ate n.',
     'PROD_{i=1}^{3} i = 1 * 2 * 3 = 6'),
    ('INT',          'Integral',
     'Soma continua (area sob a curva). INT_{a}^{b} f(x)dx = area de f entre a e b.',
     'INT_{0}^{1} x dx = 0.5'),
    ('grad / nabla', 'Gradiente',
     'Vetor de derivadas parciais. Aponta na direcao de maior crescimento da funcao.',
     'grad f = [df/dx, df/dy, df/dz]'),
    ('d/dx ou f\'(x)','Derivada',
     'Taxa de variacao instantanea de f em relacao a x. Inclinacao da tangente.',
     'd/dx(x^2) = 2x'),
    ('E[X]',         'Esperanca',
     'Media esperada de X. Para discreto: SUM x*P(X=x). Para continuo: INT x*p(x)dx.',
     'E[dado] = (1+2+3+4+5+6)/6 = 3.5'),
    ('P(A|B)',        'Probabilidade Condicional',
     'Probabilidade de A dado que B ocorreu. P(A|B) = P(A,B)/P(B).',
     'P(chuva|nuvem) = P(chuva,nuvem)/P(nuvem)'),
    ('argmax_x f(x)','Argmax',
     'O valor de x que maximiza f(x). Diferente de max (que retorna o valor de f).',
     'argmax_{x in {1,2,3}} x^2 = 3'),
    ('||v||',        'Norma (L2)',
     'Comprimento (magnitude) de um vetor. ||v|| = sqrt(v1^2 + ... + vn^2).',
     '||[3,4]|| = sqrt(9+16) = 5'),
    ('v^T',          'Transposta',
     'Para vetor: converte coluna em linha (e vice-versa). Para matriz: troca linhas por colunas.',
     '[1,2,3]^T = vetor coluna com 3 linhas'),
    ('A^{-1}',       'Matriz Inversa',
     'Matriz tal que A * A^{-1} = I (identidade). Existe so para matrizes quadradas e nao singulares.',
     'Se A = [[2,0],[0,3]], entao A^{-1} = [[0.5,0],[0,0.33]]'),
    ('A^T * A',      'Gram Matrix',
     'Produto de A transposta por A. Resulta em matriz simetrica positiva semi-definida.',
     'Usada para calcular covariancia: Cov = X^T * X / n'),
    ('O(n)',         'Notacao Big-O',
     'Complexidade computacional no pior caso. O(n^2) significa que o custo cresce com n^2.',
     'Multiplicacao de matrizes n x n: O(n^3)'),
    ('~  / distrib', 'Distribuicao',
     'X ~ N(mu, sigma^2) significa: X segue distribuicao Normal com media mu e variancia sigma^2.',
     'w ~ N(0, I) inicializa pesos com ruido gaussiano padrao'),
    ('log',          'Logaritmo Natural (ln)',
     'Em ML, "log" quase sempre significa logaritmo natural (base e ≈ 2.718).',
     'log(1) = 0;  log(e) = 1;  log(0.01) = -4.6'),
    ('epsilon (eps)','Epsilon',
     'Valor muito pequeno adicionado para evitar divisao por zero ou log(0).',
     'log(q + 1e-8) evita log(0) = -inf'),
    ('lambda',       'Lambda — Hiperparametro de Regularizacao',
     'Controla a intensidade da regularizacao. Lambda alto = mais penalizacao nos pesos.',
     'L_ridge = MSE + lambda * SUM(w^2)'),
    ('theta',        'Theta — Parametros do Modelo',
     'Vetor de todos os parametros (pesos) do modelo. theta = {W1, b1, W2, b2, ...}.',
     'theta_MAP = argmax P(dados|theta) * P(theta)'),
    ('KL(p||q)',     'KL Divergence',
     'Medida de quanto q difere de p. KL >= 0 sempre. KL = 0 somente se p = q.',
     'KL(p||q) = SUM p(x) * log(p(x)/q(x))'),
    ('N(mu, sigma)', 'Distribuicao Normal (Gaussiana)',
     'Distribuicao em formato de sino. mu = media (centro), sigma = desvio padrao (largura).',
     'N(0, 1) = gaussiana padrao usada em inicializacao de pesos'),
]

WORD_GLOSSARY = [
    ('Backpropagation',
     'Algoritmo que calcula gradientes em redes neurais aplicando a regra da cadeia '
     'de tras para frente. Permite atualizar os pesos de todas as camadas eficientemente.',
     'grad_W1 = dL/dz1 = dL/da2 * da2/dz2 * dz2/da1 * da1/dz1'),

    ('Gradiente Descendente',
     'Algoritmo iterativo de otimizacao que move os parametros na direcao oposta ao '
     'gradiente para minimizar a funcao de perda. Equivale a "descer a montanha" da superficie de erro.',
     'w = w - lr * dL/dw'),

    ('Overfitting',
     'O modelo "decora" os dados de treinamento mas falha em generalizar para dados novos. '
     'Sintoma: loss de treino cai mas loss de validacao estagna ou sobe.',
     'Bias^2 + Variancia + Ruido = Erro total'),

    ('Embedding',
     'Representacao densa de dados discretos (palavras, usuarios, produtos) como vetores '
     'em espaco continuo de baixa dimensionalidade. Captura relacoes semanticas.',
     'rei - homem + mulher ≈ rainha (aritmetica de vetores)'),

    ('Hiperparametro',
     'Parametros do processo de treinamento que nao sao aprendidos pelos dados, '
     'mas definidos pelo usuario. Exemplos: learning rate, numero de camadas, batch size.',
     'theta_treino vs eta (lr), lambda (reg), T (epocas)'),

    ('Epoch / Epoca',
     'Uma passagem completa por todo o dataset de treinamento. '
     'Em cada epoca, o modelo ve todos os exemplos uma vez.',
     '10.000 amostras, batch=100: 100 passos = 1 epoca'),

    ('Mini-batch',
     'Subconjunto do dataset usado para calcular o gradiente em cada passo. '
     'Balanceia precisao (batch completo) e velocidade (amostra unica).',
     'Batch de 32: calcula gradiente em 32 amostras, atualiza pesos, repete'),

    ('Regularizacao',
     'Tecnica para reduzir overfitting adicionando penalidade aos pesos grandes. '
     'L1 gera esparsidade; L2 distribui pesos uniformemente.',
     'L_total = L_dados + lambda * L_regularizacao'),

    ('Feature / Atributo',
     'Variavel de entrada do modelo. Uma coluna do dataset. '
     'Pode ser numerica, categorica, ou representada como embedding.',
     'Dataset de clientes: idade, renda, score = 3 features'),

    ('Tensor',
     'Generalizacao de vetores (1D) e matrizes (2D) para N dimensoes. '
     'Um video e um tensor 4D: (frames, altura, largura, canais_de_cor).',
     'Imagem RGB: tensor (altura x largura x 3)'),

    ('Loss Function / Funcao de Perda',
     'Funcao que quantifica o erro do modelo. O objetivo do treinamento '
     'e minimiza-la. Escolha depende da tarefa: MSE para regressao, CE para classificacao.',
     'L(y, y_pred) mede distancia entre predicao e verdade'),

    ('Softmax',
     'Funcao que converte um vetor de scores (logits) em probabilidades que somam 1. '
     'Usada na ultima camada de classificadores multiclasse.',
     'softmax([2, 1, 0.1]) = [0.66, 0.24, 0.10]'),

    ('Gradiente Vanishing',
     'Fenomeno onde gradientes ficam muito proximos de zero em camadas iniciais '
     'de redes profundas, impossibilitando o aprendizado. Causa: funcoes de ativacao '
     'com derivadas menores que 1 compostas muitas vezes.',
     'sigmoid\'(x) <= 0.25; apos 10 camadas: 0.25^10 ≈ 0.000001'),

    ('Batch Normalization',
     'Tecnica que normaliza as ativacoes de cada camada para ter media 0 e desvio 1, '
     'depois reescala com parametros treinaveis. Acelera treinamento e permite lr maiores.',
     'z_norm = (z - mean(z)) / std(z); saida = gamma * z_norm + beta'),

    ('Atencao / Attention',
     'Mecanismo que permite ao modelo focar em partes relevantes da entrada. '
     'Base dos Transformers. Calcula similaridade entre cada posicao e todas as outras.',
     'Attention(Q,K,V) = softmax(QK^T/sqrt(d)) V'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CONTEUDO DOS CAPITULOS (mantido compacto — igual ao artigo anterior)
# ═══════════════════════════════════════════════════════════════════════════════
TOPICS = [
  {
    'key': 'cap_al', 'num': '1', 'title': 'Algebra Linear',
    'accent': P['blue'], 'bg': P['blue_l'],
    'intro': (
        'Algebra linear e a linguagem fundamental dos dados em machine learning. '
        'Todo dataset e uma matriz, toda predicao e um produto matricial, toda rede '
        'neural e uma sequencia de transformacoes lineares. Este capitulo apresenta os '
        'conceitos essenciais e como eles se traduzem em codigo e em consultas de dados.'
    ),
    'levels': [
      {
        'name': 'Junior', 'accent': P['green'], 'bg': P['green_l'],
        'body': (
            'O profissional de nivel inicial deve compreender que vetores sao representacoes '
            'numericas de objetos e que matrizes organizam conjuntos de vetores. Sabe operar '
            'com numpy, interpretar shapes de tensores e calcular produto escalar como medida '
            'de similaridade.'
        ),
        'math': [
            ('v = [x1, x2, ..., xn]',
             'Vetor: lista ordenada de n numeros reais. Representa um ponto no espaco n-dimensional. '
             'Ex: perfil de cliente com n atributos (idade, renda, score).'),
            ('v . u = x1*u1 + ... + xn*un',
             'Produto escalar: soma dos produtos elemento a elemento. '
             'Resultado alto indica que os vetores apontam na mesma direcao (alta similaridade).'),
            ('||v|| = sqrt(x1^2 + ... + xn^2)',
             'Norma L2: comprimento geometrico do vetor. '
             'Usada para normalizar vetores e calcular distancias euclidianas.'),
            ('A(m x n) * B(n x p) = C(m x p)',
             'Multiplicacao matricial: A com m linhas e n colunas vezes B com n linhas '
             'e p colunas produz C com m linhas e p colunas. Dimensoes internas (n) devem coincidir.'),
        ],
        'py': '''import numpy as np

# Perfil de clientes: [idade_norm, renda_norm, score_norm]
cliente_A = np.array([0.28, 0.52, 0.75])
cliente_B = np.array([0.35, 0.80, 0.68])

# Produto escalar: mede similaridade direcional
sim_escalar = np.dot(cliente_A, cliente_B)
print(f"Produto escalar A.B = {sim_escalar:.4f}")

# Norma L2: magnitude do perfil
norma_A = np.linalg.norm(cliente_A)  # sqrt(0.28^2 + 0.52^2 + 0.75^2)
norma_B = np.linalg.norm(cliente_B)

# Similaridade cosseno: independe da magnitude
cos_sim = sim_escalar / (norma_A * norma_B)
print(f"Similaridade cosseno = {cos_sim:.4f}  (1=identicos, 0=ortogonais)")

# Dataset como matriz: 4 clientes, 3 features
X = np.array([[0.28, 0.52, 0.75],
              [0.35, 0.80, 0.68],
              [0.22, 0.31, 0.82],
              [0.45, 0.95, 0.60]])
print(f"Shape do dataset: {X.shape}")  # (4 amostras, 3 features)

# Multiplicacao matricial: camada linear simples
# W: 2 neuronios de saida, 3 features de entrada
W = np.array([[0.5, -0.2, 0.8],
              [0.1,  0.9, -0.3]])
b = np.array([[0.1], [0.2]])
Y = W @ X.T + b  # (2, 4): 2 saidas para 4 clientes
print(f"Saida da camada (Y shape): {Y.shape}")''',
        'sql': '''-- Produto escalar e similaridade de cosseno em SQL
WITH features AS (
    SELECT
        'A' AS cliente, 0.28 AS f1, 0.52 AS f2, 0.75 AS f3 UNION ALL
    SELECT 'B',          0.35,       0.80,       0.68
),
calculo AS (
    SELECT
        a.cliente AS c_a, b.cliente AS c_b,
        -- Produto escalar: soma dos produtos elemento a elemento
        a.f1*b.f1 + a.f2*b.f2 + a.f3*b.f3          AS produto_escalar,
        -- Normas L2 de cada vetor
        SQRT(POWER(a.f1,2)+POWER(a.f2,2)+POWER(a.f3,2)) AS norma_a,
        SQRT(POWER(b.f1,2)+POWER(b.f2,2)+POWER(b.f3,2)) AS norma_b
    FROM features a, features b
    WHERE a.cliente < b.cliente
)
SELECT
    c_a, c_b,
    ROUND(produto_escalar, 4)                        AS produto_escalar,
    ROUND(produto_escalar / (norma_a * norma_b), 4) AS similaridade_cosseno
FROM calculo;''',
      },
      {
        'name': 'Pleno', 'accent': P['blue'], 'bg': P['blue_l'],
        'body': (
            'O profissional pleno domina a multiplicacao matricial como operacao central '
            'de redes neurais. Aplica PCA do zero (covariancia, autovetores) e entende SVD '
            'para sistemas de recomendacao. Consegue derivar shapes de tensores em arquiteturas '
            'mais complexas e debugar erros de dimensao.'
        ),
        'math': [
            ('Y = W * X + b',
             'Camada densa: W(d_out x d_in) multiplica X(d_in x N). Cada neuronio computa '
             'uma combinacao linear das entradas, mais bias b(d_out x 1).'),
            ('Cov = (1/n) X^T * X',
             'Matriz de covariancia: elemento (i,j) mede como features i e j variam juntas. '
             'Diagonal = variancia de cada feature. Simetrica por definicao.'),
            ('X = U * S * V^T  (SVD)',
             'Decomposicao em Valores Singulares: U = direcoes dos dados (usuarios), '
             'S = importancia de cada direcao (diagonal), V^T = direcoes de features (itens). '
             'Base de sistemas de recomendacao por fatoracao de matrizes.'),
        ],
        'py': '''import numpy as np
from sklearn.decomposition import PCA

X = np.array([[28,5.2,750,12],[35,8.0,680,45],
              [22,3.1,820, 5],[45,12., 600,80],
              [31,6.5,710,20]], dtype=float)

# PCA manual: centralizar -> covariancia -> autovetores
X_c = X - X.mean(axis=0)
cov = (X_c.T @ X_c) / len(X)
vals, vecs = np.linalg.eigh(cov)
idx = np.argsort(vals)[::-1]   # ordena: maior autovalor primeiro
X_pca = X_c @ vecs[:, idx[:2]] # projeta nas 2 primeiras componentes
print(f"Shape reduzido: {X_pca.shape}")

# Variancia explicada por componente
var_exp = vals[idx] / vals.sum()
print(f"Variancia explicada: {var_exp[:2].round(3)}")

# SVD para recomendacao
ratings = np.array([[5,3,0,1],[4,0,4,1],[1,1,0,5],[0,0,5,4]])
U, S, Vt = np.linalg.svd(ratings, full_matrices=False)
# Reconstrucao com top-2 componentes (filtragem de ruido)
k = 2
reconstruido = U[:,:k] @ np.diag(S[:k]) @ Vt[:k,:]
print(f"Rating[0,2] original: {ratings[0,2]} -> estimado: {reconstruido[0,2]:.2f}")''',
        'sql': '''-- Matriz de covariancia em SQL (conceitual)
WITH stats AS (
    SELECT AVG(renda) m_r, AVG(score) m_s,
           STDDEV(renda) sd_r, STDDEV(score) sd_s
    FROM clientes
),
norm AS (
    SELECT (renda - m_r)/NULLIF(sd_r,0) AS z_r,
           (score - m_s)/NULLIF(sd_s,0) AS z_s
    FROM clientes, stats
)
SELECT
    AVG(z_r * z_r)  AS var_renda,   -- diagonal: variancia
    AVG(z_s * z_s)  AS var_score,
    AVG(z_r * z_s)  AS cov_r_s      -- fora da diagonal: covariancia
FROM norm;''',
      },
      {
        'name': 'Senior', 'accent': P['amber'], 'bg': P['amber_l'],
        'body': (
            'O profissional senior compreende propriedades profundas: rank, numero de '
            'condicao, estabilidade numerica. Implementa self-attention como multiplicacao '
            'matricial QK^T/sqrt(d_k). Analisa o espectro singular de pesos para '
            'diagnosticar colapso de representacao e instabilidade de treinamento.'
        ),
        'math': [
            ('Attention(Q,K,V) = softmax(Q*K^T / sqrt(d_k)) * V',
             'Self-attention: Q,K,V sao projecoes lineares da entrada. '
             'Q*K^T calcula similaridade entre todas as posicoes. '
             'sqrt(d_k) evita saturacao do softmax para dimensoes grandes.'),
            ('kappa(A) = sigma_max / sigma_min',
             'Numero de condicao: razao entre maior e menor valor singular. '
             'kappa >> 1 implica instabilidade numerica e gradientes explosivos.'),
        ],
        'py': '''import numpy as np

def self_attention(X, d_model=4, d_k=2):
    np.random.seed(0)
    W_Q = np.random.randn(d_model, d_k) * 0.1
    W_K = np.random.randn(d_model, d_k) * 0.1
    W_V = np.random.randn(d_model, d_k) * 0.1
    Q = X @ W_Q; K = X @ W_K; V = X @ W_V
    # Scores escalados para evitar gradientes minusculos
    scores = Q @ K.T / np.sqrt(d_k)
    # Softmax estavel numericamente
    scores -= scores.max(axis=1, keepdims=True)
    w = np.exp(scores)
    w /= w.sum(axis=1, keepdims=True)
    return w @ V, w

X = np.random.randn(3, 4)  # 3 tokens, embedding dim 4
out, attn = self_attention(X)
print(f"Pesos atencao token 0: {attn[0].round(3)}")
print(f"Soma (deve ser 1.0):   {attn[0].sum():.4f}")

# Analise espectral de matriz de pesos
W = np.random.randn(64, 64)
_, S, _ = np.linalg.svd(W)
print(f"Numero de condicao: {S[0]/S[-1]:.1f}")
print(f"Top-5 singulares:   {S[:5].round(2)}")''',
        'sql': None,
      },
      {
        'name': 'Especialista', 'accent': P['violet'], 'bg': P['violet_l'],
        'body': (
            'O especialista aplica LoRA (Low-Rank Adaptation) para fine-tuning eficiente '
            'de LLMs com base matematica solida: updates de peso tem rank intrinscamente baixo. '
            'Trabalha com decomposicoes tensoriais (Tucker, CP) e com geometria diferencial '
            'em variedades de parametros para otimizacao por gradiente natural.'
        ),
        'math': [
            ('W_novo = W_0 + B * A,  B(d x r), A(r x d),  r << d',
             'LoRA: W_0 congelado (pre-treinado), B e A sao treinaveis. '
             'Custo: O(r*(d+d)) em vez de O(d^2). Para d=768, r=8: reducao de 99%.'),
            ('F(theta) = E[ grad_log_p * grad_log_p^T ]',
             'Matriz de Fisher: curvatura da log-verossimilhanca. '
             'Gradiente natural: delta_nat = F^{-1} * grad_L. '
             'Invariante a reparametrizacao — otimiza na geometria da distribuicao.'),
        ],
        'py': '''import torch, torch.nn as nn

class LoRALinear(nn.Module):
    """Camada Linear com Low-Rank Adaptation (LoRA)."""
    def __init__(self, d_in, d_out, rank=8, alpha=16):
        super().__init__()
        self.scale = alpha / rank
        self.W0 = nn.Linear(d_in, d_out, bias=False)
        self.W0.weight.requires_grad = False  # CONGELADO
        self.A = nn.Parameter(torch.randn(rank, d_in) * 0.01)
        self.B = nn.Parameter(torch.zeros(d_out, rank))

    def forward(self, x):
        # saida original + delta de baixo posto escalonado
        return self.W0(x) + self.scale * (x @ self.A.T @ self.B.T)

d = 768; r = 8
lora = LoRALinear(d, d, rank=r)
total = d * d
lora_p = r * d + d * r
print(f"Full fine-tune: {total:,} params")
print(f"LoRA (r={r}):    {lora_p:,} params ({100*lora_p/total:.1f}%)")''',
        'sql': None,
      },
    ],
  },
  # ── CALCULO ──────────────────────────────────────────────────────────────────
  {
    'key': 'cap_calc', 'num': '2', 'title': 'Calculo Diferencial e Integral',
    'accent': P['coral'], 'bg': P['coral_l'],
    'intro': (
        'O calculo diferencial e o motor do aprendizado em ML. Derivadas quantificam '
        'como a funcao de perda responde a pequenas perturbacoes nos pesos. '
        'O gradiente generaliza esse conceito para espacos de alta dimensao. '
        'Backpropagation e a aplicacao sistematica da regra da cadeia nesse contexto.'
    ),
    'levels': [
      {
        'name': 'Junior', 'accent': P['green'], 'bg': P['green_l'],
        'body': (
            'Compreende a derivada como taxa de variacao instantanea e entende o '
            'algoritmo de gradient descent como descida na superficie de perda. '
            'Sabe interpretar o loop de treinamento e usar .backward() sem derivar '
            'o backpropagation manualmente.'
        ),
        'math': [
            ("f'(x) = lim_{h->0} [f(x+h) - f(x)] / h",
             'Definicao de derivada: quanto f(x) muda quando x varia um infinitesimo h. '
             'Geometricamente: inclinacao da reta tangente em x.'),
            ('w = w - lr * dL/dw',
             'Gradient Descent: move w na direcao de maior queda de L. '
             'lr (learning rate) controla o tamanho do passo. '
             'lr muito alto: diverge. lr muito baixo: convergencia lenta.'),
            ('L_MSE = (1/n) SUM (y_pred - y_real)^2',
             'Mean Squared Error: media dos erros ao quadrado. '
             'Derivada em relacao a y_pred: 2*(y_pred - y_real)/n. '
             'Penaliza erros grandes desproporcionalmente.'),
        ],
        'py': '''import numpy as np

# Gradient Descent manual para y = w*x + b
X = np.array([1., 2., 3., 4., 5.])
y = np.array([2., 4., 5., 4., 5.])
w, b, lr, n = 0.0, 0.0, 0.01, len(X)

print(f"{'Ep':>4} | {'MSE':>8} | {'w':>7} | {'b':>7}")
for ep in range(100):
    y_hat = w * X + b
    loss  = np.mean((y_hat - y)**2)
    # Derivadas parciais de MSE em relacao a w e b
    dw = (2/n) * np.sum((y_hat - y) * X)  # dL/dw
    db = (2/n) * np.sum(y_hat - y)         # dL/db
    w -= lr * dw;  b -= lr * db
    if ep % 25 == 0:
        print(f"{ep:>4} | {loss:>8.4f} | {w:>7.4f} | {b:>7.4f}")
print(f"Modelo: y = {w:.3f}*x + {b:.3f}")''',
        'sql': '''-- Predicoes de regressao linear e residuos em SQL
WITH pesos AS (SELECT 0.70 AS w, 2.10 AS b),  -- aprendidos por GD
dados  AS (
    SELECT 1 AS x, 2 AS y UNION ALL SELECT 2,4 UNION ALL
    SELECT 3,5 UNION ALL SELECT 4,4 UNION ALL SELECT 5,5
),
pred AS (
    SELECT x, y,
           p.w * x + p.b                  AS y_pred,
           y - (p.w * x + p.b)            AS residuo
    FROM dados, pesos p
)
SELECT x, y, ROUND(y_pred,2) y_pred,
       ROUND(residuo,3)       residuo,
       ROUND(POWER(residuo,2),4) erro_quadrado
FROM pred
UNION ALL
SELECT NULL,NULL,NULL,NULL,
       ROUND(AVG(POWER(residuo,2)),4)  -- MSE
FROM pred;''',
      },
      {
        'name': 'Pleno', 'accent': P['blue'], 'bg': P['blue_l'],
        'body': (
            'Domina a regra da cadeia e implementa backpropagation manualmente para '
            'redes rasas. Compreende por que gradientes desaparecem em redes profundas '
            'com sigmoid e como ReLU mitiga esse problema. Implementa loops de '
            'treinamento com diferentes otimizadores.'
        ),
        'math': [
            ('dL/dW1 = dL/dz2 * dz2/da1 * da1/dz1 * dz1/dW1',
             'Regra da cadeia (backprop em 2 camadas): cada fator e a derivada parcial '
             'de uma variavel em relacao a seguinte. Gradiente "flui" de tras para frente.'),
            ("sigmoid'(x) = s(x)*(1-s(x)) <= 0.25",
             'Derivada da sigmoid: maxima em x=0, valor 0.25. '
             'Para |x|>2, aproxima-se de zero — causa vanishing gradient em redes profundas.'),
            ("ReLU'(x) = 1 (x>0), 0 (x<=0)",
             'Derivada da ReLU: preserva gradiente para ativacoes positivas. '
             'Resolve vanishing gradient, mas cria "neuronios mortos" (x<0 para sempre).'),
        ],
        'py': '''import numpy as np

def sigmoid(x):   return 1/(1+np.exp(-x))
def sig_d(x):     return sigmoid(x)*(1-sigmoid(x))

# XOR: demonstra backpropagation completo
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])
np.random.seed(42)
W1=np.random.randn(2,4)*0.5; b1=np.zeros((1,4))
W2=np.random.randn(4,1)*0.5; b2=np.zeros((1,1))

for ep in range(2000):
    # FORWARD
    z1=X@W1+b1; a1=sigmoid(z1)
    z2=a1@W2+b2; a2=sigmoid(z2)
    loss=-np.mean(y*np.log(a2+1e-8)+(1-y)*np.log(1-a2+1e-8))
    # BACKWARD (regra da cadeia)
    dL_dz2=(-(y/(a2+1e-8)-(1-y)/(1-a2+1e-8)))*sig_d(z2)/4
    dL_dz1=(dL_dz2@W2.T)*sig_d(z1)
    W2-=0.1*a1.T@dL_dz2; b2-=0.1*dL_dz2.sum(0,keepdims=True)
    W1-=0.1*X.T@dL_dz1;  b1-=0.1*dL_dz1.sum(0,keepdims=True)
    if ep%500==0: print(f"Ep {ep:4d}: loss={loss:.4f}")

pred=(sigmoid(sigmoid(X@W1+b1)@W2+b2)>0.5).astype(int)
print(f"XOR: {pred.T[0]}  (esperado: [0 1 1 0])")''',
        'sql': None,
      },
      {
        'name': 'Senior', 'accent': P['amber'], 'bg': P['amber_l'],
        'body': (
            'Domina calculo vetorial completo: Jacobianas para funcoes vetoriais e '
            'Hessianas para curvatura. Implementa gradient clipping com fundamentacao '
            'teorica, usa mixed precision training e analisa estabilidade de treinamento '
            'monitorando a norma do gradiente.'
        ),
        'math': [
            ('J_f(x)_{ij} = df_i / dx_j',
             'Jacobiana: matriz (m x n) das derivadas parciais de cada componente de '
             'saida em relacao a cada componente de entrada. Generalizacao da derivada '
             'para funcoes vetoriais. Essencial para camadas como BatchNorm e Attention.'),
            ('||g|| > C => g = g * (C / ||g||)',
             'Gradient Clipping: re-escala o vetor de gradientes preservando a direcao '
             'quando sua norma excede o limite C. Crucial para Transformers e RNNs.'),
        ],
        'py': '''import torch
import torch.nn as nn

# Jacobiana com autograd
x = torch.tensor([1.,2.,3.], requires_grad=True)
def f(x): return torch.stack([x[0]**2+x[1], x[1]*x[2], x[0]+x[2]**2])
J = torch.autograd.functional.jacobian(f, x)
print(f"Jacobiana:\\n{J.numpy().round(2)}")

# Gradient Clipping + monitoramento de norma
model  = nn.Sequential(nn.Linear(10,64), nn.ReLU(), nn.Linear(64,1))
opt    = torch.optim.Adam(model.parameters(), lr=1e-3)
X_t, y_t = torch.randn(32,10), torch.randn(32,1)

opt.zero_grad()
nn.MSELoss()(model(X_t), y_t).backward()

norma_antes = sum(p.grad.norm()**2 for p in model.parameters()
                  if p.grad is not None) ** 0.5
nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
norma_depois = sum(p.grad.norm()**2 for p in model.parameters()
                   if p.grad is not None) ** 0.5

print(f"Norma antes clipping:  {norma_antes.item():.4f}")
print(f"Norma depois clipping: {norma_depois.item():.4f}")''',
        'sql': None,
      },
      {
        'name': 'Especialista', 'accent': P['violet'], 'bg': P['violet_l'],
        'body': (
            'Trabalha com equacoes diferenciais estocasticas (SDEs) para modelar '
            'treinamento com SGD. Modelos de difusao (DDPM, Score Matching) usam SDEs '
            'explicitamente: adicionar ruido e uma SDE, denoising aprende o score function '
            '(gradiente do log da densidade).'
        ),
        'math': [
            ('dx = f(x,t)dt + g(t)dW_t',
             'SDE de Ito: f(x,t) e o drift (tendencia deterministica), '
             'g(t) e a difusao (intensidade do ruido), dW_t e incremento Browniano. '
             'O treinamento com SGD pode ser modelado como esta equacao.'),
            ('s_theta(x,t) = grad_x log p_t(x)',
             'Score function: gradiente do log da densidade em x. '
             'Modelos de difusao treinam rede para estimar este score em cada nivel de ruido t. '
             'Equivalente a prever o ruido adicionado (formulacao DDPM).'),
        ],
        'py': '''import numpy as np, torch, torch.nn as nn

class SimpleDiffusion:
    """DDPM simplificado — ilustra a matematica de difusao."""
    def __init__(self, T=100):
        self.T = T
        betas = torch.linspace(1e-4, 0.02, T)
        self.alpha_bars = torch.cumprod(1 - betas, dim=0)

    def forward_process(self, x0, t):
        # x_t = sqrt(alpha_bar_t)*x0 + sqrt(1-alpha_bar_t)*eps
        # Forma fechada: em um passo vai de x0 ate x_t qualquer t
        ab = self.alpha_bars[t]
        eps = torch.randn_like(x0)
        return torch.sqrt(ab)*x0 + torch.sqrt(1-ab)*eps, eps

diff = SimpleDiffusion(T=100)
x0   = torch.tensor([[1.0, 2.0, 3.0]])
print("Niveis de ruido (x0 = [1, 2, 3]):")
for t in [0, 25, 50, 75, 99]:
    x_t, _ = diff.forward_process(x0, t)
    ab = diff.alpha_bars[t].item()
    print(f"  t={t:3d} | alpha_bar={ab:.4f} | x_t={x_t[0].numpy().round(2)}")''',
        'sql': None,
      },
    ],
  },
  # ── ESTATISTICA ──────────────────────────────────────────────────────────────
  {
    'key': 'cap_stat', 'num': '3', 'title': 'Estatistica e Probabilidade',
    'accent': P['teal'], 'bg': P['teal_l'],
    'intro': (
        'Estatistica e probabilidade fornecem a base epistemica para entender '
        'incerteza em ML. Cada modelo faz suposicoes sobre a distribuicao dos dados. '
        'Entender essas suposicoes e validar se sao adequadas define a qualidade '
        'da solucao e a confianca nas predicoes.'
    ),
    'levels': [
      {
        'name': 'Junior', 'accent': P['green'], 'bg': P['green_l'],
        'body': (
            'Domina estatistica descritiva, interpreta metricas de classificacao '
            '(precisao, recall, F1, AUC) e diferencia correlacao de causalidade. '
            'Sabe quando acuracia sozinha e uma metrica enganosa (datasets desbalanceados).'
        ),
        'math': [
            ('media = (1/n) SUM x_i',
             'Media aritmetica: ponto de equilibrio dos dados. Senssivel a outliers. '
             'Para dados com outliers, a mediana e mais robusta.'),
            ('Precision = TP / (TP + FP)',
             'Precisao: dos que o modelo disse POSITIVO, quantos realmente sao? '
             'Alta precisao = poucos falsos alarmes. Importante quando FP e custoso.'),
            ('Recall = TP / (TP + FN)',
             'Recall: dos que sao realmente POSITIVOS, quantos o modelo capturou? '
             'Alto recall = poucos casos perdidos. Importante quando FN e custoso (e.g. fraude, cancer).'),
            ('F1 = 2 * Prec * Rec / (Prec + Rec)',
             'Media harmonica de precisao e recall. Balanceia os dois. '
             'Indispensavel para datasets desbalanceados onde acuracia engana.'),
        ],
        'py': '''import numpy as np
from sklearn.metrics import classification_report, roc_auc_score

# Deteccao de fraude: 1=fraude (raro), 0=legitimo
y_real = np.array([0,0,1,0,1,1,0,0,1,0,1,0,0,1,0])
y_pred = np.array([0,0,1,0,0,1,0,0,1,0,1,0,1,1,0])
y_prob = np.array([.1,.2,.9,.15,.4,.85,.1,.05,.92,.3,.88,.2,.6,.95,.1])

# Estatistica descritiva do score de probabilidade
print(f"Media prob:    {y_prob.mean():.3f}")
print(f"Mediana prob:  {np.median(y_prob):.3f}")
print(f"Desvio padrao: {y_prob.std():.3f}")

print(classification_report(y_real, y_pred,
      target_names=['Legitimo','Fraude']))
print(f"AUC-ROC: {roc_auc_score(y_real, y_prob):.4f}")''',
        'sql': '''-- Metricas de classificacao em SQL
WITH cm AS (
    SELECT
        SUM(CASE WHEN y_real=1 AND y_pred=1 THEN 1 ELSE 0 END) AS TP,
        SUM(CASE WHEN y_real=0 AND y_pred=1 THEN 1 ELSE 0 END) AS FP,
        SUM(CASE WHEN y_real=1 AND y_pred=0 THEN 1 ELSE 0 END) AS FN,
        SUM(CASE WHEN y_real=0 AND y_pred=0 THEN 1 ELSE 0 END) AS TN,
        COUNT(*) AS total
    FROM predicoes
)
SELECT
    ROUND(1.0*(TP+TN)/total,4)              AS acuracia,
    ROUND(1.0*TP/NULLIF(TP+FP,0),4)         AS precisao,
    ROUND(1.0*TP/NULLIF(TP+FN,0),4)         AS recall,
    ROUND(2.0*TP/NULLIF(2*TP+FP+FN,0),4)    AS f1_score
FROM cm;''',
      },
      {
        'name': 'Pleno', 'accent': P['blue'], 'bg': P['blue_l'],
        'body': (
            'Domina maxima verossimilhanca (MLE) e entende sua equivalencia com '
            'minimizacao de cross-entropy. Aplica regularizacao L1/L2 com '
            'fundamentacao probabilistica (priors MAP). Compreende e quantifica '
            'o tradeoff bias-variancia. Usa validacao cruzada corretamente.'
        ),
        'math': [
            ('theta_MLE = argmax SUM log P(x_i | theta)',
             'MLE: parametros que tornam os dados observados mais provaveis. '
             'Equivale a minimizar a cross-entropy entre dados e modelo.'),
            ('L_ridge = MSE + lambda * SUM w_j^2',
             'Regularizacao L2 (Ridge): equivale a MAP estimation com prior gaussiana N(0, 1/lambda). '
             'Pesos grandes sao penalizados — gera solucoes estavel e bem condicionadas.'),
            ('L_lasso = MSE + lambda * SUM |w_j|',
             'Regularizacao L1 (Lasso): equivale a MAP com prior de Laplace. '
             'Gera esparsidade: muitos pesos vao exatamente a zero (selecao de features).'),
            ('Erro_total = Bias^2 + Variancia + Ruido',
             'Decomposicao do erro: Bias = erro sistematico (underfitting). '
             'Variancia = sensibilidade a dados (overfitting). Ruido = irredutivel.'),
        ],
        'py': '''import numpy as np
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

np.random.seed(42)
X = np.linspace(-3, 3, 60).reshape(-1,1)
y = 0.5*X.ravel()**2 + np.random.randn(60)*0.8

# Tradeoff bias-variancia por grau do polinomio
print(f"{'Grau':>5} | {'MSE CV':>8} | {'Std':>7} | Diagnostico")
for grau in [1, 2, 4, 8, 15]:
    pipe = Pipeline([('poly', PolynomialFeatures(grau)),
                     ('reg',  Ridge(alpha=0.01))])
    sc = cross_val_score(pipe, X, y, cv=5,
                         scoring='neg_mean_squared_error')
    mse, std = -sc.mean(), sc.std()
    diag = "underfitting" if grau<2 else ("overfitting" if grau>8 else "OK")
    print(f"{grau:>5} | {mse:>8.3f} | {std:>7.3f} | {diag}")''',
        'sql': '''-- Regularizacao e analise de residuos em SQL
WITH pred AS (
    SELECT y_real,
           0.43*x1 + 0.0*x2 + 1.8 AS y_hat,
           y_real-(0.43*x1+0.0*x2+1.8) AS resid
    FROM dados
)
SELECT
    AVG(POWER(resid,2))                  AS mse,
    -- L2: adiciona lambda * SUM(w^2) — penaliza pesos grandes
    AVG(POWER(resid,2)) + 0.1*(POWER(0.43,2)+POWER(0.0,2)) AS loss_ridge,
    -- L1: adiciona lambda * SUM(|w|) — gera esparsidade
    AVG(POWER(resid,2)) + 0.1*(ABS(0.43)+ABS(0.0))          AS loss_lasso
FROM pred;''',
      },
      {
        'name': 'Senior', 'accent': P['amber'], 'bg': P['amber_l'],
        'body': (
            'Domina inferencia bayesiana completa, implementa expectation-maximization (EM) '
            'para modelos de mistura. Aplica testes de hipotese com correcao para multiplos '
            'testes (Bonferroni, FDR) em experimentos A/B rigorosos. '
            'Trabalha com distribuicoes de cauda pesada para dados com outliers frequentes.'
        ),
        'math': [
            ('P(theta|X) prop. P(X|theta) * P(theta)',
             'Bayes: posterior proporcional a verossimilhanca vezes prior. '
             'A posterior combina evidencia dos dados com conhecimento previo. '
             'Ridge = MAP com prior gaussiana; Lasso = MAP com prior de Laplace.'),
            ('alpha_corr = alpha / n_testes  (Bonferroni)',
             'Correcao de Bonferroni: divide o nivel de significancia pelo numero '
             'de testes realizados. Controla a taxa de erro familia-wise (FWER). '
             'Ex: 10 variantes A/B, alpha=0.05 -> alpha_corr=0.005.'),
        ],
        'py': '''import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

# MAP bayesiano para regressao
np.random.seed(0)
X_b = np.linspace(0, 5, 50)
y_b = 2*X_b + 1 + np.random.randn(50)*1.5

def neg_log_posterior(params, X, y, prior_std=2.0):
    w, b, ls = params
    sig = np.exp(ls)
    log_like  = norm.logpdf(y, w*X+b, sig).sum()
    log_prior = norm.logpdf(w, 0, prior_std) + norm.logpdf(b, 0, prior_std)
    return -(log_like + log_prior)

res = minimize(neg_log_posterior, [0,0,0], args=(X_b, y_b))
w_map, b_map, _ = res.x
print(f"MAP: w={w_map:.3f}, b={b_map:.3f}  (verdadeiro: w=2, b=1)")

# Teste A/B com Bonferroni
n_vars = 5; alpha = 0.05 / n_vars  # correcao
p_vals = [0.032, 0.001, 0.214, 0.008, 0.189]
print(f"\\nAlpha corrigido: {alpha:.3f}")
for i, p in enumerate(p_vals):
    sig = "SIGNIFICATIVO" if p < alpha else "nao sig."
    print(f"  Variante {i+1}: p={p:.3f} -> {sig}")''',
        'sql': None,
      },
      {
        'name': 'Especialista', 'accent': P['violet'], 'bg': P['violet_l'],
        'body': (
            'Domina inferencia variacional (base teorica de VAEs): aproxima posteriors '
            'intratavel minimizando KL(q||p). Implementa MCMC para posteriors complexas. '
            'Aplica teoria de causalidade (DAGs de Pearl, do-calculus) para decisoes '
            'de alto impacto onde correlacao nao e suficiente.'
        ),
        'math': [
            ('ELBO = E_q[log P(X|Z)] - KL(q(Z|X) || p(Z))',
             'Evidence Lower Bound (VAE): maximizar ELBO = maximizar log-evidencia. '
             'Termo 1: qualidade da reconstrucao. Termo 2: alinhamento da posterior '
             'aprendida com a prior (gaussiana padrao).'),
            ("P(Y|do(X=x)) != P(Y|X=x)",
             'Do-calculus de Pearl: condicionar em X (observar) e diferente de '
             'intervir em X (do-operator). A diferenca e confunding — variaveis '
             'de confusao que causam tanto X quanto Y.'),
        ],
        'py': '''import torch, torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, dim=4, lat=2):
        super().__init__()
        self.fc=nn.Linear(dim,16)
        self.mu=nn.Linear(16,lat)
        self.lv=nn.Linear(16,lat)
    def forward(self,x):
        h=torch.relu(self.fc(x))
        return self.mu(h), self.lv(h)

class Decoder(nn.Module):
    def __init__(self, lat=2, dim=4):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(lat,16),nn.ReLU(),nn.Linear(16,dim))
    def forward(self,z): return self.net(z)

def vae_loss(x, x_recon, mu, logvar):
    # Reconstrucao + KL divergence (forma fechada para gaussianas)
    recon = nn.MSELoss(reduction="sum")(x_recon, x)
    kl    = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + kl, recon.item(), kl.item()

enc=Encoder(); dec=Decoder()
x = torch.rand(8, 4)
mu, lv = enc(x)
# Reparametrizacao: z = mu + sigma * eps (eps ~ N(0,I))
# Permite backprop atraves da amostragem
z = mu + torch.exp(0.5*lv) * torch.randn_like(mu)
x_rec = dec(z)
loss, recon, kl = vae_loss(x, x_rec, mu, lv)
print(f"ELBO: {loss.item():.2f} | Recon: {recon:.2f} | KL: {kl:.2f}")''',
        'sql': None,
      },
    ],
  },
  # ── OTIMIZACAO ──────────────────────────────────────────────────────────────
  {
    'key': 'cap_opt', 'num': '4', 'title': 'Otimizacao',
    'accent': P['amber'], 'bg': P['amber_l'],
    'intro': (
        'Todo treinamento de modelo e, em sua essencia, um problema de otimizacao: '
        'encontrar os parametros theta que minimizam a funcao de perda L(theta). '
        'A escolha do algoritmo de otimizacao impacta diretamente a velocidade '
        'de convergencia, a qualidade da solucao e a estabilidade do treinamento.'
    ),
    'levels': [
      {
        'name': 'Junior', 'accent': P['green'], 'bg': P['green_l'],
        'body': (
            'Compreende o loop de treinamento: forward, loss, backward, update. '
            'Entende o papel do learning rate e suas consequencias praticas. '
            'Usa Adam como escolha padrao e monitora curvas de loss para diagnosticar problemas.'
        ),
        'math': [
            ('w_{t+1} = w_t - lr * dL/dw_t',
             'Gradient Descent: subtrai o gradiente multiplicado pelo learning rate. '
             'Uma iteracao por batch (ou dataset completo no caso batch GD).'),
            ('w_{t+1} = w_t - lr * grad_{batch_t}',
             'SGD (Stochastic): usa mini-batch em vez do dataset inteiro. '
             'Mais rapido, ruido do batch pode ajudar a escapar de minimos ruins.'),
        ],
        'py': '''import torch, torch.nn as nn

X = torch.tensor([[1.],[2.],[3.],[4.],[5.],[6.]])
y = torch.tensor([[3.],[5.],[7.],[9.],[11.],[13.]])
model = nn.Linear(1,1)
opt   = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

print(f"{'Ep':>5} | {'Loss':>9}")
for ep in range(300):
    opt.zero_grad()      # 1. Limpa gradientes acumulados
    pred = model(X)      # 2. Forward pass
    loss = loss_fn(pred, y)  # 3. Calcula perda
    loss.backward()      # 4. Backpropagation
    opt.step()           # 5. Atualiza pesos
    if ep % 60 == 0:
        print(f"{ep:>5} | {loss.item():>9.4f}")
w = model.weight.item(); b = model.bias.item()
print(f"Modelo: y = {w:.3f}*x + {b:.3f}  (esperado: 2*x + 1)")''',
        'sql': '''-- Monitoramento de curvas de treinamento no banco
SELECT
    epoca,
    ROUND(loss_treino, 4)   AS loss_train,
    ROUND(loss_val, 4)      AS loss_val,
    CASE
        WHEN loss_val - loss_treino > 0.15 THEN 'OVERFITTING'
        WHEN loss_treino > 0.5            THEN 'UNDERFITTING'
        ELSE 'OK'
    END                     AS diagnostico,
    -- Variacao percentual da loss (detecta platô)
    ROUND(100*(loss_treino - LAG(loss_treino,1) OVER
          (PARTITION BY run_id ORDER BY epoca))
          / NULLIF(LAG(loss_treino,1) OVER
          (PARTITION BY run_id ORDER BY epoca),0), 2) AS delta_pct
FROM training_log
WHERE run_id = 'exp_001'
ORDER BY epoca;''',
      },
      {
        'name': 'Pleno', 'accent': P['blue'], 'bg': P['blue_l'],
        'body': (
            'Domina os principais otimizadores e quando usar cada um. Implementa '
            'learning rate schedulers (warmup + cosine annealing). Usa gradient '
            'accumulation para simular batches maiores em memoria limitada. '
            'Diagnostica problemas de convergencia por curvas de loss.'
        ),
        'math': [
            ('m_t = b1*m_{t-1} + (1-b1)*g_t',
             'Adam — 1o momento: media movel exponencial do gradiente. '
             'b1=0.9 tipicamente. Acumula direcao do gradiente ao longo do tempo.'),
            ('v_t = b2*v_{t-1} + (1-b2)*g_t^2',
             'Adam — 2o momento: media movel do quadrado do gradiente. '
             'b2=0.999. Estima variancia do gradiente por parametro.'),
            ("w = w - lr * m_hat / (sqrt(v_hat) + eps)",
             'Atualizacao Adam: passo adaptativo por parametro. '
             'Parametros com gradiente historicamente alto recebem passos menores.'),
        ],
        'py': '''import torch, torch.nn as nn, numpy as np

model = nn.Sequential(nn.Linear(10,64), nn.ReLU(), nn.Linear(64,1))
X_t, y_t = torch.randn(256,10), torch.randn(256,1)

# Comparativo de otimizadores
for nome, Opt, kw in [
    ('SGD',         torch.optim.SGD,   {'lr':0.01}),
    ('SGD+Momentum',torch.optim.SGD,   {'lr':0.01,'momentum':0.9}),
    ('Adam',        torch.optim.Adam,  {'lr':0.001}),
    ('AdamW',       torch.optim.AdamW, {'lr':0.001,'weight_decay':0.01}),
]:
    for l in model.modules():
        if hasattr(l,'reset_parameters'): l.reset_parameters()
    opt = Opt(model.parameters(), **kw)
    for _ in range(80):
        opt.zero_grad()
        nn.MSELoss()(model(X_t),y_t).backward()
        opt.step()
    with torch.no_grad():
        final_loss = nn.MSELoss()(model(X_t),y_t).item()
    print(f"{nome:15s}: {final_loss:.4f}")

# Warmup + Cosine Annealing
def lr_schedule(step, warmup=50, total=500, lr_max=1e-3):
    if step < warmup:
        return lr_max * (step+1) / warmup
    p = (step-warmup) / (total-warmup)
    return lr_max * 0.5 * (1 + np.cos(np.pi * p))

print("\\nLR Schedule:")
for s in [0,10,50,100,250,499]:
    print(f"  step={s:3d}: lr={lr_schedule(s):.6f}")''',
        'sql': '''-- Comparativo de experimentos de otimizacao
WITH resultados AS (
    SELECT run_id, otimizador,
           MIN(loss_val)  AS melhor_val,
           MIN(CASE WHEN loss_val=(SELECT MIN(lv) FROM training_log l2
                                   WHERE l2.run_id=t.run_id)
               THEN epoca END) AS ep_convergencia
    FROM training_log t
    GROUP BY run_id, otimizador
)
SELECT
    RANK() OVER (ORDER BY melhor_val)  AS ranking,
    otimizador,
    ROUND(melhor_val,5)                AS melhor_val_loss,
    ep_convergencia
FROM resultados ORDER BY ranking;''',
      },
      {
        'name': 'Senior', 'accent': P['amber'], 'bg': P['amber_l'],
        'body': (
            'Compreende a teoria de convergencia de otimizadores, diagnostica '
            'landscape de perda (selas, minimos agudos vs planos). Implementa '
            'mixed precision training e analisa estabilidade monitorando '
            'a norma do gradiente ao longo do treinamento.'
        ),
        'math': [
            ('||g_t|| > C => g_t <- g_t * (C / ||g_t||)',
             'Gradient clipping por norma: re-escala proporcionalmente sem alterar direcao. '
             'Crucial para Transformers e RNNs onde explosao de gradiente e frequente.'),
            ('G_t = rho * G_{t-1} + (1-rho) * g_t^2',
             'RMSProp: media movel do quadrado do gradiente. '
             'Normaliza o passo por feature individualmente. '
             'Adam = RMSProp + Momentum + correcao de vies inicial.'),
        ],
        'py': '''import torch, torch.nn as nn

class Deep(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(*[
            nn.Sequential(nn.Linear(64,64), nn.ReLU())
            for _ in range(5)
        ] + [nn.Linear(64,1)])
    def forward(self,x): return self.net(x)

model = Deep()
opt   = torch.optim.Adam(model.parameters(), lr=1e-3)
X_t, y_t = torch.randn(64,64), torch.randn(64,1)
norms = []

for step in range(30):
    opt.zero_grad()
    nn.MSELoss()(model(X_t),y_t).backward()
    # Norma ANTES do clipping
    n = sum(p.grad.norm()**2 for p in model.parameters()
            if p.grad is not None)**0.5
    norms.append(n.item())
    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    opt.step()

print("Norma do gradiente (primeiros 5 passos):")
for i,v in enumerate(norms[:5]):
    print(f"  step {i}: {v:.4f}")
print(f"Media: {sum(norms)/len(norms):.4f}")''',
        'sql': None,
      },
      {
        'name': 'Especialista', 'accent': P['violet'], 'bg': P['violet_l'],
        'body': (
            'Pesquisa e projeta otimizadores. Domina otimizacao distribuida '
            '(data/model/pipeline parallelism) e seus efeitos na convergencia. '
            'Trabalha com otimizacao multi-objetivo para alinhamento de LLMs '
            '(RLHF, PPO). Implementa otimizadores de segunda ordem (Shampoo, KFAC).'
        ),
        'math': [
            ('L_PPO = E[ min(r_t * A_t, clip(r_t, 1-e, 1+e) * A_t) ]',
             'PPO (base do RLHF): r_t = razao new/old policy. A_t = vantagem estimada. '
             'Clipping previne atualizacoes grandes — chave para estabilidade em fine-tuning de LLMs.'),
            ('delta_nat = F^{-1} * grad_L',
             'Gradiente natural: F = Fisher Information Matrix. '
             'Passo invariante a reparametrizacao — otimiza na geometria da distribuicao, '
             'nao no espaco euclidiano. KFAC aproxima F^{-1} eficientemente.'),
        ],
        'py': '''import torch

def ppo_loss(log_new, log_old, adv, eps=0.2):
    """
    log_new/old: log-probs da policy nova e antiga
    adv: vantagem normalizada
    """
    ratio  = torch.exp(log_new - log_old)  # r_t = pi_new / pi_old
    surr1  = ratio * adv
    surr2  = torch.clamp(ratio, 1-eps, 1+eps) * adv
    # Pessimista: min garante que nao exploramos demais a policy
    return -torch.mean(torch.min(surr1, surr2))

B = 64  # batch size
log_old = torch.randn(B).detach()
log_new = log_old + 0.15 * torch.randn(B)
adv     = torch.randn(B)

loss = ppo_loss(log_new, log_old, adv)
ratios = torch.exp(log_new - log_old)
print(f"PPO Loss: {loss.item():.4f}")
print(f"Ratios: min={ratios.min():.3f}, max={ratios.max():.3f}")
clipped = torch.clamp(ratios, 0.8, 1.2)
print(f"Apos clip: min={clipped.min():.3f}, max={clipped.max():.3f}")''',
        'sql': None,
      },
    ],
  },
  # ── TEORIA DA INFORMACAO ────────────────────────────────────────────────────
  {
    'key': 'cap_info', 'num': '5', 'title': 'Teoria da Informacao',
    'accent': P['green'], 'bg': P['green_l'],
    'intro': (
        'A teoria da informacao, desenvolvida por Claude Shannon em 1948, quantifica '
        'informacao e incerteza de maneira precisa. Em ML, ela fundamenta as '
        'funcoes de perda mais utilizadas e conecta aprendizado, compressao e '
        'distribuicoes de probabilidade num framework unificado.'
    ),
    'levels': [
      {
        'name': 'Junior', 'accent': P['green'], 'bg': P['green_l'],
        'body': (
            'Compreende entropia como medida de incerteza: maxima para distribuicoes '
            'uniformes, zero para distribuicoes certas. Sabe usar CrossEntropyLoss '
            'corretamente em PyTorch e entende o que ela mede concretamente.'
        ),
        'math': [
            ('H(p) = -SUM p(x) * log2(p(x))',
             'Entropia de Shannon: incerteza em bits. '
             'Distribuicao uniforme com 8 classes: H = log2(8) = 3 bits (maxima). '
             'Uma classe certa com prob 1: H = 0 bits (minima).'),
            ('H(p, q) = -SUM p(x) * log(q(x))',
             'Cross-entropy: "custo" de usar modelo q para descrever dados que seguem p. '
             'Minimizar H(p,q) em relacao a q = aprender q mais proximo de p.'),
            ('L_CE = -log(prob_classe_correta)',
             'Para classificacao com y one-hot: a soma colapsa para o negativo '
             'do log da probabilidade predita para a classe verdadeira. '
             '-log(0.01) = 4.6 (penalidade alta). -log(0.99) = 0.01 (penalidade baixa).'),
        ],
        'py': '''import numpy as np, torch, torch.nn as nn

# Entropia de Shannon
def H(p):
    p = np.array(p, float); p = p[p>0]
    return -np.sum(p * np.log2(p))

print(f"H uniforme (4 cls): {H([.25,.25,.25,.25]):.3f} bits (max=2)")
print(f"H certeza:          {H([1,0,0,0]):.3f} bits")
print(f"H preferencia:      {H([.7,.1,.1,.1]):.3f} bits")

# Cross-entropy loss: manual vs PyTorch
logits = torch.tensor([[2.0, 1.0, 0.1],  # logits amostra 1
                        [0.5, 2.5, 0.3]]) # logits amostra 2
labels = torch.tensor([0, 1])             # classes verdadeiras

probs = torch.softmax(logits, dim=1)
# Manual: -log(prob da classe correta)
manual = -torch.log(probs[torch.arange(2), labels]).mean()
# PyTorch: ja aplica softmax internamente
pytorch = nn.CrossEntropyLoss()(logits, labels)

print(f"\\nCE manual: {manual.item():.4f}")
print(f"CE PyTorch:{pytorch.item():.4f}  (devem ser iguais)")
print(f"Probs preditas: {probs.detach().numpy().round(3)}")''',
        'sql': '''-- Entropia por classe e balanceamento do dataset
WITH dist AS (
    SELECT classe,
           COUNT(*) AS n,
           COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS prob
    FROM rotulos
    GROUP BY classe
)
SELECT
    classe, n,
    ROUND(prob, 4)                             AS probabilidade,
    -- Auto-informacao: surpresa ao observar esta classe
    ROUND(-LOG(prob) / LOG(2), 3)              AS surpresa_bits,
    -- Contribuicao desta classe para a entropia total
    ROUND(-prob * LOG(prob) / LOG(2), 4)       AS contrib_entropia
FROM dist
UNION ALL
SELECT 'TOTAL', SUM(n),
    1.0,
    -- Entropia total do dataset
    ROUND(SUM(-prob*LOG(prob)/LOG(2)), 4),
    ROUND(SUM(-prob*LOG(prob)/LOG(2)), 4)
FROM dist;''',
      },
      {
        'name': 'Pleno', 'accent': P['blue'], 'bg': P['blue_l'],
        'body': (
            'Domina a relacao fundamental entre cross-entropy e MLE. Compreende '
            'KL divergence e sua assimetria. Entende ganho de informacao em arvores '
            'de decisao e usa informacao mutua como criterio de selecao de features.'
        ),
        'math': [
            ('KL(p||q) = SUM p(x) * log(p(x)/q(x))',
             'KL divergence: informacao extra necessaria para codificar amostras de p '
             'usando q em vez de p. KL >= 0 sempre (desigualdade de Jensen). '
             'KL(p||q) != KL(q||p) — e assimetrica.'),
            ('H(p,q) = H(p) + KL(p||q)',
             'Relacao fundamental: cross-entropy = entropia de p + KL(p||q). '
             'Minimizar H(p,q) em theta = minimizar KL(p||q_theta). '
             'MLE e exatamente isso: encontrar q_theta mais proximo de p.'),
            ('IG = H(S) - SUM_v (|Sv|/|S|) * H(Sv)',
             'Ganho de Informacao em arvores de decisao: reducao de entropia ao '
             'dividir dataset S pelo atributo A. Escolhe split que mais reduz incerteza.'),
        ],
        'py': '''import numpy as np

def kl(p, q, eps=1e-10):
    p, q = np.array(p)+eps, np.array(q)+eps
    p /= p.sum(); q /= q.sum()
    return np.sum(p * np.log(p / q))

def ce(p, q, eps=1e-10):
    p, q = np.array(p)+eps, np.array(q)+eps
    p /= p.sum(); q /= q.sum()
    return -np.sum(p * np.log(q))

def H(p, eps=1e-10):
    p = np.array(p)+eps; p /= p.sum()
    return -np.sum(p * np.log(p))

p = [0.6, 0.3, 0.1]; q = [0.2, 0.5, 0.3]

print(f"KL(p||q) = {kl(p,q):.4f}")
print(f"KL(q||p) = {kl(q,p):.4f}  (assimetrica!)")
print(f"H(p)     = {H(p):.4f}")
print(f"KL(p||q) + H(p) = {H(p)+kl(p,q):.4f}")
print(f"H(p,q)           = {ce(p,q):.4f}  (devem coincidir)")

# Ganho de informacao para um split
def ig(dataset_labels, esq, dir):
    n = len(dataset_labels)
    return (H(np.bincount(dataset_labels)/n)
            - len(esq)/n * H(np.bincount(esq)/len(esq) if len(esq)>0 else [1])
            - len(dir)/n * H(np.bincount(dir)/len(dir) if len(dir)>0 else [1]))

todos = [0,0,0,1,1,1,1]; esq = [0,0,0]; dir = [1,1,1,1]
print(f"\\nGanho de Informacao: {ig(todos, esq, dir):.4f} bits")''',
        'sql': '''-- KL divergence e ganho de informacao em SQL
WITH dist AS (
    SELECT classe,
           COUNT(*)*1.0/SUM(COUNT(*)) OVER ()  AS p_real,
           AVG(prob_pred)                       AS q_pred
    FROM predicoes GROUP BY classe
)
SELECT
    -- KL(p||q): custo de usar q_pred em vez de p_real
    SUM(p_real * LOG(p_real / NULLIF(q_pred,0)))  AS kl_divergence,
    -- Cross-entropy H(p,q)
    -SUM(p_real * LOG(NULLIF(q_pred,0)))           AS cross_entropy,
    -- Entropia do dataset H(p)
    -SUM(p_real * LOG(p_real))                     AS entropia_real
FROM dist;''',
      },
      {
        'name': 'Senior', 'accent': P['amber'], 'bg': P['amber_l'],
        'body': (
            'Domina divergencias-f e sua relacao com diferentes arquiteturas de GAN. '
            'Usa informacao mutua para analisar representacoes em aprendizado contrastivo. '
            'Compreende entropia diferencial para variaveis continuas — base de '
            'fluxos normalizantes e modelos de densidade.'
        ),
        'math': [
            ('JSD(p||q) = 0.5*KL(p||m) + 0.5*KL(q||m),  m=(p+q)/2',
             'Jensen-Shannon Divergence: versao simetrica e limitada da KL. '
             'JSD em [0, log2]. GAN original minimiza JSD entre dados reais e gerados. '
             'Problema: JSD = log(2) quando suportes nao se sobrepoem (inicio do treino).'),
            ('W_1(p,q) = inf_{gamma in P(p,q)} E_{(x,y)~gamma}[||x-y||]',
             'Distancia de Wasserstein (Earth Movers Distance): custo minimo para '
             'transportar massa de p para q. Continua e suave mesmo sem sobreposicao '
             '— base do WGAN, mais estavel para treinar.'),
        ],
        'py': '''import numpy as np, torch, torch.nn as nn

def jsd(p, q, eps=1e-10):
    """Jensen-Shannon Divergence: simetrica, em [0, log(2)]"""
    p, q = np.array(p)+eps, np.array(q)+eps
    p /= p.sum(); q /= q.sum()
    m = 0.5*(p+q)
    return 0.5*(np.sum(p*np.log(p/m)) + np.sum(q*np.log(q/m)))

# Demonstracao: por que WGAN substitui JSD
p_real = [0.9, 0.1, 0.0, 0.0]
q_sem  = [0.0, 0.0, 0.1, 0.9]  # sem sobreposicao
q_com  = [0.0, 0.1, 0.8, 0.1]  # leve sobreposicao
print(f"JSD sem sobreposicao: {jsd(p_real,q_sem):.4f} (= log2={np.log(2):.4f})")
print(f"JSD com sobreposicao: {jsd(p_real,q_com):.4f} (diferente!)")
print("Wasserstein cresce suavemente mesmo sem sobreposicao.")

# InfoNCE Loss (base do SimCLR / CLIP)
def infonce(z1, z2, tau=0.07):
    z1 = nn.functional.normalize(z1, dim=1)
    z2 = nn.functional.normalize(z2, dim=1)
    N  = z1.shape[0]
    sim = (z1 @ z2.T) / tau          # (N x N) similaridades
    labels = torch.arange(N)          # positivo na diagonal
    return nn.CrossEntropyLoss()(sim, labels)

z1 = torch.randn(16, 64)
z2 = z1 + 0.1 * torch.randn_like(z1)  # views similares
print(f"\\nInfoNCE Loss: {infonce(z1, z2).item():.4f}")''',
        'sql': None,
      },
      {
        'name': 'Especialista', 'accent': P['violet'], 'bg': P['violet_l'],
        'body': (
            'Aplica MDL (Minimum Description Length) como justificativa teorica para '
            'regularizacao. Pesquisa aprendizado contrastivo pela lente de informacao mutua '
            '(InfoNCE bound). Aplica teoria da informacao a privacidade diferencial '
            '(Renyi DP) para treinar modelos com garantias formais de privacidade.'
        ),
        'math': [
            ('L_MDL = -log P(dados|modelo) + L(modelo)',
             'MDL: o melhor modelo comprime dados + descricao do proprio modelo. '
             'Modelos simples ganham se verossimilhanca similar — formalizacao de Occam. '
             'Equivalente a regularizacao bayesiana.'),
            ('M satisfaz eps-DP: P[M(D) in S] <= e^eps * P[M(D\') in S]',
             'Privacidade Diferencial: output do mecanismo M muda no maximo por fator '
             'e^eps quando um individuo e adicionado/removido. eps <= 1 = fortemente privado.'),
        ],
        'py': '''import numpy as np, torch, torch.nn as nn

# DP-SGD: Gradientes privatizados para treinamento diferentemente privado
class DPMechanism:
    def __init__(self, C=1.0, sigma_mult=1.1):
        self.C = C           # sensibilidade L2 (clipping)
        self.sigma = sigma_mult * C

    def privatize(self, params):
        total_norm = sum(p.grad.norm()**2 for p in params
                         if p.grad is not None)**0.5
        # 1. Clip per-sample (limita sensibilidade)
        clip = min(1.0, self.C / (total_norm.item() + 1e-6))
        for p in params:
            if p.grad is not None:
                p.grad.data.mul_(clip)
                # 2. Adiciona ruido gaussiano calibrado
                p.grad.data.add_(torch.randn_like(p.grad) * self.sigma)

    def epsilon_estimate(self, n, batch, steps):
        """Estimativa simplificada de epsilon consumido."""
        q = batch / n   # prob de sampling
        return steps * 2 * q**2 / (2 * self.sigma**2)

model = nn.Linear(10, 1)
dp    = DPMechanism(C=1.0, sigma_mult=1.1)
X_p, y_p = torch.randn(64, 10), torch.randn(64, 1)

model.zero_grad()
nn.MSELoss()(model(X_p), y_p).backward()

g_antes = model.weight.grad.norm().item()
dp.privatize(list(model.parameters()))
g_depois = model.weight.grad.norm().item()

eps = dp.epsilon_estimate(n=10000, batch=64, steps=1000)
print(f"Norma grad antes DP:  {g_antes:.4f}")
print(f"Norma grad depois DP: {g_depois:.4f}")
print(f"Epsilon estimado (1000 passos): {eps:.4f}")
print(f"(eps < 1.0 = fortemente privado, eps < 10 = pratico)")''',
        'sql': None,
      },
    ],
  },
]

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════════════════════
def build():
    out = '/mnt/user-data/outputs/matematica_ml_profissional.pdf'

    frame_main = Frame(MARGIN_L, MARGIN_B, CW, H - MARGIN_T - MARGIN_B,
                       id='main', leftPadding=0, rightPadding=0,
                       topPadding=0, bottomPadding=0)
    frame_cover = Frame(MARGIN_L, MARGIN_B, CW, H - 30 - MARGIN_B,
                        id='cover', leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)

    tpl_cover = PageTemplate(id='cover', frames=[frame_cover], onPage=on_cover)
    tpl_main  = PageTemplate(id='main',  frames=[frame_main],  onPage=on_page)

    doc = AcademicDoc(out, pagesize=A4,
                      pageTemplates=[tpl_cover, tpl_main],
                      leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                      topMargin=MARGIN_T, bottomMargin=MARGIN_B)

    story = []

    # ── CAPA ─────────────────────────────────────────────────────────────────
    story.append(sp(18))
    # Linha superior decorativa
    story.append(Table([['']], colWidths=[CW],
                       style=TableStyle([('LINEABOVE',(0,0),(-1,-1),2,P['violet']),
                                         ('TOPPADDING',(0,0),(-1,-1),0),
                                         ('BOTTOMPADDING',(0,0),(-1,-1),0)])))
    story.append(sp(10))
    story.append(Paragraph('UNIVERSIDADE DE SAO PAULO', ST['cov_inst']))
    story.append(Paragraph('Instituto de Matematica e Estatistica', ST['cov_inst']))
    story.append(Paragraph('Departamento de Ciencia da Computacao', ST['cov_inst']))
    story.append(sp(16))
    story.append(Paragraph(
        'Fundamentos Matematicos para<br/>Data Science e Machine Learning',
        ST['cov_title']))
    story.append(sp(8))
    story.append(Paragraph(
        'Algebra Linear · Calculo · Estatistica · Otimizacao · Teoria da Informacao',
        ST['cov_sub']))
    story.append(sp(14))
    # Meta info
    meta_data = [[
        Paragraph('Lucas Rodrigues', ParagraphStyle('_m', fontSize=9, textColor=P['text_main'], alignment=TA_CENTER)),
        Paragraph('Guia Progressivo', ParagraphStyle('_m2', fontSize=9, textColor=P['blue'], alignment=TA_CENTER)),
        Paragraph('2024 — Versao 2.0', ParagraphStyle('_m3', fontSize=9, textColor=P['text_muted'], alignment=TA_CENTER)),
    ]]
    mt = Table(meta_data, colWidths=[CW/3]*3)
    mt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['bg_card']),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LINEBEFORE',    (1,0),(2,-1),  0.5, P['border']),
    ]))
    story.append(mt)
    story.append(sp(16))

    # Mapa dos pilares (capa)
    story.append(MathMap(CW, 195))
    story.append(sp(4))
    story.append(Paragraph(
        'Figura 1 — Relacao entre os pilares matematicos e o Machine Learning.',
        ST['caption']))
    story.append(sp(14))

    # Abstract
    abs_border = Table([[Paragraph(
        '<b>Resumo.</b> Este artigo apresenta os fundamentos matematicos essenciais para '
        'praticantes de Data Science e Machine Learning em quatro niveis de profundidade '
        'progressiva: Junior, Pleno, Senior e Especialista. Para cada pilar — '
        'Algebra Linear, Calculo, Estatistica, Otimizacao e Teoria da Informacao — '
        'sao apresentadas as expressoes matematicas com explicacoes autocontidas, '
        'implementacoes em Python e consultas SQL com aplicacoes praticas em cenarios '
        'reais de dados. O artigo inclui um glossario de notacoes matematicas e um '
        'vocabulario tecnico para leitores em formacao.',
        ST['cov_abs'])]], colWidths=[CW])
    abs_border.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['bg_card']),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ('LINEABOVE',     (0,0),(-1,0),  1.5, P['teal']),
        ('LINEBEFORE',    (0,0),(0,-1),  1.5, P['teal']),
    ]))
    story.append(abs_border)
    story.append(sp(8))
    story.append(Paragraph(
        '<b>Palavras-chave:</b> algebra linear, calculo diferencial, estatistica bayesiana, '
        'otimizacao, teoria da informacao, machine learning, data science.',
        ST['cov_kw']))

    # ── TROCA PARA TEMPLATE PRINCIPAL ────────────────────────────────────────
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.append(NextPageTemplate('main'))
    story.append(PageBreak())

    # ── SUMARIO ───────────────────────────────────────────────────────────────
    story.append(LabeledAnchor('toc', 'Sumario', 0))
    story.append(colored_bar('Sumario', P['bg_card2'], P['white'], 14, 10, 14))
    story.append(sp(8))
    story.append(hr(P['violet'], 1, 0, 8))

    toc_entries = [
        ('0', 'Sumario de Notacoes Matematicas', 'not'),
        ('0', 'Glossario de Termos Tecnicos', 'glos'),
        ('1', 'Algebra Linear', 'cap_al'),
        ('2', 'Calculo Diferencial e Integral', 'cap_calc'),
        ('3', 'Estatistica e Probabilidade', 'cap_stat'),
        ('4', 'Otimizacao', 'cap_opt'),
        ('5', 'Teoria da Informacao', 'cap_info'),
    ]
    sublevel_labels = ['Junior', 'Pleno', 'Senior', 'Especialista']

    for num, title, key in toc_entries:
        is_main = num not in ('0',)
        # TOC entry com link interno
        link_text = (f'<link dest="{key}"><u>{num}. {title}</u></link>'
                     if is_main else
                     f'<link dest="{key}"><u>{title}</u></link>')
        row = Table([[
            Paragraph(link_text,
                ParagraphStyle('_tl', fontName='Helvetica-Bold', fontSize=10,
                               textColor=P['blue'] if is_main else P['teal'],
                               leading=16)),
            Paragraph('· · · · · · · · ·',
                ParagraphStyle('_td', fontSize=8, textColor=P['border_l'],
                               alignment=TA_CENTER)),
        ]], colWidths=[CW*0.7, CW*0.3])
        row.setStyle(TableStyle([
            ('TOPPADDING',    (0,0),(-1,-1), 3),
            ('BOTTOMPADDING', (0,0),(-1,-1), 3),
            ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ]))
        story.append(row)

        if is_main:
            for lv in sublevel_labels:
                lv_key = f"{key}_{lv.lower()}"
                lv_row = Table([[
                    Paragraph(
                        f'  <link dest="{lv_key}">· Nivel {lv}</link>',
                        ParagraphStyle('_tlv', fontSize=8.5, textColor=P['text_muted'],
                                       leading=14)),
                ]], colWidths=[CW])
                lv_row.setStyle(TableStyle([
                    ('TOPPADDING',    (0,0),(-1,-1),1),
                    ('BOTTOMPADDING', (0,0),(-1,-1),1),
                    ('LEFTPADDING',   (0,0),(-1,-1),20),
                ]))
                story.append(lv_row)
        story.append(sp(3))

    story.append(PageBreak())

    # ── SUMARIO DE NOTACOES MATEMATICAS ──────────────────────────────────────
    story.append(LabeledAnchor('not', 'Sumario de Notacoes Matematicas', 0))
    story.append(colored_bar('Sumario de Notacoes Matematicas', P['violet_l'], P['white'], 14))
    story.append(sp(4))
    story.append(Paragraph(
        'Esta secao apresenta as notacoes matematicas utilizadas ao longo do artigo. '
        'Cada simbolo e descrito com seu nome formal, significado e um exemplo concreto. '
        'O leitor e encorajado a retornar a esta secao sempre que encontrar uma notacao desconhecida.',
        ST['body']))
    story.append(sp(8))

    # Cabecalho da tabela de notacoes
    hdr_data = [[
        Paragraph('Simbolo / Notacao', ParagraphStyle('_nh', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=P['white'])),
        Paragraph('Nome', ParagraphStyle('_nh2', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=P['white'])),
        Paragraph('Descricao e Exemplo', ParagraphStyle('_nh3', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=P['white'])),
    ]]
    hdr_t = Table(hdr_data, colWidths=[CW*0.20, CW*0.18, CW*0.62])
    hdr_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['violet']),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ]))
    story.append(hdr_t)

    for i, (sym, name, desc, example) in enumerate(NOTATION_GLOSSARY):
        bg = P['bg_card'] if i % 2 == 0 else P['bg_card2']
        row_data = [[
            Paragraph(sym, ST['nota_math']),
            Paragraph(name, ST['glos_term']),
            Paragraph(f'{desc}<br/><font color="#D4B07E" name="Courier"><i>Ex: {example}</i></font>',
                      ParagraphStyle('_nd', fontSize=8, textColor=P['text_main'],
                                     leading=12)),
        ]]
        row_t = Table(row_data, colWidths=[CW*0.20, CW*0.18, CW*0.62])
        row_t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), bg),
            ('TOPPADDING',    (0,0),(-1,-1), 6),
            ('BOTTOMPADDING', (0,0),(-1,-1), 6),
            ('LEFTPADDING',   (0,0),(-1,-1), 8),
            ('RIGHTPADDING',  (0,0),(-1,-1), 6),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ('GRID',          (0,0),(-1,-1), 0.2, P['border']),
        ]))
        story.append(row_t)

    story.append(sp(6))
    nota_box = Table([[Paragraph(
        '<b>Nota sobre logaritmos:</b> Em machine learning, "log" sem base especificada '
        'quase invariavelmente denota o logaritmo natural (base e ≈ 2.718, tambem escrito ln). '
        'Em teoria da informacao, "log" frequentemente significa log na base 2 (resultado em bits). '
        'O contexto determina a convencao; os exemplos de codigo sempre usam np.log() (natural).',
        ST['nota'])]], colWidths=[CW])
    nota_box.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['amber_l']),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ('LINEBEFORE',    (0,0),(0,-1),  2.5, P['amber']),
    ]))
    story.append(nota_box)
    story.append(PageBreak())

    # ── GLOSSARIO DE TERMOS TECNICOS ─────────────────────────────────────────
    story.append(LabeledAnchor('glos', 'Glossario de Termos Tecnicos', 0))
    story.append(colored_bar('Glossario de Termos Tecnicos', P['teal_l'], P['white'], 14))
    story.append(sp(4))
    story.append(Paragraph(
        'Vocabulario tecnico utilizado no artigo. Cada termo inclui definicao conceitual '
        'e a formulacao matematica quando aplicavel. Termos marcados com (*) sao '
        'prerequisitos para os niveis Senior e Especialista.',
        ST['body']))
    story.append(sp(8))

    for i, (term, defn, formula) in enumerate(WORD_GLOSSARY):
        bg = P['bg_card'] if i % 2 == 0 else P['bg_card2']
        inner = [
            [Paragraph(term, ST['glos_term'])],
            [Paragraph(defn, ST['glos_def'])],
        ]
        if formula:
            inner.append([Paragraph(formula, ST['glos_math'])])
        inner_t = Table(inner, colWidths=[CW - 20])
        inner_t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), bg),
            ('TOPPADDING',    (0,0),(-1,-1), 3),
            ('BOTTOMPADDING', (0,0),(-1,-1), 3),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ]))
        outer = Table([[inner_t]], colWidths=[CW])
        outer.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), bg),
            ('TOPPADDING',    (0,0),(-1,-1), 7),
            ('BOTTOMPADDING', (0,0),(-1,-1), 7),
            ('LEFTPADDING',   (0,0),(-1,-1), 14),
            ('RIGHTPADDING',  (0,0),(-1,-1), 12),
            ('LINEBEFORE',    (0,0),(0,-1),  2, P['teal']),
            ('LINEBELOW',     (0,-1),(-1,-1),0.2, P['border']),
        ]))
        story.append(outer)
        story.append(sp(3))

    story.append(PageBreak())

    # ── CAPITULOS ─────────────────────────────────────────────────────────────
    for topic in TOPICS:
        # Anchor do capitulo
        story.append(LabeledAnchor(topic['key'], f"{topic['num']}. {topic['title']}", 0))

        # Header colorido do capitulo
        story.append(colored_bar(
            f"  {topic['num']}.  {topic['title']}",
            topic['bg'], topic['accent'], 15, 12, 16))
        story.append(sp(8))

        # Introducao do capitulo
        intro_t = Table([[Paragraph(topic['intro'], ST['body'])]], colWidths=[CW])
        intro_t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), P['bg_card']),
            ('TOPPADDING',    (0,0),(-1,-1), 10),
            ('BOTTOMPADDING', (0,0),(-1,-1), 10),
            ('LEFTPADDING',   (0,0),(-1,-1), 14),
            ('RIGHTPADDING',  (0,0),(-1,-1), 14),
            ('LINEBEFORE',    (0,0),(0,-1),  2.5, topic['accent']),
        ]))
        story.append(intro_t)
        story.append(sp(12))
        story.append(section_rule(P['border']))
        story.append(sp(8))

        # Niveis
        for lv in topic['levels']:
            lv_key = f"{topic['key']}_{lv['name'].lower()}"
            story.append(LabeledAnchor(lv_key, f"  {topic['num']}.x  Nivel {lv['name']}", 1))
            story += level_section(
                lv['name'], lv['accent'], lv['bg'],
                lv['body'],
                math_items=lv.get('math'),
                py_code=lv.get('py'),
                sql_code=lv.get('sql'),
            )

        story.append(PageBreak())

    # ── PAGINA FINAL: SEQUENCIA DE ESTUDO ────────────────────────────────────
    story.append(LabeledAnchor('sequencia', 'Sequencia de Estudo Recomendada', 0))
    story.append(colored_bar('Sequencia de Estudo Recomendada', P['bg_card2'], P['white'], 14))
    story.append(sp(8))
    story.append(Paragraph(
        'A sequencia abaixo reflete a dependencia natural entre os pilares matematicos. '
        'Cada etapa prepara o terreno conceitual para a seguinte. '
        'O aprendizado mais efetivo combina estudo teorico com implementacao pratica imediata.',
        ST['body']))
    story.append(sp(12))

    seq = [
        (P['blue'],   '1', 'Algebra Linear',
         'Entenda o que os dados sao e como os modelos processam informacao matricialmente. '
         'Comece com numpy, vetores e multiplicacao de matrizes.'),
        (P['coral'],  '2', 'Calculo',
         'Entenda como o modelo aprende: gradiente, derivadas, backpropagation. '
         'Implemente gradient descent manualmente em Python.'),
        (P['teal'],   '3', 'Estatistica',
         'Entenda se o modelo funciona bem e por que. Detecte overfitting, '
         'valide com cross-validation, interprete metricas.'),
        (P['amber'],  '4', 'Otimizacao',
         'Entenda como convergir mais rapido e escolher o algoritmo certo. '
         'Experimente Adam vs SGD e learning rate schedulers.'),
        (P['green'],  '5', 'Teoria da Informacao',
         'Entenda por que certas funcoes de perda fazem sentido matematico. '
         'Compreenda entropia, cross-entropy e KL divergence.'),
    ]
    for col, num, title, desc in seq:
        srow = Table([[
            Paragraph(num, ParagraphStyle('_sn', fontName='Helvetica-Bold',
                       fontSize=18, textColor=P['bg_page'], alignment=TA_CENTER,
                       leading=22)),
            Table([[
                Paragraph(title, ParagraphStyle('_st', fontName='Helvetica-Bold',
                           fontSize=10.5, textColor=col, leading=14)),
                Paragraph(desc, ParagraphStyle('_sd', fontSize=9, leading=14,
                           textColor=P['text_main'], alignment=TA_JUSTIFY)),
            ]], colWidths=[CW*0.5 - 44])
        ]], colWidths=[44, CW - 44])
        srow.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(0,0), col),
            ('BACKGROUND',    (1,0),(1,0), P['bg_card']),
            ('TOPPADDING',    (0,0),(-1,-1), 10),
            ('BOTTOMPADDING', (0,0),(-1,-1), 10),
            ('LEFTPADDING',   (0,0),(0,0), 10),
            ('LEFTPADDING',   (1,0),(1,0), 14),
            ('RIGHTPADDING',  (0,0),(-1,-1), 12),
            ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,-1),(-1,-1), 0.4, P['border']),
        ]))
        story.append(srow)
        story.append(sp(4))

    story.append(sp(16))
    final = Table([[Paragraph(
        'Voce nao precisa dominar toda a teoria antes de construir o primeiro modelo. '
        'O caminho mais efetivo e alternar entre estudo e pratica: cada equacao aprendida '
        'deve se traduzir em codigo funcionando. A matematica e a linguagem — '
        'o codigo e a conversacao.',
        ParagraphStyle('_fi', fontSize=10, textColor=P['text_main'], leading=16,
                       alignment=TA_CENTER, fontName='Helvetica-BoldOblique'))]], colWidths=[CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), P['violet_l']),
        ('TOPPADDING',    (0,0),(-1,-1), 14),
        ('BOTTOMPADDING', (0,0),(-1,-1), 14),
        ('LEFTPADDING',   (0,0),(-1,-1), 18),
        ('RIGHTPADDING',  (0,0),(-1,-1), 18),
        ('LINEBEFORE',    (0,0),(0,-1),  3, P['violet']),
        ('LINEAFTER',     (0,-1),(-1,-1),3, P['violet']),
    ]))
    story.append(final)

    doc.build(story)
    print(f'PDF gerado: {out}')

build()