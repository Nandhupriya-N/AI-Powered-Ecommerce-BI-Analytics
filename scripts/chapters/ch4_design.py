import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter4(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']
    add_figure_image = helpers['add_figure_image']

    add_styled_heading(doc, "Chapter 4", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "SYSTEM DESIGN", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    # 4.1 System Architecture
    add_styled_heading(doc, "4.1 System Architecture", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "System architecture defines the high-level structural organization of software components, their interfaces, and the pathways "
        "through which data flows across system boundaries. Designing a clean, modular architecture was essential for our project because "
        "it combines diverse computational tasks: data ingestion, unsupervised anomaly detection, supervised machine learning, statistical "
        "time-series forecasting, and voice synthesis. To ensure maintainability, we structured the platform into well-defined architectural layers.")

    add_body_p(doc,
        "We begin by examining the system context. A context diagram, also known as a Level-0 Data Flow Diagram (DFD), models the software "
        "as a single central system interacting with external entities. In our application, external entities include business users (who provide "
        "credentials and queries), raw e-commerce CSV files (uploaded by users or selected from preloaded scenarios), and the voice output devices "
        "that deliver spoken memos. Figure 4.1 illustrates this high-level boundary interaction.")

    add_figure_image(doc, "diagrams/fig4_1_context_diagram.png", "Figure 4.1: Context Diagram (Level-0 DFD) of the System", width_in=5.4)

    add_body_p(doc,
        "As shown in Figure 4.1, the system receives three primary inputs from external entities: user authentication credentials, raw e-commerce "
        "CSV files, and interactive natural-language queries. The internal system processes these inputs through its data harmonization, machine learning, "
        "and decision engines. In return, the system delivers three primary outputs: interactive visual KPI dashboards, an ROI-ranked business "
        "action memo, and synthesized voice briefings played through the browser. This clean boundary ensures that external data formats can change "
        "without affecting internal analytical processing.")

    add_body_p(doc,
        "To translate this context into a concrete software implementation, we organized the platform into a four-tier architecture, as illustrated "
        "in Figure 4.2. This tiered perspective separates the user interface, application controllers, analytical machine learning models, and underlying "
        "data persistence layers.")

    add_figure_image(doc, "diagrams/fig4_2_system_perspective.png", "Figure 4.2: System Perspective and Tiered Architecture", width_in=5.4)

    add_body_p(doc,
        "The four tiers illustrated in Figure 4.2 fulfill distinct operational responsibilities:")

    add_body_p(doc,
        "1. Presentation Tier (Client Layer): Built using Streamlit, HTML5, and Plotly. It renders reactive metric cards, dynamic line charts, "
        "interactive sliders, and data tables. It runs directly inside standard web browsers (Google Chrome, Mozilla Firefox, Microsoft Edge) "
        "and handles browser-native voice dictation via the Web Speech API.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Application Logic Tier (Controller Layer): Implemented in Python. This tier coordinates user requests, validates session tokens, "
        "manages the workflow between different analytical modules, and directs cleaned datasets to the appropriate model engines.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Analytical & Machine Learning Tier (Model Engine): Houses the core mathematical and predictive algorithms. This includes the Isolation Forest "
        "for anomaly detection, SMOTE oversampling, the Random Forest classifier for churn, Chronos-Bolt and gradient boosting trees for sales forecasting, "
        "the Silver-Meal inventory optimizer, Apriori association mining, and the Unified Business Decision Engine.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Data Persistence & In-Memory Storage Tier: Combines an embedded SQLite database (for user accounts, salted password hashes, and session logs) "
        "with high-speed in-memory Pandas dataframes and temporary SQLite tables for executing real-time analytical SQL queries.",
        bold_prefix="• ")

    add_body_p(doc,
        "Figure 4.3 provides a detailed structural view of the high-level system architecture, showing how individual Python modules within the "
        "codebase interact with one another.")

    add_figure_image(doc, "diagrams/fig4_3_system_architecture.png", "Figure 4.3: High-Level System Architecture", width_in=5.4)

    add_body_p(doc,
        "As depicted in Figure 4.3, incoming CSV datasets pass directly into the Multi-Schema Harmonizer (`src/data_processor.py`). "
        "The harmonizer standardizes column headers and filters outliers before writing clean data into memory. From there, four independent analytical "
        "engines process the data concurrently: the Churn Classifier (`src/analyzer.py`), the Demand Forecaster (`src/forecaster.py`), "
        "the Inventory Optimizer (`src/inventory_optimizer.py`), and the Association Engine. Finally, the Unified Decision Engine (`src/decision_engine.py`) "
        "synthesizes outputs from all four engines into an action memo, which is converted to audio by the Text-to-Speech Engine and made queryable "
        "by the Conversational Assistant (`src/assistant.py`).")

    # 4.2 System Modules
    add_styled_heading(doc, "4.2 System Modules", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "To ensure maintainability and high code quality, we organized the software into eight decoupled, modular components:")

    add_body_p(doc,
        "1. Authentication & Security Module (`src/auth.py`): Manages user registration, login verification, password hashing using PBKDF2-HMAC-SHA256, "
        "and session state management. It restricts access to administrative views and ensures sensitive operations cannot be performed by unauthenticated users.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Multi-Schema Harmonization Module (`src/data_processor.py`): Automatically maps heterogeneous column headers to canonical names using "
        "an alias dictionary. It performs statistical imputation for missing numerical values, parses date strings into standardized timestamps, and "
        "executes an Isolation Forest to remove multivariate anomalies.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Executive KPI Dashboard Module (`app.py`): Computes aggregate business metrics including total gross revenue, total completed orders, "
        "average order value, and active customer counts. It renders interactive Plotly charts showing monthly revenue trends and category breakdowns.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Customer Churn Prediction Module (`src/analyzer.py`): Computes customer-level RFM features, applies SMOTE to resolve class imbalance, and "
        "trains a Random Forest classifier. It outputs individual churn probability scores and identifies primary factors driving customer attrition.",
        bold_prefix="• ")

    add_body_p(doc,
        "5. Multi-Horizon Demand Forecasting Module (`src/forecaster.py`): Aggregates daily transaction totals and generates 14-day forward sales forecasts. "
        "It utilizes the Chronos-Bolt foundation model when available and falls back to deterministic regression trees when running on resource-constrained systems.",
        bold_prefix="• ")

    add_body_p(doc,
        "6. Supply Chain & Inventory Optimization Module (`src/inventory_optimizer.py`): Analyzes product-level demand mean and variance to determine "
        "continuous-review Reorder Points (ROP) and safety stock requirements. It applies the Silver-Meal heuristic to compute optimal replenishment quantities.",
        bold_prefix="• ")

    add_body_p(doc,
        "7. Unified Business Decision Engine (`src/decision_engine.py`): Aggregates predicted churn risks, demand trends, and stockout liabilities into "
        "a ranked executive action memo. It calculates estimated financial impact for each action and coordinates with Google Text-to-Speech (gTTS) for audio playback.",
        bold_prefix="• ")

    add_body_p(doc,
        "8. Conversational Query Assistant Module (`src/assistant.py`): Provides an interactive natural language chat interface. It converts user questions "
        "into safe SQL SELECT statements, executes them against in-memory tables, and returns clear summaries with tabular results.",
        bold_prefix="• ")

    # 4.3 Data Flow
    add_styled_heading(doc, "4.3 Data Flow", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Understanding data flow is critical for verifying how raw numbers transform into actionable business recommendations. In our platform, "
        "data flows sequentially through six distinct processing stages:")

    add_body_p(doc,
        "Stage 1 – Ingestion & Upload: The user uploads a CSV file or selects a preloaded benchmark scenario. The raw byte stream is read into a temporary "
        "Pandas dataframe.",
        bold_prefix="1. ")

    add_body_p(doc,
        "Stage 2 – Column Normalization & Imputation: Column headers are converted to lowercase, stripped of whitespace, and matched against canonical "
        "alias dictionaries. Missing numerical values are imputed using column medians, and dates are parsed into ISO timestamps.",
        bold_prefix="2. ")

    add_body_p(doc,
        "Stage 3 – Outlier Isolation: The cleaned dataset is passed to an Isolation Forest algorithm (`contamination=0.05`). Anomalous rows with "
        "abnormal price spikes or impossible quantities are filtered out, producing a clean analysis dataframe.",
        bold_prefix="3. ")

    add_body_p(doc,
        "Stage 4 – Feature Extraction & Model Execution: The clean dataframe is partitioned. One stream generates RFM features for churn classification, "
        "a second stream aggregates daily sales for demand forecasting, and a third stream calculates SKU-level demand statistics for inventory optimization.",
        bold_prefix="4. ")

    add_body_p(doc,
        "Stage 5 – Decision Synthesis: Predictions from all models are collected by the Unified Decision Engine, which evaluates financial risk "
        "and creates a prioritized list of business actions.",
        bold_prefix="5. ")

    add_body_p(doc,
        "Stage 6 – Visualization & Audio Delivery: Outputs are rendered as interactive Plotly charts, data tables, and an audio MP3 voice briefing.",
        bold_prefix="6. ")

    # 4.4 System Workflow
    add_styled_heading(doc, "4.4 System Workflow", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Figure 4.4 presents the complete end-to-end analytical processing pipeline flowchart, detailing how every computational step executes "
        "from initial file ingestion to final executive presentation.")

    add_figure_image(doc, "diagrams/fig4_4_analytical_pipeline.png", "Figure 4.4: Analytical Data Processing Pipeline Flowchart", width_in=5.4)

    add_body_p(doc,
        "As illustrated in Figure 4.4, the workflow incorporates defensive validation at each stage. If a user uploads a file with missing headers, "
        "the alias matching engine resolves the discrepancies without halting execution. If a foundation forecasting model encounters a hardware bottleneck, "
        "the fallback mechanism activates instantly. This fault-tolerant pipeline ensures that business users receive dependable insights without "
        "experiencing technical crashes or unhandled exceptions.")

    doc.add_page_break()
