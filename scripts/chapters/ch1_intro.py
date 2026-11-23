import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter1(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']

    add_styled_heading(doc, "Chapter 1", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "INTRODUCTION", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    # 1.1 Project Description
    add_styled_heading(doc, "1.1 Project Description", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "Online shopping has expanded rapidly in recent years. Today, retail businesses process thousands of transactions every single day, "
        "recording timestamps, item quantities, unit prices, customer identifiers, and shipping locations. This steady inflow of numbers creates "
        "huge datasets. In theory, having access to so much transactional data should make it easy for store owners to run their business smoothly. "
        "They should know who is buying, what items are running out of stock, and which loyal buyers are slowly losing interest. In reality, "
        "things are never that simple.")

    add_body_p(doc,
        "Most e-commerce managers rely on conventional Business Intelligence tools or spreadsheet workbooks to track performance. "
        "These dashboards display retrospective metrics such as total sales revenue from last week, top-selling categories from last month, "
        "and geographical sales distribution. While these retrospective charts show what already happened, they fail to tell the manager what to do next. "
        "A manager might stare at a dashboard displaying forty different graphs, yet still struggle to make a concrete business decision. "
        "Industry practitioners call this problem dashboard fatigue. It takes hours of manual effort to translate a drop in sales numbers into "
        "practical supply chain orders or customer retention emails.")

    add_body_p(doc,
        "Another serious obstacle is data quality. E-commerce transaction records arrive in diverse file layouts. One store export might label "
        "customer identification numbers as 'CustomerID', another platform might label it as 'client_id', and a third export might call it 'user_code'. "
        "Order timestamps can appear as 'InvoiceDate', 'order_timestamp', or 'purchase_date'. When analysts attempt to load these different CSV files "
        "into traditional data science scripts, the programs crash immediately due to missing column names or unexpected data types. "
        "Furthermore, human data entry errors and software bugs often introduce negative quantities, zero unit prices, and abnormal outlier values "
        "that distort statistical calculations.")

    add_body_p(doc,
        "Even when data is properly formatted, predictive modeling remains disconnected from everyday operations. A data scientist might build "
        "a customer churn classification model in a separate Python notebook, but the output remains isolated as a CSV list of probabilities. "
        "The marketing department rarely knows how to use raw probability scores. Similarly, supply chain teams frequently calculate inventory "
        "reorder points using basic rules of thumb rather than linking their replenishment schedules to seasonal demand forecasting models. "
        "These operational silos result in two costly problems: valuable customers slip away unnoticed, and warehouses alternate between expensive "
        "overstocking and damaging stockouts.")

    add_body_p(doc,
        "We designed and developed this MCA project, titled “AI-Powered E-Commerce Business Intelligence”, to solve these practical problems directly. "
        "Our goal was not just to build another dashboard with charts, but to build an end-to-end software application that connects raw data ingestion, "
        "predictive machine learning, and operational action recommendations into one unified workflow. When a user uploads an e-commerce sales dataset, "
        "our system automatically detects column headers, repairs missing values, isolates abnormal outliers, runs machine learning models for customer "
        "churn and sales demand, calculates inventory reorder levels, and generates a clear action register that tells the business owner exactly what "
        "steps to take today.")

    # 1.2 Objectives of the Project
    add_styled_heading(doc, "1.2 Objectives of the Project", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "The primary aim of our project is to create an accessible, dependable, and intelligent analytics system tailored for e-commerce operators. "
        "To achieve this overall goal, we divided our development into six concrete technical objectives:")

    add_body_p(doc,
        "1. Automated Multi-Schema Data Harmonization: Build an ingestion engine in Python that accepts heterogeneous CSV files from different e-commerce "
        "platforms (such as Kaggle retail benchmarks, UK Online Retail, and US Superstore datasets). The system must match column aliases dynamically, "
        "fill missing data with appropriate statistical measures, and remove anomalous outlier records without crashing on irregular formats.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Customer Churn Prediction and Retention Scoring: Transform raw transaction logs into behavioral Recency, Frequency, and Monetary (RFM) metrics. "
        "Train a Random Forest classification model with Synthetic Minority Over-sampling Technique (SMOTE) to identify customers who are likely to stop "
        "purchasing, providing clear probability scores and ranking key churn factors.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Multi-Horizon Sales Demand Forecasting: Model product sales trends over time using modern time-series forecasting. The platform must generate "
        "14-day forward demand projections with upper and lower confidence intervals, incorporating automated fallbacks to regression trees when hardware "
        "resources are constrained.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Supply Chain Safety Stock and Reorder Optimization: Implement continuous-review inventory control formulas and the Silver-Meal lot-sizing "
        "heuristic. The application must calculate exact Reorder Points (ROP) and safety stocks for every inventory item to eliminate stockouts while "
        "controlling holding costs.",
        bold_prefix="• ")

    add_body_p(doc,
        "5. Automated Business Action Synthesis and Voice Briefing: Engineer a decision engine that takes the analytical outputs from all individual modules "
        "and synthesizes them into an executive action memo. The memo must rank recommended operational tasks by financial impact and support audio voice "
        "playback so store owners can listen to their daily operational priorities on the go.",
        bold_prefix="• ")

    add_body_p(doc,
        "6. Conversational Data Exploration Assistant: Develop an interactive chat assistant embedded directly in the web application. The assistant must "
        "allow business users to ask plain-English questions about sales figures, customer segments, and inventory shortages, translating user questions "
        "into safe SQL queries over in-memory tables.",
        bold_prefix="• ")

    # 1.3 Scope of the Project
    add_styled_heading(doc, "1.3 Scope of the Project", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "The scope of this Phase-1 project encompasses the complete data science and software development lifecycle, from raw data ingestion to "
        "a functioning, interactive web platform. The boundaries of the project are defined as follows:")

    add_body_p(doc,
        "Functional Scope: The application handles historical e-commerce transactional data containing customer identifiers, order dates, invoice lines, "
        "quantities purchased, and product prices. It supports four major analytical domains: descriptive sales analytics, customer retention modeling, "
        "time-series demand forecasting, and inventory replenishment planning. In addition, it includes cryptographic user authentication with role-based "
        "access control, automated decision synthesis, and voice-assisted memo narration.",
        bold_prefix="• ")

    add_body_p(doc,
        "Target Users: The software is designed for store owners, e-commerce operations managers, sales executives, and retail data analysts. "
        "It provides intuitive, graphical controls and clear tables so non-technical users can obtain actionable insights without writing code, "
        "while still allowing technical analysts to inspect detailed statistical metrics and model parameters.",
        bold_prefix="• ")

    add_body_p(doc,
        "Deployment Environment: The system is packaged as a lightweight web application using Streamlit, Scikit-learn, PyTorch, and SQLite. "
        "It is designed to run efficiently on standard consumer computer hardware (such as an Intel Core i5 processor with 8 to 16 GB of RAM) "
        "without requiring costly specialized cloud server clusters or dedicated graphics processing units.",
        bold_prefix="• ")

    add_body_p(doc,
        "Operational Boundaries: In this Phase-1 release, data ingestion is designed for periodic batch uploads of CSV files rather than millisecond-level "
        "real-time event streaming. Financial recommendations are generated as decision-support guidance for human store managers rather than executing "
        "unsupervised banking transactions or automated supplier purchase orders.",
        bold_prefix="• ")

    doc.add_page_break()
