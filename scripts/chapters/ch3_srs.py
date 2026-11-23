import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_chapter3(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']
    set_cell_background = helpers['set_cell_background']
    set_cell_margins = helpers['set_cell_margins']

    add_styled_heading(doc, "Chapter 3", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "SOFTWARE REQUIREMENTS SPECIFICATIONS", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    # 3.1 Users and User Characteristics
    add_styled_heading(doc, "3.1 Users and User Characteristics", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "An effective software system must be designed around the specific skills, operational responsibilities, and workflows of its human users. "
        "During requirement analysis, we identified four distinct user personas who interact with our platform: System Administrators, Business Executives, "
        "Data Analysts, and Operations Managers. Each group has different technical backgrounds and requires different views of the analytical data.")

    add_body_p(doc,
        "System Administrators are technical users responsible for system maintenance, user account provisioning, role management, and database integrity. "
        "They have strong software engineering skills and ensure that the server environment and cryptographic authentication services operate securely. "
        "Business Executives, such as store owners and managing directors, focus on high-level gross revenue, customer retention rates, and prioritized action memos. "
        "They typically have minimal programming experience and require clean visual dashboards and audio briefings. Data Analysts examine model parameters, "
        "confusion matrices, feature importance rankings, and data cleaning scores. Operations Managers manage warehouse inventory, tracking daily stock depletion "
        "rates and reorder schedules to prevent stockouts.")

    # Table 3.1
    add_styled_heading(doc, "Table 3.1: User Characteristics and Role-Based Access Control Specification Matrix", 3, font_size=11, bold=True, space_before=12, space_after=4)

    user_rows = [
        ("User Role", "Technical Background", "Primary Responsibilities", "Access Permissions & Visible Features"),
        ("System Administrator", "High (Software administration, database management, security protocols)", "User account provisioning, session auditing, server maintenance, database backups", "Full administrative access: User management console, system logs, security settings, all analytical modules"),
        ("Business Executive", "Low to Medium (Business strategy, retail operations, financial oversight)", "Monitoring top-line revenue, tracking customer retention, reviewing strategic action items", "Executive KPI dashboard, customer retention summaries, financial action memos, voice briefing playback"),
        ("Data Analyst", "High (Data manipulation, statistics, exploratory analysis, machine learning)", "Evaluating model accuracy, tuning hyperparameters, inspecting feature importance, validating datasets", "Full data science suite: Raw dataset inspection, outlier distribution plots, ROC-AUC curves, association rules, SQL assistant"),
        ("Operations / Inventory Manager", "Medium (Supply chain logistics, purchasing, warehouse management)", "Tracking stock levels, executing purchase orders, preventing product stockouts, managing lead times", "Supply chain module: Safety stock matrices, Reorder Point (ROP) tables, stockout alerts, lot-sizing calculators")
    ]

    t_users = doc.add_table(rows=len(user_rows), cols=4)
    t_users.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_users.columns[0].width = Inches(1.4)
    t_users.columns[1].width = Inches(1.5)
    t_users.columns[2].width = Inches(1.8)
    t_users.columns[3].width = Inches(2.0)

    for r_idx, row in enumerate(user_rows):
        cells = t_users.rows[r_idx].cells
        is_h = (r_idx == 0)
        for c_idx, val in enumerate(row):
            c = cells[c_idx]
            set_cell_margins(c, 50, 50, 60, 60)
            if is_h:
                set_cell_background(c, "EAEAEA")
            elif r_idx % 2 == 1:
                set_cell_background(c, "F9F9F9")
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_h else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9 if not is_h else 9.5)
            if is_h or c_idx == 0: r.font.bold = True

    # 3.2 Functional Requirements
    add_styled_heading(doc, "3.2 Functional Requirements", 2, font_size=14, bold=True, space_before=16, space_after=6)

    add_body_p(doc,
        "Functional requirements describe the specific operations, behaviors, and services that the software must provide to its users. "
        "We formalized these requirements into ten modular functional specifications (FR-01 to FR-10):")

    fr_specs = [
        ("FR-01: User Authentication & Role Management: ",
         "The system shall provide a secure login interface where users authenticate using a username and password. "
         "Passwords must be hashed using PBKDF2 with SHA-256 and an individual cryptographic salt. The system shall maintain user sessions "
         "and enforce role-based access control, ensuring that users only view pages and controls permitted by their assigned role."),

        ("FR-02: Multi-Schema Ingestion & Outlier Cleaning: ",
         "The system shall accept CSV dataset uploads through a web widget and provide pre-loaded benchmark retail scenarios. "
         "An intelligent alias dictionary shall map irregular column names (e.g., 'client_id' to 'customer_id', 'invoicedate' to 'order_date') "
         "automatically. Missing numerical values must be imputed with column medians, and missing dates must be filled safely. "
         "An Isolation Forest model shall identify multivariate outliers in sales and quantities and filter them out to prevent statistical distortion."),

        ("FR-03: Executive Business KPI Calculation: ",
         "The system shall compute core retail KPIs from cleaned transaction logs, including Total Revenue, Total Order Count, "
         "Average Order Value (AOV), and Overall Customer Retention Rate. These metrics must render immediately upon dataset selection "
         "in prominent visual cards alongside interactive Plotly charts showing monthly sales trends and category distributions."),

        ("FR-04: Customer Churn Classification & RFM Segmentation: ",
         "The system shall transform transactional logs into customer-level RFM features (Recency, Frequency, and Monetary spend). "
         "To handle class imbalance, the system shall apply SMOTE oversampling. The system shall train a Random Forest classifier "
         "to predict whether each active customer is at risk of churning, outputting calibrated probability scores and ranking primary churn factors."),

        ("FR-05: Multi-Horizon Sales Demand Forecasting: ",
         "The system shall aggregate daily sales into time series and generate 14-day forward demand projections. "
         "The system shall utilize the Chronos-Bolt foundation model when available and automatically fall back to gradient boosting or "
         "random forest regression tree ensembles when hardware constraints prevent neural model execution, displaying upper and lower confidence bounds."),

        ("FR-06: Supply Chain Safety Stock & Reorder Optimization: ",
         "The system shall calculate average daily sales demand and demand standard deviation for every inventory item. "
         "Using a continuous-review inventory control formula and the Silver-Meal heuristic, the system shall determine the Reorder Point (ROP) "
         "and required safety stock, flagging products whose current stock is below the reorder threshold with urgent replenishment alerts."),

        ("FR-07: Customer Lifetime Value (CLV) & Pareto Segmentation: ",
         "The system shall estimate 12-month forward Customer Lifetime Value for each customer based on purchase history and average order margins. "
         "The system shall apply the Pareto 80/20 principle to categorize customers into Gold, Silver, and Bronze tiers, allowing marketing teams "
         "to focus retention campaigns on high-value buyers."),

        ("FR-08: Market Basket Association Analysis: ",
         "The system shall analyze co-occurring items in transaction invoices using the Apriori association rule mining algorithm. "
         "It shall compute Support, Confidence, and Lift metrics for product pairs, identifying strong cross-selling bundles (rules with Lift > 1.2) "
         "to help retail managers optimize website merchandising and promotional packages."),

        ("FR-09: Automated Executive Decision Synthesis & Voice Memo: ",
         "The system shall feature a Unified Business Decision Engine that aggregates liabilities from customer churn, sales trends, and stockout risks. "
         "It shall generate an action memo listing specific, prioritized tasks ranked by estimated financial impact. "
         "An integrated text-to-speech module shall synthesize the text into an audio briefing that users can listen to directly in their browser."),

        ("FR-10: Conversational Query Assistant & Data Exploration: ",
         "The system shall provide an interactive natural language chat interface. "
         "Users can type or speak questions regarding store revenue, churn rates, or low-stock items. "
         "The system shall translate these questions into safe SQL queries executed against in-memory SQLite tables, displaying tabular answers "
         "and natural-language explanations without exposing backend database internals.")
    ]

    for prefix, body in fr_specs:
        add_body_p(doc, body, bold_prefix=prefix)

    # 3.3 Non-Functional Requirements
    add_styled_heading(doc, "3.3 Non-Functional Requirements", 2, font_size=14, bold=True, space_before=16, space_after=6)

    add_body_p(doc,
        "Non-functional requirements specify the operational quality, performance standards, security protections, and usability constraints "
        "of the software system. We defined six essential non-functional requirements (NFR-01 to NFR-06):")

    nfr_specs = [
        ("NFR-01: Performance & Response Time: ",
         "The web application shall render initial executive KPI dashboards in less than 1.5 seconds upon dataset selection. "
         "Machine learning training for customer churn and demand forecasting shall complete in under 5.0 seconds for datasets containing up to "
         "50,000 transaction rows on standard consumer laptop hardware. Audio voice briefing generation shall begin playback within 2.0 seconds."),

        ("NFR-02: Security & Session Isolation: ",
         "User credentials must never be stored in plain text. Passwords must be hashed using PBKDF2-HMAC-SHA256 with a unique 16-byte salt and at least "
         "100,000 hashing iterations. Session states must remain isolated between different user browser tabs. Natural language SQL queries must be "
         "strictly read-only (SELECT queries only), rejecting any DROP, UPDATE, DELETE, or INSERT statements to prevent SQL injection vulnerabilities."),

        ("NFR-03: Zero-Crash Reliability & Fault Tolerance: ",
         "The data ingestion pipeline must handle dirty, irregular, or missing data gracefully without raising unhandled runtime exceptions. "
         "If a foundation forecasting model fails due to GPU memory constraints, the system must seamlessly fall back to deterministic regression tree "
         "models, ensuring uninterrupted user experience."),

        ("NFR-04: Scalability & Resource Efficiency: ",
         "The software architecture must run efficiently on local machines with 8 GB of RAM and standard dual-core or quad-core CPUs. "
         "Matrix computations and data cleaning operations must utilize vectorized Pandas and NumPy operations to minimize memory overhead."),

        ("NFR-05: Usability & User Experience: ",
         "The user interface must follow modern design principles, featuring clean typography, consistent color palettes, responsive layout grids, "
         "and intuitive navigation tabs. Non-technical users must be able to complete a full analytical run—from CSV upload to decision memo generation—"
         "in fewer than three clicks without consulting external documentation."),

        ("NFR-06: Maintainability & Modularity: ",
         "The codebase must adhere strictly to PEP 8 standards, utilizing modular directory organization, explicit type hints, and comprehensive "
         "docstrings. Individual analytical components (data cleaning, churn modeling, forecasting, inventory, decisions) must remain decoupled, "
         "allowing developers to update or replace specific algorithms without affecting other subsystems.")
    ]

    for prefix, body in nfr_specs:
        add_body_p(doc, body, bold_prefix=prefix)

    doc.add_page_break()
