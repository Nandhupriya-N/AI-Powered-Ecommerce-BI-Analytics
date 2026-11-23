import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter9(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']

    add_styled_heading(doc, "Chapter 9", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "SCOPE FOR FURTHER ENHANCEMENT", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    add_body_p(doc,
        "The architecture of “AI-Powered E-Commerce Business Intelligence” was intentionally designed with modular interfaces to facilitate "
        "future research and technical enhancements. In this chapter, we outline five promising technical areas that can be explored in future "
        "iterations of the platform.")

    # 9.1 Real-Time Data Streaming
    add_styled_heading(doc, "9.1 Real-Time Data Streaming", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "In our current Phase-1 release, data ingestion operates primarily on batch CSV files uploaded by users. As retail enterprises expand, "
        "transactional velocity increases significantly. A natural enhancement is transitioning ingestion from static file uploads to real-time "
        "distributed event streaming using Apache Kafka and Apache Spark Streaming. This architecture would allow the platform to process incoming "
        "purchase webhooks, live cart abandonment events, and real-time inventory decrement signals within sub-second latencies. By maintaining "
        "rolling sliding windows over streaming data, the system could update revenue velocity metrics and recalculate stockout risks continuously.")

    # 9.2 Advanced Pricing Models
    add_styled_heading(doc, "9.2 Advanced Pricing Models", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Retail pricing directly impacts customer conversion rates, gross profit margins, and inventory turnover. Future versions of our software "
        "can integrate dynamic pricing algorithms powered by Deep Reinforcement Learning (such as Proximal Policy Optimization or Deep Q-Networks). "
        "The pricing agent could observe real-time competitor price feeds, current warehouse inventory age, and demand price elasticity, adjusting "
        "product discounts dynamically to maximize total gross revenue while preventing excess inventory buildup.")

    # 9.3 Multi-Warehouse Inventory Support
    add_styled_heading(doc, "9.3 Multi-Warehouse Inventory Support", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Our current inventory optimization module calculates safety stock and Reorder Points (ROP) assuming a single centralized warehouse location. "
        "However, multi-channel e-commerce retailers frequently maintain regional fulfillment centers located near major metropolitan areas. "
        "Extending the inventory optimization model into a multi-echelon supply chain network using Mixed-Integer Linear Programming (MILP) would allow "
        "the software to balance stock across regional hubs, minimizing long-distance shipping expenses and delivery lead times.")

    # 9.4 Voice Assistant Improvements
    add_styled_heading(doc, "9.4 Voice Assistant Improvements", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "While our current assistant uses the browser's Web Speech API and Google Text-to-Speech for audio synthesis, future releases can incorporate "
        "fully offline, edge-deployable speech-to-text models like OpenAI Whisper Small alongside quantized local Large Language Models (such as LLaMA-3 "
        "or Mistral 7B running via Ollama). This would enable sophisticated, context-aware conversational voice interactions without relying on external "
        "cloud API connections, ensuring faster response times and complete privacy for proprietary sales data.")

    # 9.5 Data Privacy and Compliance
    add_styled_heading(doc, "9.5 Data Privacy and Compliance", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "As global data privacy regulations (such as GDPR, CCPA, and India's Digital Personal Data Protection Act) become increasingly stringent, "
        "future enhancements must prioritize automated regulatory compliance. Integrating automated Personally Identifiable Information (PII) "
        "masking engines will ensure that sensitive customer data (such as customer names, email addresses, phone numbers, and physical delivery addresses) "
        "is automatically hashed or anonymized during ingestion before being written to disk or processed by analytical machine learning models.")

    doc.add_page_break()
