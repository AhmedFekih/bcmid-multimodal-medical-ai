"""
scripts/generate_translated_english_report_pdf.py
Generates the authoritative 12-page English translation of BCMID_Rapport_Final_Condense.pdf.
Strictly mirrors the 12-page structure, exact layout, figures, tables, and references.
"""

import os
import sys
from pathlib import Path
from PIL import Image as PILImage
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image as RLImage
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "bcmid_work" / "reports" / "figures" / "extracted_pdf_images"
OUTPUT_EN_PDF = BASE_DIR / "bcmid_work" / "reports" / "BCMID_Technical_Report_EN.pdf"
OUTPUT_EN_GRAND_PDF = BASE_DIR / "bcmid_work" / "reports" / "BCMID_Grand_Technical_Report.pdf"

# Color Palette matching the French document
C_PRIMARY = colors.HexColor("#0f172a")       # Dark Slate Header
C_NAVY = colors.HexColor("#1e3a8a")          # Deep Navy
C_CRIMSON = colors.HexColor("#b91c1c")       # Red Banner
C_PURPLE = colors.HexColor("#7c3aed")        # Chapter Tag
C_BLUE_BG = colors.HexColor("#f0f7ff")       # Callout Background
C_BORDER_BLUE = colors.HexColor("#3b82f6")   # Callout Border
C_TEXT_DARK = colors.HexColor("#1e293b")     # Body Text
C_MUTED = colors.HexColor("#64748b")         # Subtitles / Footers
C_LIGHT_GRAY = colors.HexColor("#f8fafc")    # Table alt row
C_BORDER_GRAY = colors.HexColor("#cbd5e1")   # Table border


class TwelvePageCanvas(canvas.Canvas):
    """Custom canvas that draws running headers and footers matching BCMID_Rapport_Final_Condense.pdf."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        page_num = self._pageNumber
        # Draw opaque white background on every page
        self.saveState()
        self.setFillColor(colors.white)
        self.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        self.restoreState()

        if page_num == 1:
            # Page 1 has custom cover decorations drawn by flowables
            return

        self.saveState()
        # Running Header
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_DARK)
        self.drawString(1.8 * cm, A4[1] - 1.2 * cm, "ESPRIT / Deep Learning & AI")

        # BCMID logo on top right of header
        logo_path = IMG_DIR / "page_2_img_1_FormXob.7dd60bb9e187bd26a4b243b6ea94402f.png"
        if logo_path.exists():
            try:
                self.drawImage(str(logo_path), A4[0] - 4.6 * cm, A4[1] - 1.45 * cm, width=2.8 * cm, height=0.7 * cm, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass

        # Thin rule under header
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(1.8 * cm, A4[1] - 1.55 * cm, A4[0] - 1.8 * cm, A4[1] - 1.55 * cm)

        # Running Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)
        self.drawString(1.8 * cm, 1.0 * cm, "BCMID / ESPRIT | 2026–2027")
        self.drawRightString(A4[0] - 1.8 * cm, 1.0 * cm, str(page_num))
        self.restoreState()


def get_image(filename: str, width: float, height: float):
    path = IMG_DIR / filename
    if path.exists():
        return RLImage(str(path), width=width, height=height)
    return Spacer(width, height)


def build_callout(text: str, title: str = "", styles=None, width=17.4*cm):
    content = []
    if title:
        content.append(Paragraph(f"<b>{title}</b>", styles["CalloutTitle"]))
        content.append(Spacer(1, 1.5*mm))
    content.append(Paragraph(text, styles["CalloutText"]))

    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_BG),
        ('BOX', (0,0), (-1,-1), 1.0, C_BORDER_BLUE),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def build_english_pdf():
    OUTPUT_EN_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_EN_PDF),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.6 * cm,
        title="BCMID – Academic Project Report (Technical & Architecture)",
        author="Ikbel Hamdi, Ahmed Fekih, Mohammed Malek Hammami, Samar Omrani"
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    styles.add(ParagraphStyle(
        'CoverTop',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=C_PRIMARY
    ))
    styles.add(ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=C_MUTED
    ))
    styles.add(ParagraphStyle(
        'CoverBannerTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        'CoverBannerSub',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        'CoverDesc',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=C_NAVY
    ))
    styles.add(ParagraphStyle(
        'CoverMetaLabel',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_PRIMARY
    ))
    styles.add(ParagraphStyle(
        'CoverMetaVal',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'CoverFooter',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=C_MUTED
    ))

    styles.add(ParagraphStyle(
        'H1_Title',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=C_PRIMARY,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'ChapterTag',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=C_PURPLE,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'ChapterTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=C_PRIMARY,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'H2_Subtitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=6,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'BodyEN',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        alignment=TA_JUSTIFY,
        textColor=C_TEXT_DARK,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'BodyBoldEN',
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12.2,
        textColor=C_PRIMARY
    ))
    styles.add(ParagraphStyle(
        'CalloutTitle',
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12,
        textColor=C_NAVY
    ))
    styles.add(ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=C_TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'FigCaption',
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=C_MUTED,
        spaceBefore=3,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=C_PRIMARY
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=C_TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=C_PRIMARY
    ))

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 : COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    # Header Logos
    esprit_logo = get_image("page_1_img_2_FormXob.a47a285059900b5e971ee591a7499316.png", width=3.8*cm, height=1.9*cm)
    bcmid_logo = get_image("page_1_img_1_FormXob.7d82a16874bc329b7d820c7e940452e8.png", width=4.5*cm, height=1.1*cm)

    t_logos = Table([[esprit_logo, "", bcmid_logo]], colWidths=[5.5*cm, 6.4*cm, 5.5*cm])
    t_logos.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_logos)
    story.append(Spacer(1, 1.2*cm))

    # Title Block
    story.append(Paragraph("ACADEMIC PROJECT<br/>REPORT", styles['CoverTop']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Module: Deep Learning & Artificial Intelligence<br/>Engineering Cycle – 5th Year", styles['CoverSub']))
    story.append(Spacer(1, 1.0*cm))

    # Red Banner
    banner_content = [
        Spacer(1, 4*mm),
        Paragraph("BCMID", styles['CoverBannerTitle']),
        Paragraph("Breast Cancer Multimodal Imaging & Diagnosis", styles['CoverBannerSub']),
        Spacer(1, 4*mm)
    ]
    t_banner = Table([[banner_content]], colWidths=[17.4*cm])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CRIMSON),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 1.0*cm))

    # Project Subtitle
    story.append(Paragraph("Design and Evaluation of an Intelligent Decision Support System<br/>for Breast Imaging Interpretation", styles['CoverDesc']))
    story.append(Spacer(1, 1.4*cm))

    # Meta Table: Authors and Supervisor
    col_left = [
        Paragraph("<b>Conducted by:</b>", styles['CoverMetaLabel']),
        Spacer(1, 2*mm),
        Paragraph("Ikbel Hamdi<br/>Ahmed Fekih<br/>Mohammed Malek Hammami<br/>Samar Omrani", styles['CoverMetaVal'])
    ]
    col_right = [
        Paragraph("<b>Supervised by:</b>", styles['CoverMetaLabel']),
        Spacer(1, 1.5*mm),
        Paragraph("Mme Oumayma Guesmi", styles['CoverMetaVal']),
        Spacer(1, 4*mm),
        Paragraph("<b>Institution:</b>", styles['CoverMetaLabel']),
        Spacer(1, 1.5*mm),
        Paragraph("ESPRIT – École Supérieure Privée<br/>d'Ingénierie et de Technologies", styles['CoverMetaVal'])
    ]

    t_meta = Table([[col_left, col_right]], colWidths=[8.7*cm, 8.7*cm])
    t_meta.setStyle(TableStyle([
        ('LINEBEFORE', (0,0), (0,0), 0.5, colors.transparent),
        ('LINEAFTER', (0,0), (0,0), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 1.4*cm))

    # Cover Footer
    story.append(Paragraph("Applied AI in Medicine Research Project · Academic prototype subject to human validation", styles['CoverFooter']))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph("<b>2026–2027</b>", ParagraphStyle('Y', fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER, textColor=C_PRIMARY)))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 : EXECUTIVE SUMMARY & ABSTRACT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Résumé", styles['H1_Title']))
    p_resume = (
        "Le projet <b>BCMID</b> (<i>Breast Cancer Multimodal Imaging & Diagnosis</i>) vise à concevoir un prototype "
        "d’assistance à l’interprétation d’examens mammaires intégrant des données d’imagerie hétérogènes et des connaissances documentaires. "
        "L’approche relie la <b>mammographie numérique plein champ (FFDM)</b> et l’<b>échographie</b> à une architecture répartie en <b>sept agents spécialisés</b>, "
        "afin de produire un compte rendu structuré, explicable et soumis à vérification.<br/><br/>"
        "Le dispositif comprend un prétraitement des examens, deux branches <b>ResNet-18</b>, des cartes <b>Grad-CAM</b>, un système de recherche documentaire "
        "<b>Clinical RAG</b> (BAAI/bge-small-en-v1.5 et FAISS), un agent de synthèse piloté par <b>Qwen2.5-3B-Instruct</b> et une couche de sécurité déterministe. "
        "L’orchestration est assurée par <b>n8n</b>, en relation avec des microservices <b>FastAPI</b>.<br/><br/>"
        "Sur le corpus du projet (332 patientes, 2 001 images brutes, 321 rapports PDF), le sous-ensemble multimodal de 323 patientes obtient une <b>ROC-AUC de 0,8198</b> "
        "(« malin contre autres »), contre 0,7917 pour la mammographie seule et 0,6743 pour l’échographie seule. L’audit XAI rapporte <b>87,4 % d’énergie Grad-CAM</b> dans le "
        "masque mammaire ; <b>61/61 tests logiciels</b> sont réussis. Ces résultats demeurent exploratoires : les annotations ne constituent pas une vérité terrain "
        "histologique, le corpus est limité et aucune validation clinique prospective n’est fournie.<br/><br/>"
        "<b>Mots-clés :</b> imagerie mammaire, fusion multimodale, ResNet-18, Grad-CAM, RAG, FAISS, Qwen2.5, agents intelligents, sécurité clinique."
    )
    story.append(Paragraph(p_resume, styles['BodyEN']))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("Abstract", styles['H1_Title']))
    p_abstract = (
        "<b>BCMID</b> is an academic prototype supporting the interpretation of breast imaging by combining full-field digital mammography, "
        "ultrasound and clinical documentary knowledge through seven specialized agents (data quality, dual-branch ResNet-18 vision with Grad-CAM, "
        "FAISS-based clinical retrieval, Qwen2.5-3B-Instruct reasoning, deterministic safety checks and structured reporting), coordinated by n8n and FastAPI. "
        "On 323 patients with both modalities, multimodal ensemble ROC-AUC reaches <b>0.8198</b> versus 0.7917 (mammography) and 0.6743 (ultrasound); "
        "61 software tests pass, 10/10 adversarial scenarios are neutralized and 17/20 reports are compliant on first pass. These observations do not establish "
        "medical effectiveness: labels derive from BI-RADS annotations, the cohort is small and no external clinical validation was conducted.<br/><br/>"
        "<b>Keywords:</b> multimodal breast imaging, explainable deep learning, clinical RAG, multi-agent orchestration, human oversight."
    )
    story.append(Paragraph(p_abstract, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 : TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Table of Contents", styles['H1_Title']))
    story.append(Spacer(1, 4*mm))

    toc_data = [
        [Paragraph("<b>Résumé</b>", styles['BodyBoldEN']), Paragraph("2", styles['TableCellBold'])],
        [Paragraph("<b>Abstract</b>", styles['BodyBoldEN']), Paragraph("2", styles['TableCellBold'])],
        [Paragraph("<b>Table of Contents</b>", styles['BodyBoldEN']), Paragraph("3", styles['TableCellBold'])],
        [Paragraph("<b>General Introduction</b>", styles['BodyBoldEN']), Paragraph("4", styles['TableCellBold'])],
        [Paragraph("<b>Context and Multi-Agent Architecture</b>", styles['BodyBoldEN']), Paragraph("5", styles['TableCellBold'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Clinical Context and Challenges", styles['TableCell']), Paragraph("5", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement, Objectives and Scope", styles['TableCell']), Paragraph("5", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Justification of an Agentic Architecture", styles['TableCell']), Paragraph("5", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Global Architecture and the Seven Agents", styles['TableCell']), Paragraph("6", styles['TableCell'])],
        [Paragraph("<b>Data and Multimodal Analysis</b>", styles['BodyBoldEN']), Paragraph("7", styles['TableCellBold'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Medical Corpus and Annotation Distribution", styles['TableCell']), Paragraph("7", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Preprocessing, Quality Control and Leakage-Free Protocol", styles['TableCell']), Paragraph("7", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 ResNet-18 Models and Multimodal Fusion", styles['TableCell']), Paragraph("8", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Explainability with Grad-CAM", styles['TableCell']), Paragraph("8", styles['TableCell'])],
        [Paragraph("<b>Clinical RAG and Prompt Engineering</b>", styles['BodyBoldEN']), Paragraph("9", styles['TableCellBold'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Knowledge Base and Semantic Search", styles['TableCell']), Paragraph("9", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Choice and Integration of Qwen2.5-3B-Instruct", styles['TableCell']), Paragraph("9", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Structuring Medical Prompts", styles['TableCell']), Paragraph("9", styles['TableCell'])],
        [Paragraph("<b>Automation, Validation and Results</b>", styles['BodyBoldEN']), Paragraph("10", styles['TableCellBold'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 FastAPI Services and n8n Workflows", styles['TableCell']), Paragraph("10", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Control Loop and Automated Error Correction", styles['TableCell']), Paragraph("10", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Safety, Data Protection and Regulatory Boundaries", styles['TableCell']), Paragraph("10", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Multimodal Classification Performance", styles['TableCell']), Paragraph("11", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Agentic Pipeline Audit and Case Study", styles['TableCell']), Paragraph("11", styles['TableCell'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Critical Discussion and Threats to Validity", styles['TableCell']), Paragraph("12", styles['TableCell'])],
        [Paragraph("<b>General Conclusion</b>", styles['BodyBoldEN']), Paragraph("12", styles['TableCellBold'])],
        [Paragraph("<b>Bibliographical References</b>", styles['BodyBoldEN']), Paragraph("12", styles['TableCellBold'])],
    ]
    t_toc = Table(toc_data, colWidths=[16.0*cm, 1.4*cm])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(t_toc)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 : GENERAL INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("General Introduction", styles['H1_Title']))
    p_intro_1 = (
        "Breast cancer represents a major public health concern, for which the quality of medical imaging interpretation plays a decisive role. "
        "Breast examination mobilizes mammography, ultrasound, clinical records and standardized diagnostic reference systems: these sources are highly "
        "complementary, yet their heterogeneity demands a rigorous methodology to minimize interpretation errors."
    )
    p_intro_2 = (
        "Deep learning enables the automated extraction of rich representations useful for classification, and explainable AI (XAI) techniques such as "
        "Grad-CAM visualize regions associated with model decisions. Nonetheless, an elevated probability score does not constitute clinical proof, "
        "and an activation heatmap does not confirm the anatomical presence of a lesion. Large language models (LLMs) facilitate the generation of structured summaries, "
        "yet a fluent response may contain numerical discrepancies or ungrounded assertions. It is therefore vital to segregate image analysis, documentary knowledge retrieval "
        "and report synthesis, while subjecting all outputs to deterministic, independent checks."
    )
    p_intro_3 = (
        "<b>BCMID</b> combines two ResNet-18 vision branches with Grad-CAM, a Clinical RAG retrieval module (FAISS) and a Qwen2.5-3B-Instruct model, structured across "
        "seven specialized agents orchestrated via n8n and FastAPI. <b>The central goal is to study how an explainable, traceable multimodal architecture "
        "can articulate visual predictions, documentary groundings and report generation while strictly preserving human supervision.</b> "
        "BCMID is an academic research and demonstration prototype, and not an approved clinical medical device."
    )
    story.append(Paragraph(p_intro_1, styles['BodyEN']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(p_intro_2, styles['BodyEN']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(p_intro_3, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 : CHAPTER 1: CONTEXT & MULTI-AGENT ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 1", styles['ChapterTag']))
    story.append(Paragraph("Context and Multi-Agent Architecture", styles['ChapterTitle']))

    story.append(Paragraph("1.1 Clinical Context and Challenges", styles['H2_Subtitle']))
    p_1_1 = (
        "Full-Field Digital Mammography (FFDM, CC and MLO views) enables the detection of microcalcifications and subtle architectural distortions; "
        "ultrasound characterizes the solid versus cystic nature of an anomaly, its margins and its posterior acoustic behavior. Combining modalities aims "
        "to exploit non-identical physical information. Interpretation becomes significantly more challenging in dense breast tissue, causing sensitivity to vary [1]."
    )
    story.append(Paragraph(p_1_1, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    fig_1_1 = get_image("page_5_img_2_FormXob.965992cbdc958b110d6ec5c59b07b9b7.png", width=14.5*cm, height=5.5*cm)
    story.append(fig_1_1)
    story.append(Paragraph("<b>Figure 1.1:</b> Examples of mammography and ultrasound data from the project image dataset.", styles['FigCaption']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("1.2 Problem Statement, Objectives and Scope", styles['H2_Subtitle']))
    p_1_2 = (
        "How can multiple medical modalities be analyzed jointly, their results linked to documentary evidence, and a structured summary generated whose "
        "coherence can be verified prior to specialist review? Four core challenges emerge: <b>D1 Data Heterogeneity</b>; <b>D2 Interpretability</b> (revealing "
        "influential areas without framing them as confirmed lesions); <b>D3 Documentary Grounding</b> (tying syntheses to identifiable citations); "
        "<b>D4 Output Safety</b> (preventing contradictory, inaccurate or unreviewed statements)."
    )
    story.append(Paragraph(p_1_2, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    callout_scope = (
        "<b>Scope:</b> BCMID is an academic decision-support prototype, not an approved medical device nor an autonomous diagnostic system. "
        "A BI-RADS category derived from a numeric score matrix must never be confused with a clinical radiological assessment performed according "
        "to the ACR Atlas [2]. The <code>human_review_required</code> field materializes this essential safeguard."
    )
    story.append(build_callout(callout_scope, "", styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("1.3 Justification of an Agentic Architecture", styles['H2_Subtitle']))
    p_1_3 = (
        "BCMID does not delegate all operations to a single generative model. Images are preprocessed and verified before analysis, probabilities originate "
        "from dedicated vision encoders, references are retrieved via RAG, and LLM text is audited prior to dispatch. Dividing the pipeline into autonomous "
        "agents segregates ingestion, vision prediction, knowledge retrieval, report writing and safety auditing; n8n sequencing renders inputs, outputs and "
        "rejection points traceable at every phase. This justification is architectural: it does not imply an empirical benchmark across alternative orchestrators."
    )
    story.append(Paragraph(p_1_3, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6 : 1.4 GLOBAL ARCHITECTURE AND THE SEVEN AGENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("1.4 Global Architecture and the Seven Agents", styles['H2_Subtitle']))
    fig_1_2 = get_image("page_6_img_2_FormXob.d84c4e091dcf5f764922ec624046b15b.png", width=16.8*cm, height=9.5*cm)
    story.append(fig_1_2)
    story.append(Paragraph("<b>Figure 1.2:</b> BCMID Architecture: seven agents, n8n orchestrator, infrastructure, monitoring and clinical end-users.", styles['FigCaption']))
    story.append(Spacer(1, 2*mm))

    agents_table_data = [
        [Paragraph("<b>Agent</b>", styles['TableHead']),
         Paragraph("<b>Responsibilities and Methods</b>", styles['TableHead']),
         Paragraph("<b>Technologies</b>", styles['TableHead']),
         Paragraph("<b>Outputs</b>", styles['TableHead'])],
        [Paragraph("<b>01 – Ingestion</b>", styles['TableCellBold']),
         Paragraph("Reception, metadata verification, SHA-256 hashing, pseudonymization", styles['TableCell']),
         Paragraph("Python, pandas", styles['TableCell']),
         Paragraph("Verified dossier, pseudonymized ID", styles['TableCell'])],
        [Paragraph("<b>02 – Data Quality</b>", styles['TableCellBold']),
         Paragraph("Profiling, Otsu thresholding, OCR, inpainting, patient-level splitting", styles['TableCell']),
         Paragraph("OpenCV, EasyOCR", styles['TableCell']),
         Paragraph("Normalized tensors, quality report", styles['TableCell'])],
        [Paragraph("<b>03 – Vision</b>", styles['TableCellBold']),
         Paragraph("Dual ResNet-18, multimodal fusion, scores, Grad-CAM attention", styles['TableCell']),
         Paragraph("PyTorch, torchvision", styles['TableCell']),
         Paragraph("Probabilities, uncertainty, heatmaps", styles['TableCell'])],
        [Paragraph("<b>04 – Clinical RAG</b>", styles['TableCellBold']),
         Paragraph("Semantic encoding, dual FAISS indices, cross-fold patient filtering", styles['TableCell']),
         Paragraph("bge-small-en-v1.5, FAISS IndexFlatIP", styles['TableCell']),
         Paragraph("Grounded excerpts [G1], [E1]", styles['TableCell'])],
        [Paragraph("<b>05 – Reasoning</b>", styles['TableCellBold']),
         Paragraph("Evidence aggregation, schema-constrained structured synthesis", styles['TableCell']),
         Paragraph("Qwen2.5-3B-Instruct", styles['TableCell']),
         Paragraph("Structured JSON report proposition", styles['TableCell'])],
        [Paragraph("<b>06 – Quality & Safety</b>", styles['TableCellBold']),
         Paragraph("Numerical tolerance, semantic grounding, citation validation", styles['TableCell']),
         Paragraph("Deterministic rules, pytest", styles['TableCell']),
         Paragraph("Approval, revision or flagged alert", styles['TableCell'])],
        [Paragraph("<b>07 – Reporting</b>", styles['TableCellBold']),
         Paragraph("Delivery in structured multi-target formats (doctor / technician)", styles['TableCell']),
         Paragraph("ReportLab, FastAPI, Pydantic, n8n", styles['TableCell']),
         Paragraph("PDF report, JSON, interactive Web view", styles['TableCell'])],
    ]
    t_agents = Table(agents_table_data, colWidths=[2.8*cm, 7.2*cm, 3.8*cm, 3.6*cm])
    t_agents.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_agents)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 7 : CHAPTER 2: DATA & MULTIMODAL ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 2", styles['ChapterTag']))
    story.append(Paragraph("Data and Multimodal Analysis", styles['ChapterTitle']))

    story.append(Paragraph("2.1 Medical Corpus and Annotation Distribution", styles['H2_Subtitle']))
    p_2_1 = (
        "The patient level constitutes the primary grouping unit in order to preserve absolute independence between training and validation sets."
    )
    story.append(Paragraph(p_2_1, styles['BodyEN']))

    corpus_table_data = [
        [Paragraph("<b>Dataset Metric</b>", styles['TableHead']),
         Paragraph("<b>Volume</b>", styles['TableHead']),
         Paragraph("<b>Specification / Description</b>", styles['TableHead'])],
        [Paragraph("Registered Patients", styles['TableCellBold']), Paragraph("332", styles['TableCell']), Paragraph("327 of which feature supervised labels", styles['TableCell'])],
        [Paragraph("Raw Medical Images", styles['TableCellBold']), Paragraph("2,001", styles['TableCell']), Paragraph("Before quality control and artifact filtering", styles['TableCell'])],
        [Paragraph("Retained Images", styles['TableCellBold']), Paragraph("1,974", styles['TableCell']), Paragraph("951 mammograms and 1,023 ultrasound scans", styles['TableCell'])],
        [Paragraph("Medical PDF Reports", styles['TableCellBold']), Paragraph("321", styles['TableCell']), Paragraph("320 retained for clinical RAG after filtering", styles['TableCell'])],
        [Paragraph("Bimodal Patients", styles['TableCellBold']), Paragraph("323", styles['TableCell']), Paragraph("Complete cohort for ROC-AUC benchmarking", styles['TableCell'])],
        [Paragraph("Overall Volume", styles['TableCellBold']), Paragraph("12.11 GB", styles['TableCell']), Paragraph("Documented across raw archive packages", styles['TableCell'])],
    ]
    t_corpus = Table(corpus_table_data, colWidths=[4.8*cm, 2.6*cm, 10.0*cm])
    t_corpus.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_corpus)
    story.append(Spacer(1, 2*mm))

    p_2_1_b = (
        "Lesion categories comprise normal (15.1%), benign (64.5%), malignant (19.0%) and five unlabelled BI-RADS 0 cases (1.5%). "
        "The benign class predominance constrains aggregated metric interpretation. The supervised target is derived from BI-RADS "
        "annotations rather than independent histological proof: the evaluation measures alignment with project annotations."
    )
    story.append(Paragraph(p_2_1_b, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    fig_2_1 = get_image("page_7_img_1_FormXob.65f6dbf63f0503b5f4e3660af3671cf6.png", width=12.5*cm, height=3.8*cm)
    story.append(fig_2_1)
    story.append(Paragraph("<b>Figure 2.1:</b> Breakdown of the 332 patients across annotation categories.", styles['FigCaption']))
    story.append(Spacer(1, 1*mm))

    story.append(Paragraph("2.2 Preprocessing, Quality Control and Leakage-Free Protocol", styles['H2_Subtitle']))
    p_2_2 = (
        "• <b>Profiling and Integrity:</b> Formats, salted pseudonymized IDs, duplicates, corrupted scans, metadata concordance.<br/>"
        "• <b>Spatial Preprocessing:</b> Breast region segmentation via Otsu thresholding, background masking, 224×224 resize, normalization.<br/>"
        "• <b>Burn-in Text Removal:</b> Ultrasound metadata detected via EasyOCR, masked and inpainted using Navier–Stokes algorithms.<br/>"
        "• <b>Patient Partitioning:</b> 5-fold cross-validation with GroupKFold; Clinical RAG strictly excludes current patient and fold documents."
    )
    story.append(Paragraph(p_2_2, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    fig_2_2 = get_image("page_7_img_3_FormXob.e8dff2516579f840fe1a575e8b69871f.png", width=15.0*cm, height=3.8*cm)
    story.append(fig_2_2)
    story.append(Paragraph("<b>Figure 2.2:</b> Examples of preprocessing, polarity correction and burn-in text inpainting.", styles['FigCaption']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 8 : 2.3 RESNET-18 & 2.4 GRAD-CAM EXPLAINABILITY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    callout_precaution = (
        "<b>Methodological Precaution:</b> An image-level split is insufficient when a patient possesses multiple scans. "
        "Patient-level grouping and RAG document isolation represent two distinct, mandatory safeguards against data leakage, "
        "to be audited upon every reproduction cycle."
    )
    story.append(build_callout(callout_precaution, "", styles))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("2.3 ResNet-18 Models and Multimodal Fusion", styles['H2_Subtitle']))
    p_2_3 = (
        "Each imaging modality is fed into a single-channel 224×224 ResNet-18 encoder [3], accounting for distinct textures and physics. "
        "Four fusion strategies are evaluated: <b>late fusion</b> (score averaging), <b>weighted logit fusion</b>, <b>uncertainty-guided fusion</b> "
        "(weight inversely proportional to Shannon entropy) and <b>multimodal ensemble</b> combining previous models with test-time augmentation (TTA). "
        "Shannon entropy <i>H(p) = -Σ p<sub>c</sub> log<sub>2</sub> p<sub>c</sub></i> serves as an internal uncertainty metric; it does not turn outputs "
        "into clinically calibrated probabilities. The benchmark covers 323 patients (GroupKFold, malignant vs other) without undocumented hyperparameter tuning."
    )
    story.append(Paragraph(p_2_3, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("2.4 Explainability with Grad-CAM", styles['H2_Subtitle']))
    p_2_4 = (
        "Grad-CAM [4] utilizes target class gradients with respect to convolutional feature maps: "
        "<i>α<sub>k</sub><sup>c</sup> = (1/Z) Σ<sub>i,j</sub> ∂y<sup>c</sup>/∂A<sub>i,j</sub><sup>k</sup></i> and "
        "<i>L<sup>c</sup> = ReLU(Σ<sub>k</sub> α<sub>k</sub><sup>c</sup> A<sup>k</sup>)</i>. "
        "The spatial audit evaluates 387 heatmaps across 64 validation dossiers: average activation energy inside the segmented breast parenchyma "
        "reaches <b>87.4%</b> (with 12.6% outside). This confirms spatially plausible attention, without claiming systematic lesion correspondence."
    )
    story.append(Paragraph(p_2_4, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    fig_2_3 = get_image("page_8_img_1_FormXob.332ed0f6aa2216348cba63c98de4748b.png", width=16.0*cm, height=6.2*cm)
    story.append(fig_2_3)
    story.append(Paragraph("<b>Figure 2.3:</b> Original scans, activation heatmaps and Grad-CAM overlays for mammography and ultrasound.", styles['FigCaption']))
    story.append(Spacer(1, 2*mm))

    p_articulation = (
        "<b>Articulation between Vision and Documentary Agents:</b> The vision agent transmits raw logits, probabilities, uncertainties "
        "and Grad-CAM visual overlays; documentary and generative agents must never modify these numerical values. High ROC-AUC and plausible "
        "heatmaps do not replace histological benchmarks or radiologist sign-off: hence the mandate for independent deterministic safety checks."
    )
    story.append(Paragraph(p_articulation, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 9 : CHAPTER 3: CLINICAL RAG & PROMPT ENGINEERING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 3", styles['ChapterTag']))
    story.append(Paragraph("Clinical RAG and Prompt Engineering", styles['ChapterTitle']))

    story.append(Paragraph("3.1 Knowledge Base and Semantic Search", styles['H2_Subtitle']))
    p_3_1 = (
        "Clinical RAG retrieves documentary passages describing rules and relevant observations so that the generative LLM justifies its phrasing "
        "against an explicit grounding context; it documents the synthesis without certifying clinical veracity. Texts are extracted, cleaned, "
        "chunked, encoded via <b>BAAI/bge-small-en-v1.5</b> (384 dimensions) and indexed in <b>FAISS IndexFlatIP</b> (inner product of unit vectors, "
        "equivalent to cosine similarity [5, 6]). Two separate vector stores are retained:<br/>"
        "• <b>Guidelines Index:</b> Nine prototype rules derived from ACR BI-RADS principles (non-exhaustive, non-official);<br/>"
        "• <b>Cases Index:</b> 320 sanitized historical patient reports (one excluded), chunked into 995 passages.<br/>"
        "Token lengths and overlap are not documented as clinically validated. Query search returns up to four passages ([G1] or [E1]), whose validity "
        "is confirmed downstream. Two filters mitigate data leakage: <code>text_blind</code> (redacting BI-RADS categories, cancer confirmations or surgeries) "
        "and <code>exclude_pseudo_id</code> (removing current patient and fold records)."
    )
    story.append(Paragraph(p_3_1, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("3.2 Choice and Integration of Qwen2.5-3B-Instruct", styles['H2_Subtitle']))
    p_3_2 = (
        "The selection of Qwen2.5-3B-Instruct [7] is motivated by its compact footprint, local on-premise execution and superior instruction-following "
        "capability (occupying ~3.1 GB VRAM on a Tesla T4 GPU in project testing). <b>The LLM was deliberately not fine-tuned:</b> domain adaptation "
        "relies entirely on structured prompt engineering and RAG context, while supervised fine-tuning was appropriately applied to the vision backbones. "
        "Greedy decoding at temperature=0.0 minimizes stochastic drift without asserting absolute determinism. No comparative LLM benchmark is documented."
    )
    story.append(Paragraph(p_3_2, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("3.3 Structuring Medical Prompts", styles['H2_Subtitle']))
    prompt_table_data = [
        [Paragraph("<b>Prompt Section</b>", styles['TableHead']),
         Paragraph("<b>Integrated Information</b>", styles['TableHead']),
         Paragraph("<b>Targeted Constraint</b>", styles['TableHead'])],
        [Paragraph("<b>SYSTEM</b>", styles['TableCellBold']),
         Paragraph("Synthesis persona, clinical neutrality, strict ban on fabricating observations", styles['TableCell']),
         Paragraph("Prevent ungrounded claims, enforce JSON grammar", styles['TableCell'])],
        [Paragraph("<b>CONTEXT</b>", styles['TableCellBold']),
         Paragraph("Vision logits, uncertainty, Grad-CAM summary, authorized history, RAG passages", styles['TableCell']),
         Paragraph("Segregate calculated facts from documentary citations", styles['TableCell'])],
        [Paragraph("<b>TASK</b>", styles['TableCellBold']),
         Paragraph("Cross-modal reconciliation, interpretation and proposed follow-up", styles['TableCell']),
         Paragraph("Ensure medical coherence with provided context", styles['TableCell'])],
        [Paragraph("<b>OUTPUT</b>", styles['TableCellBold']),
         Paragraph("Mandatory schema keys and expected data types", styles['TableCell']),
         Paragraph("Enable automated deterministic JSON validation", styles['TableCell'])],
    ]
    t_prompt = Table(prompt_table_data, colWidths=[3.2*cm, 8.2*cm, 6.0*cm])
    t_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_prompt)
    story.append(Spacer(1, 2*mm))

    p_3_3_b = (
        "The output schema enforces six keys: <code>predicted_birads</code>, <code>confidence</code>, <code>interpretation</code>, "
        "<code>recommendations</code>, <code>limitations</code>, <code>human_review_required</code>. The confidence metric represents an internal "
        "heuristic, not a validated clinical probability. A total of <b>190 prompts</b> were constructed (64 image-only, 62 text-only, 64 multimodal); "
        "these figures reflect experimental setup and do not claim statistical superiority across conditions."
    )
    story.append(Paragraph(p_3_3_b, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    callout_rag_eval = (
        "<b>Evaluation of RAG:</b> No quantitative table of precision, Recall@4 or chunking comparisons was provided in the baseline source; "
        "no synthetic metric is fabricated. Nine rules and 995 chunks do not constitute a full validation of retrieval quality. "
        "Prompt iteration logs are maintained separately from experimental laboratory traces."
    )
    story.append(build_callout(callout_rag_eval, "", styles))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 10 : CHAPTER 4: AUTOMATION, VALIDATION & RESULTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 4", styles['ChapterTag']))
    story.append(Paragraph("Automation, Validation and Results", styles['ChapterTitle']))

    story.append(Paragraph("4.1 FastAPI Services and n8n Workflows", styles['H2_Subtitle']))
    p_4_1 = (
        "Processing steps are exposed as FastAPI REST endpoints; n8n orchestrates sequential execution, enforces routing conditions and maintains "
        "an audit trail. Two workflows are documented: <b>BCMID-Medical-Analysis</b> (8-node main pipeline, webhook to structured report) and "
        "<b>Triage</b> (9 nodes: ingestion, ID extraction, report retrieval, conditional branching, dispatch). Triage relies on the logical flag "
        "<code>requires_immediate_escalation</code>; urgent branches trigger on heuristic BI-RADS 4A–5 categories. These flows simulate hospital IT "
        "and do not constitute an active production deployment inside a certified PACS/HIS."
    )
    story.append(Paragraph(p_4_1, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("4.2 Control Loop and Automated Error Correction", styles['H2_Subtitle']))
    p_4_2 = (
        "The Reasoning ↔ Quality & Safety coupling is essential: LLM proposals undergo deterministic validation independent of generated assertions. "
        "Upon detecting an anomaly, Agent 6 refuses approval and issues targeted corrective feedback; two revision cycles are authorized before "
        "flagging the dossier as <code>FLAGGED_FOR_MANUAL_CLINICIAN_REVIEW</code>."
    )
    story.append(Paragraph(p_4_2, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    rules_table_data = [
        [Paragraph("<b>Audit Check</b>", styles['TableHead']), Paragraph("<b>Deterministic Verification Rule</b>", styles['TableHead'])],
        [Paragraph("Numerical Consistency", styles['TableCellBold']), Paragraph("Tolerated gap between quoted and vision probability: |Δp| ≤ 0.006", styles['TableCell'])],
        [Paragraph("Uncertainty Guard", styles['TableCellBold']), Paragraph("When prototype entropy H ≥ 0.50, mandate explicit cautionary phrasing", styles['TableCell'])],
        [Paragraph("Clinical Entities", styles['TableCellBold']), Paragraph("Reject medical findings not attested by vision models or authorized dossier text", styles['TableCell'])],
        [Paragraph("Citation Integrity", styles['TableCellBold']), Paragraph("Every reference token must match a valid chunk in current retrieval context", styles['TableCell'])],
        [Paragraph("Supervision Enforcer", styles['TableCellBold']), Paragraph("Enforce explicit disclaimer; unconditionally impose human_review_required = true", styles['TableCell'])],
    ]
    t_rules = Table(rules_table_data, colWidths=[4.2*cm, 13.2*cm])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_rules)
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("4.3 Safety, Data Protection and Regulatory Boundaries", styles['H2_Subtitle']))
    p_4_3 = (
        "A continuous malignancy score is mapped to an indicative category and internal workflow priority. This table is purely heuristic and not "
        "clinically validated; it must neither be confused with ACR BI-RADS diagnostic criteria nor guide real patient treatment without a radiologist."
    )
    story.append(Paragraph(p_4_3, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    calib_table_data = [
        [Paragraph("<b>Score p<sub>mal</sub></b>", styles['TableHead']),
         Paragraph("<b>Indicative Category</b>", styles['TableHead']),
         Paragraph("<b>Internal Priority Action</b>", styles['TableHead'])],
        [Paragraph("p < 0.02", styles['TableCell']), Paragraph("BI-RADS 1", styles['TableCell']), Paragraph("Routine screening interval", styles['TableCell'])],
        [Paragraph("0.02 ≤ p < 0.10", styles['TableCell']), Paragraph("BI-RADS 2", styles['TableCell']), Paragraph("Routine screening interval", styles['TableCell'])],
        [Paragraph("0.10 ≤ p < 0.35", styles['TableCell']), Paragraph("BI-RADS 3", styles['TableCell']), Paragraph("Short-interval 6-month surveillance", styles['TableCell'])],
        [Paragraph("0.35 ≤ p < 0.65", styles['TableCell']), Paragraph("BI-RADS 4A", styles['TableCellBold']), Paragraph("Workflow escalation (Urgent notification)", styles['TableCell'])],
        [Paragraph("0.65 ≤ p < 0.85", styles['TableCell']), Paragraph("BI-RADS 4B", styles['TableCellBold']), Paragraph("Workflow escalation (Urgent notification)", styles['TableCell'])],
        [Paragraph("0.85 ≤ p < 0.95", styles['TableCell']), Paragraph("BI-RADS 4C", styles['TableCellBold']), Paragraph("Workflow escalation (Urgent notification)", styles['TableCell'])],
        [Paragraph("p ≥ 0.95", styles['TableCell']), Paragraph("BI-RADS 5", styles['TableCellBold']), Paragraph("Workflow escalation (Urgent notification)", styles['TableCell'])],
    ]
    t_calib = Table(calib_table_data, colWidths=[4.0*cm, 4.4*cm, 9.0*cm])
    t_calib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.0),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_calib)
    story.append(Spacer(1, 2*mm))

    p_4_3_b = (
        "The architecture implements patient ID pseudonymization via salted SHA-256 and burn-in ultrasound text inpainting; on-premise execution "
        "of FAISS and the LLM limits cloud exfiltration. Pseudonymization is not permanent anonymization: key management, access logs and retention "
        "policies remain mandatory. GDPR, HIPAA and European MDR 2017/745 [8] form regulatory frameworks to address; the prototype does not claim formal certification."
    )
    story.append(Paragraph(p_4_3_b, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 11 : 4.4 BENCHMARK & 4.5 PIPELINE AUDIT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4.4 Multimodal Classification Performance", styles['H2_Subtitle']))
    p_4_4 = (
        "Reported metrics address distinct objectives: classification (323 patients), XAI audit (387 heatmaps) and software resilience tests, "
        "each using specific samples and criteria."
    )
    story.append(Paragraph(p_4_4, styles['BodyEN']))
    story.append(Spacer(1, 1*mm))

    bench_table_data = [
        [Paragraph("<b>Model Configuration</b>", styles['TableHead']),
         Paragraph("<b>ROC-AUC</b>", styles['TableHead']),
         Paragraph("<b>Clinical Sensitivity</b>", styles['TableHead'])],
        [Paragraph("Mammography Alone (ResNet-18)", styles['TableCellBold']), Paragraph("0.7917", styles['TableCell']), Paragraph("76.2 %", styles['TableCell'])],
        [Paragraph("Ultrasound Alone (ResNet-18)", styles['TableCellBold']), Paragraph("0.6743", styles['TableCell']), Paragraph("68.4 %", styles['TableCell'])],
        [Paragraph("Late Fusion (Averaging)", styles['TableCellBold']), Paragraph("0.8150", styles['TableCell']), Paragraph("81.5 %", styles['TableCell'])],
        [Paragraph("Weighted Logit Fusion", styles['TableCellBold']), Paragraph("0.8160", styles['TableCell']), Paragraph("81.8 %", styles['TableCell'])],
        [Paragraph("Uncertainty-Guided Fusion", styles['TableCellBold']), Paragraph("0.8120", styles['TableCell']), Paragraph("80.9 %", styles['TableCell'])],
        [Paragraph("<b>Multimodal Ensemble with TTA</b>", styles['TableCellBold']), Paragraph("<b>0.8198</b>", styles['TableCellBold']), Paragraph("<b>83.1 %</b>", styles['TableCellBold'])],
    ]
    t_bench = Table(bench_table_data, colWidths=[8.0*cm, 4.4*cm, 5.0*cm])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#ecfdf5")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 2*mm))

    fig_4_1 = get_image("page_11_img_2_FormXob.e20b1858cfdb66774c05f20575981e2b.png", width=12.5*cm, height=3.6*cm)
    story.append(fig_4_1)
    story.append(Paragraph("<b>Figure 4.1:</b> Comparison of reported ROC-AUC scores across configurations (axis truncated at 0.60).", styles['FigCaption']))
    story.append(Spacer(1, 1*mm))

    p_4_4_b = (
        "The ensemble outperforms standalone mammography by +0.0281 ROC-AUC and ultrasound by +0.1455; sensitivity increases from 76.2% to 83.1%. "
        "Variations between fusion methods remain modest and no formal significance test or confidence interval was documented in baseline logs."
    )
    story.append(Paragraph(p_4_4_b, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("4.5 Agentic Pipeline Audit and Case Study", styles['H2_Subtitle']))
    audit_table_data = [
        [Paragraph("<b>Audited Target</b>", styles['TableHead']),
         Paragraph("<b>Outcome</b>", styles['TableHead']),
         Paragraph("<b>Scope and Interpretation</b>", styles['TableHead'])],
        [Paragraph("Constructed Prompts", styles['TableCellBold']), Paragraph("190", styles['TableCell']), Paragraph("64 image-only; 62 text-only; 64 multimodal", styles['TableCell'])],
        [Paragraph("Adversarial Tests", styles['TableCellBold']), Paragraph("10 / 10", styles['TableCellBold']), Paragraph("Prompt injections and conflicting constraints neutralized", styles['TableCell'])],
        [Paragraph("Compliant on 1st Pass", styles['TableCellBold']), Paragraph("17 / 20", styles['TableCellBold']), Paragraph("3 reports corrected after first revision cycle (85% initial pass)", styles['TableCell'])],
        [Paragraph("n8n Executions", styles['TableCellBold']), Paragraph("23", styles['TableCell']), Paragraph("5 initial execution failures (21.7%) documented and resolved", styles['TableCell'])],
        [Paragraph("Mean Runtime", styles['TableCellBold']), Paragraph("5.54 s", styles['TableCell']), Paragraph("Standard n8n logger indicator across recorded runs", styles['TableCell'])],
        [Paragraph("Full Successful Run", styles['TableCellBold']), Paragraph("12.984 s", styles['TableCell']), Paragraph("Observed end-to-end execution including Grad-CAM and PDF", styles['TableCell'])],
        [Paragraph("pytest Test Suite", styles['TableCellBold']), Paragraph("61 / 61", styles['TableCellBold']), Paragraph("100% passed in 1.84 s within test environment", styles['TableCell'])],
    ]
    t_audit = Table(audit_table_data, colWidths=[4.2*cm, 2.6*cm, 10.6*cm])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.0),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 2*mm))

    p_case_study = (
        "<b>Case Study:</b> Pseudonymized patient <code>Paacb1ec57b</code> (bilateral mammography and targeted ultrasound) yields a prototype "
        "category of BI-RADS 3, p<sub>mal</sub> = 0.12, reported confidence of 78%, Shannon entropy H = 0.38 and 89.2% Grad-CAM activation energy "
        "inside the parenchymal mask. This illustrates a nominal output instance, requiring formal specialist sign-off."
    )
    story.append(Paragraph(p_case_study, styles['BodyEN']))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 12 : DISCUSSION, CONCLUSION & REFERENCES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4.6 Critical Discussion and Threats to Validity", styles['H2_Subtitle']))
    callout_discussion = (
        "<b>Structural Limitations:</b> • <b>Cohort:</b> 332 patients, class imbalance, 323 for multimodal comparison. "
        "• <b>Ground Truth:</b> Labels derived from BI-RADS annotations without independent histological validation. "
        "• <b>Generalization:</b> No multicentric external validation nor prospective trial. "
        "• <b>Comparisons:</b> No confidence intervals, statistical significance tests between fusions, nor LLM cross-benchmarking. "
        "• <b>XAI:</b> 12.6% of Grad-CAM attention energy resides outside segmented breast tissue. "
        "• <b>Integration:</b> 5 n8n failures out of 23; 3 out of 20 reports required active revision. "
        "• <b>Clinical Decision:</b> Score-to-BI-RADS mapping and entropy gating thresholds lack clinical validation."
    )
    story.append(build_callout(callout_discussion, "", styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("General Conclusion", styles['H1_Title']))
    p_conclusion_1 = (
        "The project integrates complementary scientific contributions: joint analysis of two medical imaging modalities, comparative evaluation "
        "of fusion strategies, XAI attention maps, a local dense vector documentary base and deterministic LLM output gating by independent rules. "
        "The system's core strength lies not in any isolated algorithm, but in the separation of responsibilities between vision prediction, knowledge retrieval, "
        "textual generation and deterministic safety verification."
    )
    p_conclusion_2 = (
        "Multimodal fusion achieves a higher ROC-AUC than either standalone modality (0.8198), Grad-CAM provides spatial visual evidence, RAG provides "
        "transparent access to normative excerpts, and reasoning/safety agents structure and verify the resulting clinical report.<br/><br/>"
        "<b>Perspectives:</b> External multi-hospital validation with independent pathology records; stability audit of n8n production workflows; "
        "quantitative benchmarking of RAG retrieval (Recall@4, citation accuracy); score calibration; and clinical review of triage rules prior to any clinical deployment. "
        "This contribution remains that of an academic research prototype, in which every output is traceable, all uncertainty disclosed, and all interpretation subject to human expertise."
    )
    story.append(Paragraph(p_conclusion_1, styles['BodyEN']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(p_conclusion_2, styles['BodyEN']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Bibliographical References", styles['H2_Subtitle']))
    references = [
        "[1] P. A. Carney et al. “Individual and Combined Effects of Age, Breast Density, and Hormone Replacement Therapy on the Accuracy of Screening Mammography”. <i>Annals of Internal Medicine</i> 138(3), 2003, pp. 168–175.",
        "[2] American College of Radiology. <i>ACR BI-RADS Atlas</i>, 5th ed. Reston, VA, 2013.",
        "[3] K. He, X. Zhang, S. Ren, J. Sun. “Deep Residual Learning for Image Recognition”. <i>CVPR</i>, 2016, pp. 770–778.",
        "[4] R. R. Selvaraju et al. “Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization”. <i>ICCV</i>, 2017, pp. 618–626.",
        "[5] J. Johnson, M. Douze, H. Jégou. “Billion-Scale Similarity Search with GPUs”. <i>IEEE Trans. Big Data</i> 7(3), 2021, pp. 535–547.",
        "[6] S. Xiao et al. <i>C-Pack: Packaged Resources to Advance General Chinese Embedding</i>. 2023. arXiv:2309.07597.",
        "[7] A. Yang et al. <i>Qwen2.5 Technical Report</i>. 2024. arXiv:2412.15115.",
        "[8] European Parliament and Council. Regulation (EU) 2017/745 on medical devices (MDR). <i>OJEU</i>, 2017."
    ]
    for ref in references:
        story.append(Paragraph(ref, ParagraphStyle('Ref', fontName='Helvetica', fontSize=7.2, leading=9.5, textColor=C_TEXT_DARK, spaceAfter=2)))

    doc.build(story, canvasmaker=TwelvePageCanvas)
    print(f"[OK] Generated English report: {OUTPUT_EN_PDF}")

    # Copy to grand technical report path as well
    import shutil
    shutil.copy2(OUTPUT_EN_PDF, OUTPUT_EN_GRAND_PDF)
    print(f"[OK] Copied to: {OUTPUT_EN_GRAND_PDF}")


if __name__ == "__main__":
    build_english_pdf()
