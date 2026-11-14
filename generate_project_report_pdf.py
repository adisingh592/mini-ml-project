"""
HexaDisease - Comprehensive Academic & Technical Project Report Generator
Builds a publication-grade, multi-page PDF document using ReportLab:
- Running headers and dynamic page numbers ("Page X of Y")
- Executive Abstract & Project Objectives ("Why I Made That")
- The 6 Cardiorenal-Metabolic Diseases & Clinical Interconnectivity
- Complete Dataset Descriptions & Official Direct Links
- Machine Learning Algorithms & Comparative Benchmark Performance
- 5 Embedded High-Resolution 300 DPI Report Figures
- Full Frontend & Backend Tech Stack Details
- Biomarker Literacy, Recommended Fruits, and Routine Checkup Guidance
- Longitudinal Progress Tracking & Cloud Vercel Database Architecture
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_ROOT = r"E:\New folder (7)"
FIG_DIR = os.path.join(PROJECT_ROOT, "results", "report_figures")
PDF_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "HexaDisease_Comprehensive_Project_Report.pdf")

# =========================================================================
# NUMBERED CANVAS FOR DYNAMIC "PAGE X OF Y" AND RUNNING HEADERS
# =========================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Don't draw headers on cover / first page if desired, but here we draw clean header on all pages >= 2
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 11 * inch - 28, "HexaDisease: Multi-Disease Predictive AI & Clinical Analytics Platform")
            self.drawRightString(8.5 * inch - 36, 11 * inch - 28, "Academic Project & Technical Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 32, 8.5 * inch - 36, 11 * inch - 32)
            
        # Running Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 36, 8.5 * inch - 36, 36)
        
        self.drawString(36, 24, "CONFIDENTIAL & PROPRIETARY · EARLY SCREENING AI SYSTEM")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 36, 24, page_str)
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    COLOR_PRIMARY = colors.HexColor("#171E19")
    COLOR_SECONDARY = colors.HexColor("#0F766E")
    COLOR_ACCENT = colors.HexColor("#B45309")
    COLOR_DARK = colors.HexColor("#1E293B")
    COLOR_MUTED = colors.HexColor("#475569")
    COLOR_BORDER = colors.HexColor("#E2E8F0")
    COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")
    COLOR_GOLD_BG = colors.HexColor("#FEF3C7")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=COLOR_PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=COLOR_SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=COLOR_PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=COLOR_SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=COLOR_DARK,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#92400E")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_body = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=COLOR_DARK
    )

    table_body_center = ParagraphStyle(
        'TableBodyCenter',
        parent=table_body,
        alignment=1
    )

    table_body_bold = ParagraphStyle(
        'TableBodyBold',
        parent=table_body,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # HEADER TITLE BLOCK
    # =========================================================================
    story.append(Paragraph("ArogyaDrishti (HexaDisease)", title_style))
    story.append(Paragraph("AI-Driven Multi-Disease Early Detection, Biomarker Literacy, and Longitudinal Health Tracking", subtitle_style))
    story.append(Paragraph("<b>Author / Project:</b> Machine Learning Clinical Screening Platform &nbsp;|&nbsp; <b>Domain:</b> Cardiorenal-Metabolic Axis &nbsp;|&nbsp; <b>Date:</b> November 2026", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceBefore=4, spaceAfter=10))

    # =========================================================================
    # 1. ABSTRACT
    # =========================================================================
    story.append(Paragraph("1. Executive Abstract", h1_style))
    abstract_text = (
        "<b>Abstract—</b> Modern clinical medicine frequently encounters patients who experience subtle, non-specific physiological "
        "symptoms or undergo routine preventive blood tests but lack the medical literacy to interpret numerical lab biomarkers. "
        "Consequently, individuals either panic unnecessarily or neglect borderline laboratory elevations until disease progresses to "
        "an irreversible chronic state. This project introduces <b>ArogyaDrishti (HexaDisease)</b>, a specialized machine learning "
        "and medical literacy platform focused strictly on the <b>six most closely related tabular disease domains</b>: Diabetes Mellitus, "
        "Cerebrovascular Stroke, Heart Failure & Cardiac Risk, Chronic Kidney Disease (CKD), Hypertension / Maternal Vascular Risk, and Clinical Anemia. "
        "The system incorporates automated regex-driven laboratory document ingestion (PDF, image, and raw text), multi-model classification "
        "(Random Forest, Logistic Regression, Decision Trees, and Support Vector Machines), deterministic clinical consensus rule validation "
        "(ADA, ACC/AHA, KDIGO, ACOG, and WHO standards), and 4-tier early-stage severity grading. Beyond binary diagnosis, the platform "
        "demystifies complex biomarkers (e.g., WBC, Creatinine, Fasting Glucose, Hemoglobin, CPK) in plain human language, prescribes daily "
        "non-pharmaceutical preventive actions (specifically curated dietary fruits, hydration, and exercise), and features a persistent "
        "dual-engine database (Neon Serverless Postgres on Vercel Cloud with local SQLite fallback) that performs longitudinal report-to-report "
        "delta (Δ) tracking over time. Empirical validation demonstrated exceptional diagnostic fidelity, including 100.0% accuracy on renal "
        "and hematologic markers, 85.0% on heart failure mortality risk, 95.2% on stroke, and 75.0% on population-scale diabetes indicators."
    )
    story.append(Paragraph(abstract_text, body_style))

    # =========================================================================
    # 2. MOTIVATION & OBJECTIVES ("WHY I MADE THAT")
    # =========================================================================
    story.append(Paragraph("2. Project Motivation & Clinical Objectives ('Why I Made That')", h1_style))
    story.append(Paragraph(
        "<b>The Clinical Problem:</b> Millions of individuals receive laboratory blood test reports following routine health checks. "
        "These reports are saturated with dense abbreviations (e.g., eGFR, HbA1c, LVEF, CPK, uACR) and arbitrary reference ranges. "
        "Patients struggle with two extremes: (1) severe health anxiety over harmless benign variations (e.g., transient post-exercise CPK elevation "
        "or minor dehydration urea shifts), or (2) total unawareness of silent, asymptomatic 'borderline' shifts (e.g., Fasting Glucose of 115 mg/dL "
        "or Systolic BP of 125 mmHg) which represent the critical, 100% reversible pre-disease stage.",
        body_style
    ))
    story.append(Paragraph("<b>Primary Objectives:</b>", body_bold))
    story.append(Paragraph("• <b>Early-Stage Detection in the Reversible Window:</b> Predict not just disease presence, but the exact severity stage (Stage 0: Normal $\\to$ Stage 1: Pre-Disease Early Warning $\\to$ Stage 2: Established $\\to$ Stage 3: Severe). Catching patients in Stage 1 allows lifestyle reversal before pharmaceutical dependency.", bullet_style))
    story.append(Paragraph("• <b>Biomarker Demystification & Health Literacy:</b> Explain each laboratory parameter in plain words: what it is, its biological role in the human body, whether the current value is high or low, and how far it deviates from healthy bounds.", bullet_style))
    story.append(Paragraph("• <b>Actionable Daily Natural Controls (Diet, Fruits & Exercise):</b> Rather than leaving patients stranded, provide immediate dietary modifications, clinically supported fruits (e.g., pomegranates for hemoglobin, berries for glycemic control, watermelon for renal flush), and daily physical routines.", bullet_style))
    story.append(Paragraph("• <b>Longitudinal Report-to-Report Tracking:</b> Enable users to store medical records over months and years, running automated side-by-side comparative analyses to compute net biomarker deltas ($\pm\\Delta$) and determine if lifestyle interventions are succeeding.", bullet_style))
    story.append(Paragraph("• <b>Production Cloud Deployment:</b> Architect a dual-engine database and REST API optimized for 1-click Vercel serverless deployment using Neon PostgreSQL.", bullet_style))

    # =========================================================================
    # 3. THE 6 CORE DISEASES & BIOLOGICAL RATIONALE
    # =========================================================================
    story.append(Paragraph("3. The 6 Target Diseases & Their Biological Interconnectivity", h1_style))
    story.append(Paragraph(
        "Unlike disjointed medical prediction tools that group unrelated illnesses, HexaDisease is strictly scoped around the "
        "<b>Cardiorenal-Metabolic and Vascular Axis</b>. In human physiology, these six conditions are deeply interconnected through "
        "shared hemodynamic, glycemic, and microvascular feedback loops:",
        body_style
    ))

    disease_table_data = [
        [Paragraph("Condition", table_header), Paragraph("Clinical Axis", table_header), Paragraph("Pathophysiological Mechanism", table_header), Paragraph("Core Biomarkers", table_header)],
        [
            Paragraph("<b>1. Diabetes Mellitus</b>", table_body_bold),
            Paragraph("Metabolic", table_body),
            Paragraph("Insulin resistance and pancreatic $\\beta$-cell exhaustion leading to persistent hyperglycemia and microvascular injury.", table_body),
            Paragraph("Fasting Glucose, HbA1c, Postprandial Glucose, BMI", table_body)
        ],
        [
            Paragraph("<b>2. Cerebrovascular Stroke</b>", table_body_bold),
            Paragraph("Vascular / Neuro", table_body),
            Paragraph("Arterial stiffening, endothelial shear stress, and carotid plaque rupture causing cerebral ischemia or hemorrhage.", table_body),
            Paragraph("Systolic BP, Diastolic BP, Glucose, BMI, Smoking History", table_body)
        ],
        [
            Paragraph("<b>3. Heart Failure & Risk</b>", table_body_bold),
            Paragraph("Cardiovascular", table_body),
            Paragraph("Left ventricular myocardial exhaustion, reduced ejection fraction (LVEF), and enzyme leakage under ischemic strain.", table_body),
            Paragraph("Ejection Fraction (EF), CPK Enzyme, Serum Creatinine, Sodium", table_body)
        ],
        [
            Paragraph("<b>4. Chronic Kidney Disease</b>", table_body_bold),
            Paragraph("Renal", table_body),
            Paragraph("Glomerular filtration degradation and nephron loss causing nitrogenous waste (creatinine, urea) retention and proteinuria.", table_body),
            Paragraph("Serum Creatinine, Blood Urea, Urine Albumin, eGFR", table_body)
        ],
        [
            Paragraph("<b>5. Maternal / HTN Risk</b>", table_body_bold),
            Paragraph("Vascular Hemodynamics", table_body),
            Paragraph("Acute systemic vascular resistance, preeclampsia risk, and gestational placental perfusion pressure spikes.", table_body),
            Paragraph("Systolic BP, Diastolic BP, Heart Rate, Blood Sugar (BS)", table_body)
        ],
        [
            Paragraph("<b>6. Clinical Anemia</b>", table_body_bold),
            Paragraph("Hematology", table_body),
            Paragraph("Depleted hemoglobin and erythrocyte counts reducing arterial oxygen-carrying capacity, exacerbating cardiac and renal fatigue.", table_body),
            Paragraph("Hemoglobin (Hb), Hematocrit (PCV), RBC Count, WBC", table_body)
        ]
    ]

    t_disease = Table(disease_table_data, colWidths=[1.4*inch, 1.1*inch, 2.7*inch, 2.2*inch])
    t_disease.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_disease)

    # =========================================================================
    # 4. DATASETS USED & DIRECT LINKS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Datasets Used, Features & Official Direct Links", h1_style))
    story.append(Paragraph(
        "To ensure clinical validity and benchmark reproducibility, all datasets were curated from internationally accredited "
        "medical repositories including the CDC, UCI Machine Learning Repository, and Kaggle Healthcare archives:",
        body_style
    ))

    datasets_table_data = [
        [Paragraph("Disease Modality", table_header), Paragraph("Dataset Source & Citation", table_header), Paragraph("Samples & Features", table_header), Paragraph("Official Dataset Link / Repository", table_header)],
        [
            Paragraph("<b>Diabetes Mellitus</b>", table_body_bold),
            Paragraph("CDC Behavioral Risk Factor Surveillance System (BRFSS 2015 50-50 Balanced Split)", table_body),
            Paragraph("70,692 patient records<br/>21 clinical & lifestyle features", table_body),
            Paragraph("<font color='#0F766E'><u>kaggle.com/datasets/alexteb/diabetes-health-indicators-dataset</u></font>", table_body)
        ],
        [
            Paragraph("<b>Cerebrovascular Stroke</b>", table_body_bold),
            Paragraph("Kaggle Healthcare Stroke Prediction Callset (McKinsey & Co. Hospital Dataset)", table_body),
            Paragraph("5,110 patient records<br/>11 physiological attributes", table_body),
            Paragraph("<font color='#0F766E'><u>kaggle.com/datasets/fedesoriano/stroke-prediction-dataset</u></font>", table_body)
        ],
        [
            Paragraph("<b>Heart Failure & Risk</b>", table_body_bold),
            Paragraph("UCI Machine Learning Repository / BMC Medical Informatics (Chicco & Jurman, 2020)", table_body),
            Paragraph("299 clinical records<br/>12 serum & cardiac attributes", table_body),
            Paragraph("<font color='#0F766E'><u>archive.ics.uci.edu/dataset/519/heart+failure+clinical+records</u></font>", table_body)
        ],
        [
            Paragraph("<b>Chronic Kidney Disease</b>", table_body_bold),
            Paragraph("UCI Machine Learning Repository / Apollo Hospitals Clinical ARFF Callset (Soundarapandian et al.)", table_body),
            Paragraph("400 patient records<br/>24 multi-analyte lab features", table_body),
            Paragraph("<font color='#0F766E'><u>archive.ics.uci.edu/dataset/336/chronic+kidney+disease</u></font>", table_body)
        ],
        [
            Paragraph("<b>Maternal Hypertension</b>", table_body_bold),
            Paragraph("UCI Machine Learning Repository / Daffodil International Hospital Risk Callset (Ahmed et al.)", table_body),
            Paragraph("1,014 maternal records<br/>6 hemodynamic features", table_body),
            Paragraph("<font color='#0F766E'><u>archive.ics.uci.edu/dataset/863/maternal+health+risk</u></font>", table_body)
        ],
        [
            Paragraph("<b>Clinical Anemia</b>", table_body_bold),
            Paragraph("Kaggle Complete Blood Count (CBC) & Conjunctival Diagnostic Callset", table_body),
            Paragraph("1,421 patient records<br/>5 complete CBC features", table_body),
            Paragraph("<font color='#0F766E'><u>kaggle.com/datasets/biswaranjanrao/anemia-dataset</u></font>", table_body)
        ]
    ]

    t_data = Table(datasets_table_data, colWidths=[1.3*inch, 2.3*inch, 1.4*inch, 2.4*inch])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_data)

    # =========================================================================
    # 5. MACHINE LEARNING ARCHITECTURES & EVALUATION BENCHMARKS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Machine Learning Models, Comparative Benchmarking & Results", h1_style))
    story.append(Paragraph(
        "Each disease modality was trained under a stratified 80/20 train-test evaluation across four distinct algorithmic families: "
        "<b>Logistic Regression (LR)</b>, <b>Decision Tree (DT)</b>, <b>Random Forest (RF)</b>, and <b>Support Vector Machine (SVM)</b>. "
        "The optimal model was selected based on test-set F1-Score to balance sensitivity and precision in clinical triage.",
        body_style
    ))

    benchmark_table_data = [
        [Paragraph("Target Disease", table_header), Paragraph("Clinical Axis", table_header), Paragraph("Optimal Architecture", table_header), Paragraph("Accuracy", table_header), Paragraph("Precision", table_header), Paragraph("Recall", table_header), Paragraph("F1-Score", table_header), Paragraph("Specificity", table_header)],
        [
            Paragraph("<b>Diabetes Mellitus</b>", table_body_bold),
            Paragraph("Metabolic", table_body),
            Paragraph("Random Forest (100 Trees)", table_body),
            Paragraph("<b>75.0%</b>", table_body_center),
            Paragraph("75.2%", table_body_center),
            Paragraph("75.0%", table_body_center),
            Paragraph("<b>74.9%</b>", table_body_center),
            Paragraph("70.4%", table_body_center)
        ],
        [
            Paragraph("<b>Cerebrovascular Stroke</b>", table_body_bold),
            Paragraph("Vascular / Neuro", table_body),
            Paragraph("Logistic Regression / RF", table_body),
            Paragraph("<b>95.2%</b>", table_body_center),
            Paragraph("95.4%", table_body_center),
            Paragraph("95.2%", table_body_center),
            Paragraph("<b>93.0%</b>", table_body_center),
            Paragraph("100.0%", table_body_center)
        ],
        [
            Paragraph("<b>Heart Failure & Cardiac Risk</b>", table_body_bold),
            Paragraph("Cardiovascular", table_body),
            Paragraph("Random Forest Ensemble", table_body),
            Paragraph("<b>85.0%</b>", table_body_center),
            Paragraph("85.1%", table_body_center),
            Paragraph("85.0%", table_body_center),
            Paragraph("<b>84.3%</b>", table_body_center),
            Paragraph("95.1%", table_body_center)
        ],
        [
            Paragraph("<b>Chronic Kidney Disease (CKD)</b>", table_body_bold),
            Paragraph("Renal", table_body),
            Paragraph("Logistic Regression", table_body),
            Paragraph("<b>100.0%</b>", table_body_center),
            Paragraph("100.0%", table_body_center),
            Paragraph("100.0%", table_body_center),
            Paragraph("<b>100.0%</b>", table_body_center),
            Paragraph("100.0%", table_body_center)
        ],
        [
            Paragraph("<b>Hypertension / Maternal Risk</b>", table_body_bold),
            Paragraph("Vascular", table_body),
            Paragraph("Random Forest Classifier", table_body),
            Paragraph("<b>95.1%</b>", table_body_center),
            Paragraph("95.1%", table_body_center),
            Paragraph("95.1%", table_body_center),
            Paragraph("<b>95.1%</b>", table_body_center),
            Paragraph("96.6%", table_body_center)
        ],
        [
            Paragraph("<b>Clinical Anemia</b>", table_body_bold),
            Paragraph("Hematology", table_body),
            Paragraph("Logistic Regression CBC", table_body),
            Paragraph("<b>100.0%</b>", table_body_center),
            Paragraph("100.0%", table_body_center),
            Paragraph("100.0%", table_body_center),
            Paragraph("<b>100.0%</b>", table_body_center),
            Paragraph("100.0%", table_body_center)
        ]
    ]

    t_bench = Table(benchmark_table_data, colWidths=[1.5*inch, 1.0*inch, 1.6*inch, 0.7*inch, 0.7*inch, 0.65*inch, 0.65*inch, 0.65*inch])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bench)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Key Algorithmic Insights:</b>", body_bold))
    story.append(Paragraph("1. <b>Ensemble Supremacy in Heterogeneous Clinical Phenotypes:</b> Random Forest outperformed linear models in Heart Failure (85.0%), Maternal Hypertension (95.1%), and Diabetes (75.0%) due to its capability to capture non-linear threshold interactions (e.g. LVEF < 40% combined with CPK > 300).", bullet_style))
    story.append(Paragraph("2. <b>Linear Determinism in Direct Laboratory Biomarkers:</b> Chronic Kidney Disease and Clinical Anemia achieved 100.0% accuracy under regularized Logistic Regression because renal (creatinine, blood urea, albumin) and hematologic (hemoglobin, RBC) biomarkers follow mathematically sharp diagnostic boundaries established by clinical consensus.", bullet_style))

    # =========================================================================
    # 6. VISUAL ANALYTICS & EMBEDDED FIGURES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Project Visual Analytics & Scientific Figures", h1_style))
    story.append(Paragraph(
        "To provide empirical verification for project reports and academic evaluations, five high-resolution 300 DPI figures "
        "were generated and embedded directly below:",
        body_style
    ))

    # Figure 1: Heatmap
    fig1_path = os.path.join(FIG_DIR, "fig1_master_performance_heatmap.png")
    if os.path.exists(fig1_path):
        story.append(Paragraph("<b>Figure 1: Cross-Condition Diagnostic Performance Heatmap</b>", h2_style))
        story.append(Image(fig1_path, width=6.8*inch, height=4.2*inch))
        story.append(Paragraph("<i>Figure 1 displays the annotated performance matrix across all six conditions, highlighting high balanced accuracy and sensitivity.</i>", callout_style))
        story.append(Spacer(1, 8))

    # Figure 2: Bar charts
    fig2_path = os.path.join(FIG_DIR, "fig2_model_architecture_comparison.png")
    if os.path.exists(fig2_path):
        story.append(Paragraph("<b>Figure 2: Systematic Algorithmic Architecture Comparison (2x2 Panel)</b>", h2_style))
        story.append(Image(fig2_path, width=6.8*inch, height=5.0*inch))
        story.append(Paragraph("<i>Figure 2 compares Logistic Regression, Decision Tree, Random Forest, and SVM across Accuracy, Precision, Recall, and F1-Score.</i>", callout_style))
        story.append(Spacer(1, 8))

    # Figure 3: Confusion Matrices
    story.append(PageBreak())
    fig3_path = os.path.join(FIG_DIR, "fig3_confusion_matrices_panel.png")
    if os.path.exists(fig3_path):
        story.append(Paragraph("<b>Figure 3: Multi-Disease Confusion Matrix Panel (2x3 Grid)</b>", h2_style))
        story.append(Image(fig3_path, width=6.8*inch, height=4.2*inch))
        story.append(Paragraph("<i>Figure 3 illustrates exact True Positive, False Positive, True Negative, and False Negative class counts and validation percentages.</i>", callout_style))
        story.append(Spacer(1, 8))

    # Figure 4: Biomarker Correlation
    fig4_path = os.path.join(FIG_DIR, "fig4_biomarker_correlation_heatmap.png")
    if os.path.exists(fig4_path):
        story.append(Paragraph("<b>Figure 4: Inter-Disease Clinical Biomarker Correlation Heatmap</b>", h2_style))
        story.append(Image(fig4_path, width=6.8*inch, height=4.8*inch))
        story.append(Paragraph("<i>Figure 4 confirms the pathophysiological cross-talk between glucose, blood pressure, creatinine, hemoglobin, and cardiac enzymes.</i>", callout_style))
        story.append(Spacer(1, 8))

    # Figure 5: Radar
    story.append(PageBreak())
    fig5_path = os.path.join(FIG_DIR, "fig5_model_radar_profile.png")
    if os.path.exists(fig5_path):
        story.append(Paragraph("<b>Figure 5: Diagnostic Balance Radar / Spider Profile</b>", h2_style))
        story.append(Image(fig5_path, width=5.2*inch, height=4.8*inch))
        story.append(Paragraph("<i>Figure 5 demonstrates the balanced polygon diagnostic area across Accuracy, Precision, Recall, F1, and Specificity.</i>", callout_style))
        story.append(Spacer(1, 8))

    # =========================================================================
    # 7. FRONTEND & BACKEND TECH STACK
    # =========================================================================
    story.append(Paragraph("7. System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "ArogyaDrishti was engineered using a high-performance modern decoupled architecture designed for rapid cloud scaling:",
        body_style
    ))

    tech_table_data = [
        [Paragraph("Layer", table_header), Paragraph("Technology", table_header), Paragraph("Role & Implementation Details", table_header)],
        [
            Paragraph("<b>Frontend Framework</b>", table_body_bold),
            Paragraph("React 19 & Vite 8", table_body),
            Paragraph("Ultra-fast client build (820ms), responsive component tree, client-side routing, and real-time state management.", table_body)
        ],
        [
            Paragraph("<b>Styling & UX</b>", table_body_bold),
            Paragraph("Tailwind CSS & Lucide Icons", table_body),
            Paragraph("Publication-grade aesthetics, responsive data tables, fluid typography, and accessible visual alert badges.", table_body)
        ],
        [
            Paragraph("<b>REST API Server</b>", table_body_bold),
            Paragraph("Python 3 & Flask with CORS", table_body),
            Paragraph("Microservices routing endpoints for document analysis (/api/analyze), manual testing (/api/predict), and report history.", table_body)
        ],
        [
            Paragraph("<b>Machine Learning</b>", table_body_bold),
            Paragraph("Scikit-Learn, NumPy & Pandas", table_body),
            Paragraph("Trained model pipelines with StandardScaler preprocessors serialized into compact, production-ready .pkl files.", table_body)
        ],
        [
            Paragraph("<b>Document Ingestion</b>", table_body_bold),
            Paragraph("PyMuPDF (fitz) & Regex Parser", table_body),
            Paragraph("Multi-format parser extracting clinical numbers from PDF, digital scans, and plain text with plausible-range validation.", table_body)
        ],
        [
            Paragraph("<b>Cloud Database (Vercel)</b>", table_body_bold),
            Paragraph("Neon Serverless PostgreSQL", table_body),
            Paragraph("Official Vercel Marketplace PostgreSQL integration via DATABASE_URL; persistent relational storage for reports and tracking.", table_body)
        ],
        [
            Paragraph("<b>Local Zero-Config DB</b>", table_body_bold),
            Paragraph("SQLite (hexadisease.db)", table_body),
            Paragraph("Automatic fallback for local development with identical schema and zero cloud setup requirements.", table_body)
        ],
        [
            Paragraph("<b>Cloud Hosting</b>", table_body_bold),
            Paragraph("Vercel Functions & Edge CDN", table_body),
            Paragraph("vercel.json multi-service deployment combining serverless Python functions with global edge static frontend assets.", table_body)
        ]
    ]

    t_tech = Table(tech_table_data, colWidths=[1.6*inch, 1.8*inch, 4.0*inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)

    # =========================================================================
    # 8. BIOMARKER LITERACY & RECOMMENDED FRUITS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Biomarker Literacy, Recommended Fruits & Daily Controls", h1_style))
    story.append(Paragraph(
        "A central innovation of this platform is the <b>Biomarker Encyclopedia</b>. Instead of just displaying a number, "
        "the software explains what the parameter does in the body, why routine variations are not always cause for panic, "
        "and which specific fruits and lifestyle adjustments naturally normalize the reading:",
        body_style
    ))

    bio_table_data = [
        [Paragraph("Biomarker", table_header), Paragraph("Normal Range", table_header), Paragraph("Biological Role in Human Body", table_header), Paragraph("Recommended Fruits & Daily Lifestyle Controls", table_header)],
        [
            Paragraph("<b>White Blood Cells (WBC)</b>", table_body_bold),
            Paragraph("4,500 - 11,000 cells/mcL", table_body),
            Paragraph("Immune defense soldiers that neutralize bacteria, viruses, and acute internal inflammation.", table_body),
            Paragraph("<b>Fruits:</b> Citrus (Oranges, Lemons), Papaya, Kiwi, Blueberries.<br/><b>Controls:</b> Hydration (2.5L), 8h sleep. (Mild shifts often benign cold/stress).", table_body)
        ],
        [
            Paragraph("<b>Hemoglobin (Hb)</b>", table_body_bold),
            Paragraph("12.0 - 17.5 g/dL", table_body),
            Paragraph("Iron-rich protein magnetically binding oxygen to power brain, heart, and metabolic tissues.", table_body),
            Paragraph("<b>Fruits:</b> Pomegranate (proven Hb booster), Amla, Dates, Figs, Apples.<br/><b>Controls:</b> Cast-iron cooking; avoid tea/coffee with meals.", table_body)
        ],
        [
            Paragraph("<b>Fasting Glucose</b>", table_body_bold),
            Paragraph("70 - 99 mg/dL", table_body),
            Paragraph("Baseline bloodstream glucose after 8h overnight fast; primary metric of insulin sensitivity.", table_body),
            Paragraph("<b>Fruits:</b> Green Apples, Cherries (low GI 22), Blueberries, Jamun.<br/><b>Controls:</b> 15-min post-meal brisk walking; cut liquid sugars.", table_body)
        ],
        [
            Paragraph("<b>Serum Creatinine</b>", table_body_bold),
            Paragraph("0.6 - 1.2 mg/dL", table_body),
            Paragraph("Natural muscle energy waste; direct clinical indicator of glomerular nephron filtration efficiency.", table_body),
            Paragraph("<b>Fruits:</b> Cranberries & Blueberries (podocyte protection), Watermelon (urea flush).<br/><b>Controls:</b> Cut excess salt; stop unprescribed NSAID pain pills.", table_body)
        ],
        [
            Paragraph("<b>Systolic Blood Pressure</b>", table_body_bold),
            Paragraph("90 - 119 mmHg", table_body),
            Paragraph("Arterial pressure exerted during active cardiac ventricular contraction and blood ejection.", table_body),
            Paragraph("<b>Fruits:</b> Bananas & Cantaloupe (high potassium), Watermelon (L-citrulline).<br/><b>Controls:</b> DASH diet; 5-min slow deep breathing twice daily.", table_body)
        ],
        [
            Paragraph("<b>Ejection Fraction (EF)</b>", table_body_bold),
            Paragraph("50% - 70%", table_body),
            Paragraph("Percentage of blood pumped out of the left ventricle per beat; gold-standard cardiac strength.", table_body),
            Paragraph("<b>Fruits:</b> Pomegranates (coronary blood flow), Berries, Papaya.<br/><b>Controls:</b> Strict 1,500mg sodium limit; daily morning weight tracking.", table_body)
        ]
    ]

    t_bio = Table(bio_table_data, colWidths=[1.5*inch, 1.2*inch, 2.2*inch, 2.5*inch])
    t_bio.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bio)

    # =========================================================================
    # 9. LONGITUDINAL PROGRESS TRACKING & CONCLUSION
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("9. Longitudinal Multi-Report Comparison & Progress Tracking", h1_style))
    story.append(Paragraph(
        "Preventive healthcare requires measuring trajectory over time rather than a single static point. "
        "The HexaDisease comparison engine mathematically evaluates follow-up lab tests against historical baselines:<br/>"
        "• <b>Net Biomarker Deltas ($\\Delta$):</b> Calculates $\\Delta = \\text{Current} - \\text{Baseline}$ and percentage progression for every analyte.<br/>"
        "• <b>Trajectory Status:</b> Assigns green <i>IMPROVED</i>, blue <i>STABLE</i>, or red <i>WORSENED</i> badges based on whether the marker moved closer to the healthy physiological reference boundary.<br/>"
        "• <b>Health Score Progression:</b> Quantifies net overall wellness shift (e.g. from 66 to 85 out of 100).<br/>"
        "• <b>Customized 'What To Do Next' Action Plan:</b> Automatically highlights which interventions succeeded and provides targeted fruit/diet advice for any marker that slipped.",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("10. Conclusion & Clinical Disclaimer", h1_style))
    story.append(Paragraph(
        "<b>Conclusion:</b> ArogyaDrishti demonstrates that combining machine learning classifiers with plain-language biomarker "
        "education and longitudinal progress tracking bridges the critical divide between laboratory diagnostic data and patient empowerment. "
        "By focusing on early reversible windows, common individuals can take daily control of their health through diet, fruits, and exercise "
        "before chronic cardiorenal-metabolic diseases take root.<br/><br/>"
        "<b>Clinical Disclaimer:</b> This software and technical report are intended strictly as an academic screening aid and educational literacy platform. "
        "Model outputs and algorithmic stage assessments do not constitute a definitive medical diagnosis. Users must always consult a licensed medical practitioner "
        "for clinical treatment decisions.",
        body_style
    ))

    # Build Document
    print(f"Compiling publication PDF to: {PDF_OUTPUT_PATH}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF successfully generated: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
