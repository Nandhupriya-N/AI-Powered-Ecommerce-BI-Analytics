import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter8(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']

    add_styled_heading(doc, "Chapter 8", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "CONCLUSION", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    # 8.1 Conclusion
    add_styled_heading(doc, "8.1 Conclusion", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "The primary motivation behind developing “AI-Powered E-Commerce Business Intelligence” was to solve a major operational challenge "
        "faced by everyday retail businesses: the gap between retrospective reporting, machine learning predictions, and practical decision-making. "
        "Traditional Business Intelligence dashboards show historical sales numbers, but they do not guide managers on what operational steps "
        "to take next. By combining multi-schema data harmonization, predictive machine learning, supply chain optimization, and automated decision "
        "synthesis into a single, cohesive web platform, our project provides an accessible, end-to-end solution for modern e-commerce operators.")

    add_body_p(doc,
        "Throughout this Phase-1 project work, we achieved several notable technical milestones:")

    add_body_p(doc,
        "1. Zero-Crash Data Ingestion: We built an automated harmonization engine that successfully ingests diverse e-commerce CSV files "
        "(including the UK Online Retail dataset, US Superstore, and Brazilian Olist). The engine dynamically maps polymorphic column aliases, "
        "imputes missing numerical numbers using column medians, and isolates multivariate anomalies with an Isolation Forest, achieving 100% "
        "zero-crash reliability across irregular retail formats.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Accurate Predictive Modeling: We implemented an RFM-based customer churn prediction module that uses SMOTE oversampling and Random Forest "
        "classification, reaching an 88.5% ROC-AUC score on real-world retail benchmarks. In addition, our multi-horizon sales forecasting engine "
        "generates 14-day forward sales curves with confidence intervals using Amazon Chronos-Bolt and deterministic regression tree fallbacks.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Practical Supply Chain Optimization: We implemented continuous-review Reorder Points (ROP) and the Silver-Meal lot-sizing heuristic, "
        "allowing store managers to prevent stockouts while avoiding excessive warehouse storage costs.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Automated Decision Synthesis and Voice Briefing: Rather than leaving predictive outputs as isolated charts, our Unified Business Decision "
        "Engine synthesizes customer churn risks, demand forecasts, and stockout liabilities into an executive action memo ranked by financial impact. "
        "The memo includes automated audio voice narration and an interactive natural-language conversational assistant.",
        bold_prefix="• ")

    add_body_p(doc,
        "5. High Computational Performance: The application runs smoothly on consumer laptops with 8 to 16 GB of RAM, rendering executive dashboards "
        "in under 1.5 seconds and training machine learning models in under 5.0 seconds without requiring expensive cloud infrastructure.",
        bold_prefix="• ")

    # 8.2 Future Enhancements
    add_styled_heading(doc, "8.2 Future Enhancements", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "While our Phase-1 implementation fulfills all foundational functional and architectural requirements, there are several exciting "
        "directions for future expansion:")

    add_body_p(doc,
        "Cloud-Native Containerized Deployment: Packaging our platform into Docker microservices orchestrated on Kubernetes (EKS/GKE) will allow "
        "the application to scale dynamically across multiple server nodes, supporting thousands of concurrent retail users.",
        bold_prefix="• ")

    add_body_p(doc,
        "Direct ERP & E-Commerce Platform Connectors: Building native API connectors for popular e-commerce platforms like Shopify, WooCommerce, "
        "and Magento will enable automated synchronization of sales orders and product catalogs without requiring manual CSV uploads.",
        bold_prefix="• ")

    add_body_p(doc,
        "Mobile Application Companion: Developing a lightweight mobile companion application using React Native or Flutter will allow store managers "
        "to receive push notifications for stockout emergencies and listen to daily voice briefings directly on their smartphones.",
        bold_prefix="• ")

    doc.add_page_break()
