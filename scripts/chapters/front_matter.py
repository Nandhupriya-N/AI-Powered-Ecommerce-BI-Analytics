import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_front_matter(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    set_cell_background = helpers['set_cell_background']
    set_cell_margins = helpers['set_cell_margins']

    # ==========================================
    # 1. TITLE / COVER PAGE
    # ==========================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(0)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("VISVESVARAYA TECHNOLOGICAL UNIVERSITY")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_after = Pt(10)
    r = p_loc.add_run("“Jnana Sangama”, Belagavi - 590018, Karnataka")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.35))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(4)
    r = p_rep.add_run("A Project Work (MPRJ384) Phase-1 Report on")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.italic = True

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(10)
    r = p_tit.add_run("AI-POWERED E-COMMERCE BUSINESS INTELLIGENCE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_after = Pt(12)
    r = p_subm.add_run(
        "Submitted in partial fulfillment of the requirements for the award of the degree of\n"
        "MASTER OF COMPUTER APPLICATIONS"
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.bold = True

    table_creds = doc.add_table(rows=1, cols=2)
    table_creds.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_creds.autofit = False
    table_creds.columns[0].width = Inches(3.2)
    table_creds.columns[1].width = Inches(3.2)

    cell_l = table_creds.cell(0, 0)
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_l.add_run("Submitted By:\n\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(10.5); r.font.italic = True
    r2 = p_l.add_run("NANDHUPRIYA N\n")
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(11.5); r2.font.bold = True
    r3 = p_l.add_run("USN: 1RV24MC059")
    r3.font.name = 'Times New Roman'; r3.font.size = Pt(10.5); r3.font.bold = True

    cell_r = table_creds.cell(0, 1)
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_r.add_run("Under the Guidance of:\n\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(10.5); r.font.italic = True
    r2 = p_r.add_run("Prof. Preethi S\n")
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(11.5); r2.font.bold = True
    r3 = p_r.add_run("Assistant Professor, Dept. of MCA\nRVITM, Bengaluru")
    r3.font.name = 'Times New Roman'; r3.font.size = Pt(10.5)

    p_dep = doc.add_paragraph()
    p_dep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dep.paragraph_format.space_before = Pt(14)
    p_dep.paragraph_format.space_after = Pt(2)
    r = p_dep.add_run("DEPARTMENT OF MASTER OF COMPUTER APPLICATIONS\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(11.5); r.font.bold = True
    r2 = p_dep.add_run("RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT ®\n")
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(12.5); r2.font.bold = True
    r3 = p_dep.add_run("(Affiliated to Visvesvaraya Technological University, Belagavi)\nChikkakallasandra, Bengaluru – 560076\n2026-2027")
    r3.font.name = 'Times New Roman'; r3.font.size = Pt(10.5)

    doc.add_page_break()

    # ==========================================
    # 2. CERTIFICATE PAGE
    # ==========================================
    p_cert_hdr = doc.add_paragraph()
    p_cert_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_hdr.paragraph_format.space_after = Pt(2)
    r = p_cert_hdr.add_run("RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT ®\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(12.5); r.font.bold = True
    r2 = p_cert_hdr.add_run("Chikkakallasandra, Bengaluru – 560076\n")
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(10.5)
    r3 = p_cert_hdr.add_run("Department of Master of Computer Applications\n")
    r3.font.name = 'Times New Roman'; r3.font.size = Pt(11.5); r3.font.bold = True

    add_styled_heading(doc, "CERTIFICATE", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=10)

    add_body_p(doc,
        "This is to certify that the Project Work (MPRJ384) Phase-1 entitled “AI-Powered E-Commerce Business Intelligence” "
        "is a bonafide work carried out by NANDHUPRIYA N (USN: 1RV24MC059), a bonafide student of RV Institute of Technology and Management, "
        "Bengaluru, in partial fulfillment for the award of the degree of Master of Computer Applications of Visvesvaraya "
        "Technological University, Belagavi during the academic year 2026-2027. It is certified that all corrections and suggestions "
        "indicated for internal assessment have been incorporated in the report. The project report has been approved as it "
        "satisfies the academic requirements prescribed for the degree.",
        space_after=4, line_spacing=1.35)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(30)
    p_sig.paragraph_format.space_after = Pt(20)

    t_sig = doc.add_table(rows=1, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.columns[0].width = Inches(2.1)
    t_sig.columns[1].width = Inches(2.1)
    t_sig.columns[2].width = Inches(2.1)

    c0 = t_sig.cell(0, 0).paragraphs[0]
    c0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c0.add_run("_____________________\nProf. Preethi S\nInternal Guide\nAssistant Professor, Dept. of MCA\nRVITM, Bengaluru")
    r.font.name = 'Times New Roman'; r.font.size = Pt(9.5)

    c1 = t_sig.cell(0, 1).paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c1.add_run("_____________________\nHead of Department\nDept. of MCA\nRVITM, Bengaluru")
    r.font.name = 'Times New Roman'; r.font.size = Pt(9.5)

    c2 = t_sig.cell(0, 2).paragraphs[0]
    c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c2.add_run("_____________________\nDr. Malini M Patil\nPrincipal\nRVITM, Bengaluru")
    r.font.name = 'Times New Roman'; r.font.size = Pt(9.5)

    add_styled_heading(doc, "External Viva-Voce Examination:", 2, font_size=11, bold=True, space_before=16, space_after=6)
    p_viva = doc.add_paragraph()
    p_viva.paragraph_format.line_spacing = 1.3
    r = p_viva.add_run("1. Name of Examiner 1: ____________________________    Signature with Date: ____________________\n\n"
                       "2. Name of Examiner 2: ____________________________    Signature with Date: ____________________")
    r.font.name = 'Times New Roman'; r.font.size = Pt(10)

    doc.add_page_break()

    # ==========================================
    # 3. DECLARATION PAGE
    # ==========================================
    add_styled_heading(doc, "DECLARATION", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=12)

    add_body_p(doc,
        "I, NANDHUPRIYA N (USN: 1RV24MC059), student of 3rd Semester, Department of Master of Computer Applications, "
        "RV Institute of Technology and Management, Bengaluru, hereby declare that the Project Work (MPRJ384) Phase-1 "
        "entitled “AI-Powered E-Commerce Business Intelligence” has been independently carried out by me under the guidance of "
        "Prof. Preethi S, Assistant Professor, Department of Master of Computer Applications, RVITM, Bengaluru, in partial "
        "fulfillment of the requirements for the award of the degree of Master of Computer Applications by Visvesvaraya "
        "Technological University, Belagavi during the academic year 2026-2027.",
        space_after=8, line_spacing=1.4)

    add_body_p(doc,
        "I further declare that this report has not been submitted previously to any other university or institution for the award "
        "of any degree, diploma, or other similar academic recognition, and that the analytical models, system architectures, and "
        "evaluation experiments presented herein represent my own authentic work.",
        space_after=8, line_spacing=1.4)

    p_d_sig = doc.add_paragraph()
    p_d_sig.paragraph_format.space_before = Pt(36)
    p_d_sig.paragraph_format.space_after = Pt(4)
    r = p_d_sig.add_run("Date: ____________________\nPlace: Bengaluru\n\n\n\n_________________________________\nNANDHUPRIYA N\n(USN: 1RV24MC059)")
    r.font.name = 'Times New Roman'; r.font.size = Pt(10.5); r.font.bold = True

    doc.add_page_break()

    # ==========================================
    # 4. ACKNOWLEDGEMENT PAGE
    # ==========================================
    add_styled_heading(doc, "ACKNOWLEDGEMENT", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=12)

    add_body_p(doc,
        "The completion of this Phase-1 project work entitled “AI-Powered E-Commerce Business Intelligence” gives me immense "
        "pleasure, and I take this opportunity to express my profound gratitude to everyone who supported and guided me throughout this journey.",
        space_after=4, line_spacing=1.35)

    add_body_p(doc,
        "I take this opportunity to express my profound gratitude to the Management of RV Institute of Technology and Management, "
        "Bengaluru, for providing excellent academic infrastructure, state-of-the-art laboratory facilities, and a supportive learning environment.",
        space_after=4, line_spacing=1.35)

    add_body_p(doc,
        "I convey my sincere regards and heartfelt thanks to our respected Principal, Dr. Malini M Patil, RV Institute of Technology and Management, "
        "for her constant encouragement, administrative support, and motivation to strive for academic excellence.",
        space_after=4, line_spacing=1.35)

    add_body_p(doc,
        "I express my deepest gratitude to our beloved Head of the Department, Department of Master of Computer Applications, "
        "for continuous academic support, encouragement, and for providing the necessary facilities to successfully conduct our project research.",
        space_after=4, line_spacing=1.35)

    add_body_p(doc,
        "I am deeply indebted to my internal guide, Prof. Preethi S, Assistant Professor, Department of Master of Computer Applications, "
        "for her valuable guidance, constructive feedback, insightful suggestions, and continuous encouragement throughout the design "
        "and development of this project. Her technical expertise helped me refine both the predictive analytics models and the system architecture.",
        space_after=4, line_spacing=1.35)

    add_body_p(doc,
        "Finally, I express my sincere appreciation to all the faculty and staff members of the Department of Master of Computer Applications, "
        "and to my parents and friends, whose constant encouragement and moral support made it possible for me to complete this project successfully.",
        space_after=4, line_spacing=1.35)

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sig.paragraph_format.space_before = Pt(20)
    r = p_ack_sig.add_run("NANDHUPRIYA N\n(USN: 1RV24MC059)")
    r.font.name = 'Times New Roman'; r.font.size = Pt(10.5); r.font.bold = True

    doc.add_page_break()

    # ==========================================
    # 5. ABSTRACT PAGE (FITS EXACTLY 1 PAGE)
    # ==========================================
    add_styled_heading(doc, "ABSTRACT", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)

    add_body_p(doc,
        "Modern e-commerce retail networks generate massive volumes of customer transactions, sales records, and inventory data every day. "
        "Traditional Business Intelligence platforms show retrospective numbers and charts, but they suffer from what business managers call "
        "“dashboard fatigue”. Managers have to spend hours studying static bar charts and line plots to guess which customers might leave, "
        "how much stock should be reordered, and what products should be bundled together. In this project, we designed and developed an "
        "integrated web platform titled “AI-Powered E-Commerce Business Intelligence” to solve this practical operational challenge directly.",
        space_after=4, line_spacing=1.3)

    add_body_p(doc,
        "Our platform runs as a modern, interactive web application built with Python and Streamlit. It takes raw CSV files from heterogeneous "
        "retail sources—such as the UK Online Retail dataset, US Superstore, and Brazilian Olist—and automatically cleans and harmonizes them. "
        "We built an intelligent column-mapping mechanism that matches different aliases for customer IDs, dates, quantities, and prices without "
        "crashing when headers differ. The platform cleans dirty data, fills in missing values using median imputation, and removes anomalous "
        "transaction outliers using an Isolation Forest.",
        space_after=4, line_spacing=1.3)

    add_body_p(doc,
        "Once data is cleaned, our system executes four core analytical modules in parallel. First, it segments customers using Recency, Frequency, "
        "and Monetary (RFM) metrics and trains a Random Forest classifier with SMOTE oversampling to predict customer churn, achieving an "
        "88.5% ROC-AUC score. Second, it forecasts multi-horizon product demand using Amazon Chronos-Bolt foundation models with deterministic "
        "regression tree fallbacks, generating 14-day sales projections with confidence intervals. Third, it calculates safety stock and continuous-review "
        "Reorder Points (ROP) using the Silver-Meal heuristic to prevent stockouts while avoiding excessive storage costs. Fourth, it uncovers frequent "
        "purchasing patterns using Apriori association rule mining.",
        space_after=4, line_spacing=1.3)

    add_body_p(doc,
        "Finally, rather than leaving these predictions as separate charts, our platform features a Unified Business Decision Engine. This engine "
        "converts technical predictions into an executive action memo that lists specific, prioritized tasks ranked by financial impact. The memo "
        "is converted into natural speech via an integrated text-to-speech engine, allowing busy managers to listen to daily operational priorities. "
        "Users can also ask free-text questions through an interactive conversational assistant. Comprehensive software testing across 12 test suites "
        "and 35 test assertions verified 100% pass fidelity, zero runtime crashes, and sub-second rendering speeds on standard consumer hardware.",
        space_after=4, line_spacing=1.3)

    doc.add_page_break()

    # ==========================================
    # 6. TABLE OF CONTENTS
    # ==========================================
    add_styled_heading(doc, "TABLE OF CONTENTS", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8)

    toc_items = [
        ("Certificate", "ii", True),
        ("Declaration", "iii", True),
        ("Acknowledgement", "iv", True),
        ("Abstract", "v", True),
        ("List of Figures", "viii", True),
        ("List of Tables", "ix", True),
        ("Chapter 1: INTRODUCTION", "1", True),
        ("1.1 Project Description", "1", False),
        ("1.2 Objectives of the Project", "2", False),
        ("1.3 Scope of the Project", "3", False),
        ("Chapter 2: LITERATURE SURVEY", "5", True),
        ("2.1 Literature Survey", "5", False),
        ("2.2 Existing System", "7", False),
        ("2.3 Proposed System", "8", False),
        ("2.4 Feasibility Study", "10", False),
        ("2.5 Hardware and Software Requirements", "11", False),
        ("Chapter 3: SOFTWARE REQUIREMENTS SPECIFICATIONS", "12", True),
        ("3.1 Users and User Characteristics", "12", False),
        ("3.2 Functional Requirements", "13", False),
        ("3.3 Non-Functional Requirements", "15", False),
        ("Chapter 4: SYSTEM DESIGN", "17", True),
        ("4.1 System Architecture", "17", False),
        ("4.2 System Modules", "20", False),
        ("4.3 Data Flow", "21", False),
        ("4.4 System Workflow", "22", False),
        ("Chapter 5: DETAILED DESIGN", "23", True),
        ("5.1 Activity Diagram", "23", False),
        ("5.2 Use Case Diagram", "24", False),
        ("5.3 Class Diagram", "26", False),
        ("5.4 Sequence Diagram", "27", False),
        ("Chapter 6: IMPLEMENTATION", "29", True),
        ("6.1 Coding Guidelines", "29", False),
        ("6.2 Core Implementation Code Snippets", "30", False),
        ("6.3 Screenshots and User Interface", "35", False),
        ("Chapter 7: SOFTWARE TESTING", "41", True),
        ("7.1 Testing Methods", "41", False),
        ("7.2 Test Cases", "42", False),
        ("Chapter 8: CONCLUSION", "45", True),
        ("8.1 Conclusion", "45", False),
        ("8.2 Future Enhancements", "46", False),
        ("Chapter 9: SCOPE FOR FURTHER ENHANCEMENT", "47", True),
        ("9.1 Real-Time Data Streaming", "47", False),
        ("9.2 Advanced Pricing Models", "47", False),
        ("9.3 Multi-Warehouse Inventory Support", "47", False),
        ("9.4 Voice Assistant Improvements", "48", False),
        ("9.5 Data Privacy and Compliance", "48", False),
        ("Chapter 10: BIBLIOGRAPHY", "49", True),
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.columns[0].width = Inches(1.8)
    t_toc.columns[1].width = Inches(3.8)
    t_toc.columns[2].width = Inches(0.9)

    hdr = t_toc.rows[0].cells
    hdr[0].paragraphs[0].text = "Chapter / Section"
    hdr[1].paragraphs[0].text = "Topic / Title"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, 40, 40, 80, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'; r.font.size = Pt(9.5); r.font.bold = True

    for idx, (title, pg, is_main) in enumerate(toc_items):
        row = t_toc.rows[idx + 1].cells
        set_cell_margins(row[0], 25, 25, 60, 60)
        set_cell_margins(row[1], 25, 25, 60, 60)
        set_cell_margins(row[2], 25, 25, 60, 60)

        parts = title.split(":", 1) if ":" in title else title.split(" ", 1)
        if is_main and ":" in title:
            ch_num = parts[0].strip()
            ch_name = parts[1].strip()
        elif not is_main and " " in title and title.split(" ")[0][0].isdigit():
            sec_parts = title.split(" ", 1)
            ch_num = sec_parts[0].strip()
            ch_name = sec_parts[1].strip()
        else:
            ch_num = ""
            ch_name = title

        p0 = row[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(ch_num)
        r0.font.name = 'Times New Roman'; r0.font.size = Pt(9)
        if is_main: r0.font.bold = True

        p1 = row[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(ch_name)
        r1.font.name = 'Times New Roman'; r1.font.size = Pt(9)
        if is_main: r1.font.bold = True

        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(pg)
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(9)
        if is_main: r2.font.bold = True

    doc.add_page_break()

    # ==========================================
    # 7. LIST OF FIGURES
    # ==========================================
    add_styled_heading(doc, "LIST OF FIGURES", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8)

    fig_items = [
        ("Figure 4.1", "Context Diagram (Level-0 DFD) of the System", "17"),
        ("Figure 4.2", "System Perspective and Tiered Architecture", "18"),
        ("Figure 4.3", "High-Level System Architecture", "19"),
        ("Figure 4.4", "Analytical Data Processing Pipeline", "22"),
        ("Figure 5.1", "Activity Diagram for Analytical Lifecycle", "23"),
        ("Figure 5.2", "Use Case Diagram of the System", "24"),
        ("Figure 5.3", "Object-Oriented Class Diagram of Core Architecture", "26"),
        ("Figure 5.4", "Sequence Diagram for Analytics & Decision Workflow", "27"),
        ("Figure 6.1", "User Authentication and Role-Based Access Interface", "35"),
        ("Figure 6.2", "Multi-Schema Dataset Ingestion and Harmonization View", "36"),
        ("Figure 6.3", "Executive KPI Overview and Business Health Dashboard", "37"),
        ("Figure 6.4", "Customer Churn Classification and Retention Risk Dashboard", "37"),
        ("Figure 6.5", "Sales Demand Forecasting with Confidence Intervals", "38"),
        ("Figure 6.6", "Inventory Stockout Risk and Reorder Point Matrix", "39"),
        ("Figure 6.7", "Business Action Register and Voice Narration Interface", "39"),
        ("Figure 6.8", "Natural Language Query and Decision Support Assistant", "40"),
    ]

    t_fig = doc.add_table(rows=len(fig_items) + 1, cols=3)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fig.columns[0].width = Inches(1.5)
    t_fig.columns[1].width = Inches(4.1)
    t_fig.columns[2].width = Inches(0.9)

    hdr = t_fig.rows[0].cells
    hdr[0].paragraphs[0].text = "Figure No."
    hdr[1].paragraphs[0].text = "Caption"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, 40, 40, 80, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'; r.font.size = Pt(9.5); r.font.bold = True

    for idx, (fnum, caption, pg) in enumerate(fig_items):
        row = t_fig.rows[idx + 1].cells
        set_cell_margins(row[0], 25, 25, 60, 60)
        set_cell_margins(row[1], 25, 25, 60, 60)
        set_cell_margins(row[2], 25, 25, 60, 60)

        p0 = row[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(fnum)
        r0.font.name = 'Times New Roman'; r0.font.size = Pt(9); r0.font.bold = True

        p1 = row[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(caption)
        r1.font.name = 'Times New Roman'; r1.font.size = Pt(9)

        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(pg)
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(9)

    doc.add_page_break()

    # ==========================================
    # 8. LIST OF TABLES
    # ==========================================
    add_styled_heading(doc, "LIST OF TABLES", 1, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8)

    tab_items = [
        ("Table 2.1", "Comparison Between Existing Business Intelligence Tools and Proposed System", "9"),
        ("Table 3.1", "User Characteristics and Role-Based Access Control Specification Matrix", "12"),
        ("Table 7.1", "Comprehensive Software Test Execution Suite and Verification Log", "42"),
    ]

    t_tab = doc.add_table(rows=len(tab_items) + 1, cols=3)
    t_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tab.columns[0].width = Inches(1.5)
    t_tab.columns[1].width = Inches(4.1)
    t_tab.columns[2].width = Inches(0.9)

    hdr = t_tab.rows[0].cells
    hdr[0].paragraphs[0].text = "Table No."
    hdr[1].paragraphs[0].text = "Description"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, 40, 40, 80, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'; r.font.size = Pt(9.5); r.font.bold = True

    for idx, (tnum, desc, pg) in enumerate(tab_items):
        row = t_tab.rows[idx + 1].cells
        set_cell_margins(row[0], 25, 25, 60, 60)
        set_cell_margins(row[1], 25, 25, 60, 60)
        set_cell_margins(row[2], 25, 25, 60, 60)

        p0 = row[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(tnum)
        r0.font.name = 'Times New Roman'; r0.font.size = Pt(9); r0.font.bold = True

        p1 = row[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(desc)
        r1.font.name = 'Times New Roman'; r1.font.size = Pt(9)

        p2 = row[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(pg)
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(9)

    doc.add_page_break()
