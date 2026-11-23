import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter5(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']
    add_figure_image = helpers['add_figure_image']

    add_styled_heading(doc, "Chapter 5", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "DETAILED DESIGN", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    add_body_p(doc,
        "Detailed design translates high-level architectural specifications into concrete object-oriented blueprints, behavioral activity flows, "
        "interaction sequence traces, and use case boundaries. In this chapter, we document the internal mechanisms of our software platform "
        "using standard Unified Modeling Language (UML) diagrams.")

    # 5.1 Activity Diagram
    add_styled_heading(doc, "5.1 Activity Diagram", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "An Activity Diagram models the dynamic operational workflow of a system, showing control branching, parallel operations, decision nodes, "
        "and termination states. Figure 5.1 illustrates the complete operational activity lifecycle of our platform, from user authentication to "
        "final decision generation.")

    add_figure_image(doc, "diagrams/fig5_1_activity_diagram.png", "Figure 5.1: Activity Diagram for Analytical Lifecycle", width_in=5.4)

    add_body_p(doc,
        "As depicted in Figure 5.1, the activity flow proceeds through several structured stages:")

    add_body_p(doc,
        "1. Authentication & Session Setup: The activity begins when a user submits credentials. The system hashes the password with PBKDF2-HMAC-SHA256 "
        "and verifies it against the SQLite database. If authentication fails, the user is redirected to the login screen with an error prompt. "
        "If successful, a secure session is initialized.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Ingestion & Schema Selection: The user either selects a preloaded retail scenario or uploads a custom CSV file. The ingestion engine reads "
        "the raw columns and maps them against canonical aliases.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Anomaly Isolation & Data Quality Check: An Isolation Forest evaluates transaction values, pruning extreme anomalies and computing an overall "
        "data cleanliness score.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Concurrent Analytical Execution: The cleaned data stream forks into four parallel analytical branches: customer RFM feature extraction and churn "
        "modeling, time-series aggregation for demand forecasting, inventory reorder point optimization, and market basket mining.",
        bold_prefix="• ")

    add_body_p(doc,
        "5. Decision Synthesis & Delivery: The parallel branches join into the Unified Decision Engine, which synthesizes outputs into a ranked action memo "
        "and triggers text-to-speech audio rendering. The user can interactively review results or ask questions via the conversational assistant.",
        bold_prefix="• ")

    # 5.2 Use Case Diagram
    add_styled_heading(doc, "5.2 Use Case Diagram", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "A Use Case Diagram defines system boundaries and illustrates the functional relationships between external actors and internal use cases. "
        "Figure 5.2 illustrates the Use Case Diagram for our platform, detailing the interactions of our four primary user roles.")

    add_figure_image(doc, "diagrams/fig5_2_use_case_diagram.png", "Figure 5.2: Use Case Diagram of the System", width_in=5.4)

    add_body_p(doc,
        "The diagram shows how our four actors interact with specific system capabilities:")

    add_body_p(doc,
        "System Administrator: Manages user accounts, configures system settings, monitors database logs, and reviews system health.",
        bold_prefix="• ")

    add_body_p(doc,
        "Business Executive: Reviews executive KPI cards, monitors customer retention summaries, reads the synthesized business action memo, "
        "and listens to audio voice briefings.",
        bold_prefix="• ")

    add_body_p(doc,
        "Data Analyst: Uploads custom CSV datasets, inspects data cleaning scores, evaluates churn ROC-AUC metrics, reviews sales forecasting curves "
        "with confidence bounds, and queries datasets using the natural language assistant.",
        bold_prefix="• ")

    add_body_p(doc,
        "Operations / Inventory Manager: Reviews product stockout risk tables, calculates safety stock levels using the Silver-Meal heuristic, "
        "inspects Reorder Points, and exports replenishment order schedules.",
        bold_prefix="• ")

    # 5.3 Class Diagram
    add_styled_heading(doc, "5.3 Class Diagram", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "A Class Diagram models the static structural perspective of the system by depicting core object-oriented classes, their attributes, methods, "
        "and structural associations. Figure 5.3 presents the Class Diagram for our application's core architecture.")

    add_figure_image(doc, "diagrams/fig5_3_class_diagram.png", "Figure 5.3: Object-Oriented Class Diagram of Core Architecture", width_in=5.4)

    add_body_p(doc,
        "As shown in Figure 5.3, the architecture centers around six primary collaborating classes:")

    add_body_p(doc,
        "DataProcessor (`src/data_processor.py`): Encapsulates raw data ingestion and cleaning. Key attributes include `raw_df`, `clean_df`, and `alias_map`. "
        "Key methods include `harmonize_ecommerce_data()`, `impute_missing_values()`, and `filter_outliers_isolation_forest()`.",
        bold_prefix="• ")

    add_body_p(doc,
        "ChurnAnalyzer (`src/analyzer.py`): Handles customer retention analytics. Key attributes include `rfm_df`, `model_rf`, and `roc_auc_score`. "
        "Key methods include `calculate_rfm_metrics()`, `apply_smote_oversampling()`, and `train_churn_model()`.",
        bold_prefix="• ")

    add_body_p(doc,
        "SalesForecaster (`src/forecaster.py`): Manages demand predictions. Key attributes include `history_ts`, `forecast_horizon`, and `model_type`. "
        "Key methods include `aggregate_daily_sales()`, `predict_chronos_bolt()`, and `predict_tree_ensemble_fallback()`.",
        bold_prefix="• ")

    add_body_p(doc,
        "InventoryOptimizer (`src/inventory_optimizer.py`): Manages supply chain calculations. Key attributes include `holding_cost`, `ordering_cost`, "
        "and `service_level_z`. Key methods include `calculate_reorder_points()`, `apply_silver_meal()`, and `generate_stockout_alerts()`.",
        bold_prefix="• ")

    add_body_p(doc,
        "DecisionEngine (`src/decision_engine.py`): Coordinates multi-model synthesis. Key methods include `synthesize_business_memo()`, "
        "`rank_actions_by_roi()`, and `generate_voice_briefing()`.",
        bold_prefix="• ")

    add_body_p(doc,
        "AuthManager (`src/auth.py`): Manages authentication and user sessions. Key methods include `hash_password_pbkdf2()`, `verify_user_credentials()`, "
        "and `check_role_permission()`.",
        bold_prefix="• ")

    # 5.4 Sequence Diagram
    add_styled_heading(doc, "5.4 Sequence Diagram", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "A Sequence Diagram captures the chronological order of message exchanges between participating objects over time. Figure 5.4 displays "
        "the Sequence Diagram for a complete analytics and decision generation workflow.")

    add_figure_image(doc, "diagrams/fig5_4_sequence_diagram.png", "Figure 5.4: Sequence Diagram for Analytics & Decision Generation Workflow", width_in=5.4)

    add_body_p(doc,
        "The interaction trace proceeds chronologically as follows:")

    add_body_p(doc,
        "1. Credential Submission & Validation: The User enters login credentials via the Streamlit UI. The UI sends a validation request to `AuthManager`, "
        "which queries SQLite, verifies the salted hash, and returns an authenticated user session.",
        bold_prefix="1. ")

    add_body_p(doc,
        "2. File Upload & Harmonization: The User uploads a sales CSV. The UI dispatches the file to `DataProcessor`, which cleans columns, runs the "
        "Isolation Forest, and returns a sanitized dataframe.",
        bold_prefix="2. ")

    add_body_p(doc,
        "3. Concurrent Model Execution: The UI requests churn predictions from `ChurnAnalyzer`, sales forecasts from `SalesForecaster`, and inventory alerts "
        "from `InventoryOptimizer`. Each module executes its algorithms and returns structured analytical results.",
        bold_prefix="3. ")

    add_body_p(doc,
        "4. Decision Synthesis & Audio Generation: The UI passes these results to `DecisionEngine`, which compiles the prioritized action register and calls "
        "`gTTS` to generate an audio voice memo.",
        bold_prefix="4. ")

    add_body_p(doc,
        "5. Final Presentation: The UI renders the completed dashboards, interactive charts, and playable audio briefing to the User.",
        bold_prefix="5. ")

    doc.add_page_break()
