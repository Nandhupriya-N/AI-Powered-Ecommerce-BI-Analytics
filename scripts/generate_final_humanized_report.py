import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Import chapter builders
sys.path.append(os.path.join(os.path.dirname(__file__), 'chapters'))
from front_matter import build_front_matter
from ch1_intro import build_chapter1
from ch2_literature import build_chapter2
from ch3_srs import build_chapter3
from ch4_design import build_chapter4
from ch5_detailed_design import build_chapter5
from ch6_implementation import build_chapter6
from ch7_testing import build_chapter7
from ch8_conclusion import build_chapter8
from ch9_scope import build_chapter9
from ch10_bibliography import build_chapter10

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=30, bottom=30, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level, font_size=14, bold=True, space_before=10, space_after=5, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_p(doc, text, bold_prefix="", space_after=5, line_spacing=1.4, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.italic = italic
    return p

def add_bullet_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.35
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_code_block(doc, code_str):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_str)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_figure_image(doc, img_path, caption, width_in=4.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in))
    else:
        p_img = doc.add_paragraph(f"[Image file not found: {img_path}]")
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.keep_with_next = True
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(10)
    run_cap.font.bold = True
    run_cap.font.italic = True
    return p_cap

def add_page_number_field(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def setup_header_footer(section, is_front_matter=False):
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)

    if is_front_matter:
        section.different_first_page_header_footer = True
        xml_fmt = f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>'
        section._sectPr.append(parse_xml(xml_fmt))
    else:
        section.different_first_page_header_footer = False
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        xml_fmt = f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>'
        section._sectPr.append(parse_xml(xml_fmt))

    # Header setup with Tab Stop (Right Aligned at 6.25 inches)
    header = section.header
    if not is_front_matter:
        header.is_linked_to_previous = False

    p_hdr = header.paragraphs[0]
    p_hdr.text = ""
    p_hdr.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT)
    p_hdr.paragraph_format.space_after = Pt(2)

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        r_logo = p_hdr.add_run()
        r_logo.add_picture(logo_path, width=Inches(0.42))

    r_tab = p_hdr.add_run("\t")
    r_hdr_text = p_hdr.add_run("RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT ®  |  DEPT. OF MCA")
    r_hdr_text.font.name = 'Times New Roman'
    r_hdr_text.font.size = Pt(8)
    r_hdr_text.font.bold = True
    r_hdr_text.font.color.rgb = RGBColor(90, 90, 90)

    # Footer setup with Tab Stop (Right Aligned at 6.25 inches)
    footer = section.footer
    if not is_front_matter:
        footer.is_linked_to_previous = False

    p_ftr = footer.paragraphs[0]
    p_ftr.text = ""
    p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT)
    p_ftr.paragraph_format.space_before = Pt(4)

    r_left = p_ftr.add_run("AI-Powered E-Commerce Business Intelligence")
    r_left.font.name = 'Times New Roman'
    r_left.font.size = Pt(8.5)
    r_left.font.italic = True
    r_left.font.color.rgb = RGBColor(100, 100, 100)

    r_tab_f = p_ftr.add_run("\t")
    r_pg = p_ftr.add_run()
    r_pg.font.name = 'Times New Roman'
    r_pg.font.size = Pt(9)
    r_pg.font.bold = True
    r_pg.font.color.rgb = RGBColor(60, 60, 60)
    add_page_number_field(r_pg)

def main():
    print("Initializing document...")
    doc = Document()

    helpers = {
        'add_styled_heading': add_styled_heading,
        'add_body_p': add_body_p,
        'add_bullet_p': add_bullet_p,
        'add_code_block': add_code_block,
        'add_figure_image': add_figure_image,
        'set_cell_background': set_cell_background,
        'set_cell_margins': set_cell_margins
    }

    # Section 1: Front Matter
    print("Building Front Matter (Section 1)...")
    sec_front = doc.sections[0]
    setup_header_footer(sec_front, is_front_matter=True)
    build_front_matter(doc, helpers)

    # Section 2: Main Chapters
    print("Configuring Main Matter (Section 2)...")
    sec_main = doc.add_section()
    setup_header_footer(sec_main, is_front_matter=False)

    print("Building Chapter 1: Introduction...")
    build_chapter1(doc, helpers)

    print("Building Chapter 2: Literature Survey...")
    build_chapter2(doc, helpers)

    print("Building Chapter 3: Software Requirements Specifications...")
    build_chapter3(doc, helpers)

    print("Building Chapter 4: System Design...")
    build_chapter4(doc, helpers)

    print("Building Chapter 5: Detailed Design...")
    build_chapter5(doc, helpers)

    print("Building Chapter 6: Implementation...")
    build_chapter6(doc, helpers)

    print("Building Chapter 7: Software Testing...")
    build_chapter7(doc, helpers)

    print("Building Chapter 8: Conclusion...")
    build_chapter8(doc, helpers)

    print("Building Chapter 9: Scope for Further Enhancement...")
    build_chapter9(doc, helpers)

    print("Building Chapter 10: Bibliography...")
    build_chapter10(doc, helpers)

    docx_path = os.path.abspath("AI_Powered_Ecommerce_Business_Intelligence_Final_Report.docx")
    pdf_path = os.path.abspath("AI_Powered_Ecommerce_Business_Intelligence_Final_Report.pdf")

    print(f"Saving Word document to: {docx_path}")
    doc.save(docx_path)
    print("Word document saved successfully!")

    print("Converting DOCX to PDF using Word COM...")
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(docx_path)
        doc_com.SaveAs(pdf_path, FileFormat=17)
        doc_com.Close()
        word.Quit()
        print(f"PDF document saved successfully to: {pdf_path}")
    except Exception as e:
        print(f"Warning: Word COM conversion failed: {e}")
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            print(f"PDF document converted via docx2pdf to: {pdf_path}")
        except Exception as e2:
            print(f"docx2pdf also failed: {e2}")

    # Check page count
    if os.path.exists(pdf_path):
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"==================================================")
        print(f"TOTAL REPORT PAGES IN PDF: {total_pages}")
        print(f"==================================================")
    else:
        print("PDF was not created.")

if __name__ == "__main__":
    main()
