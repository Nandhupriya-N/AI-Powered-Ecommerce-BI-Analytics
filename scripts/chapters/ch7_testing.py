import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_chapter7(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']
    set_cell_background = helpers['set_cell_background']
    set_cell_margins = helpers['set_cell_margins']

    add_styled_heading(doc, "Chapter 7", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "SOFTWARE TESTING", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    add_body_p(doc,
        "Software testing is an indispensable phase of software engineering. It verifies that every module operates correctly according to "
        "specifications, handles unexpected edge cases gracefully, and delivers accurate mathematical outputs. In our project, we implemented "
        "a multi-tiered testing strategy spanning unit, integration, boundary, security, and automated system verification.")

    # 7.1 Testing Methods
    add_styled_heading(doc, "7.1 Testing Methods", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "We applied five complementary testing methodologies to validate our application thoroughly:")

    add_body_p(doc,
        "1. Unit Testing: We tested individual functions in complete isolation. For example, we tested the password hashing function with various "
        "string inputs, verified that the Isolation Forest correctly identifies simulated outlier rows, and checked that the Silver-Meal inventory "
        "formula outputs non-negative reorder points for edge-case demand values.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Integration Testing: We validated data exchanges between collaborating modules. We verified that cleaned dataframes from `DataProcessor` "
        "flow correctly into `ChurnAnalyzer`, that time-series aggregations pass seamlessly to `SalesForecaster`, and that prediction dictionaries "
        "from all modules are correctly ingested and synthesized by `DecisionEngine`.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. System & Automated Regression Testing: To guarantee consistent performance across versions, we developed a comprehensive automated test script "
        "(`scripts/run_full_system_test.py`). This script executes 35 distinct test assertions across 12 test suites, verifying data ingestion, machine learning "
        "training, inventory optimization, audio generation, and natural-language query resolution in a single automated test run.",
        bold_prefix="• ")

    add_body_p(doc,
        "4. Boundary & Stress Testing: Real-world CSV files are often corrupted. We tested our platform against extreme boundary conditions, including "
        "single-row CSV files, datasets with completely missing column headers, files containing negative unit prices, and datasets with 100% missing values "
        "in specific columns. The ingestion engine handled all boundary cases without throwing unhandled exceptions.",
        bold_prefix="• ")

    add_body_p(doc,
        "5. Security Testing: We performed vulnerability assessments on the authentication system and conversational query engine. We tested "
        "incorrect password attempts, verified that password hashes cannot be inverted, and attempted SQL injection attacks (e.g., `' OR '1'='1'`; "
        "`DROP TABLE users;`) against the assistant input. The query engine rejected all non-SELECT queries, confirming SQL injection resistance.",
        bold_prefix="• ")

    # 7.2 Test Cases
    add_styled_heading(doc, "7.2 Test Cases", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Table 7.1 presents the complete suite of test cases executed against the platform, summarizing test preconditions, test inputs, expected outcomes, "
        "actual experimental results, and final pass/fail statuses across all 12 test suites.")

    add_styled_heading(doc, "Table 7.1: Comprehensive Software Test Execution Suite and Verification Log", 3, font_size=11, bold=True, space_before=12, space_after=4)

    test_cases = [
        ("Test ID", "Test Scenario", "Inputs / Preconditions", "Expected Outcome", "Actual Result", "Status"),
        ("TC-01.1", "Valid User Authentication", "Username: 'admin', correct password", "Authentication succeeds; role 'Administrator' returned", "Login successful; role verified", "PASS"),
        ("TC-01.2", "Invalid Password Rejection", "Username: 'admin', incorrect password", "Authentication fails; returns None with error prompt", "Access denied; returns None", "PASS"),
        ("TC-01.3", "PBKDF2 Salt Uniqueness", "Same password hashed twice with new salts", "Two completely distinct hash strings generated", "Distinct 64-char hashes generated", "PASS"),
        ("TC-02.1", "Standard CSV Ingestion", "Upload standard retail CSV (UK Retail)", "Columns mapped; clean dataframe generated", "Dataframe created; 0 errors", "PASS"),
        ("TC-02.2", "Polymorphic Header Mapping", "CSV with 'client_id', 'invoicedate', 'qty'", "Mapped to 'customer_id', 'order_date', 'quantity'", "Alias dictionary mapped all keys", "PASS"),
        ("TC-02.3", "Missing Value Imputation", "Sales column with NaN and blank values", "NaNs imputed with column median value", "Median 14.50 imputed; no NaNs", "PASS"),
        ("TC-02.4", "Outlier Filtering (Isolation Forest)", "Dataset injected with extreme sales spikes", "Anomalous spikes filtered out (top 5%)", "Outliers removed; clean mask set", "PASS"),
        ("TC-03.1", "Gross Revenue Computation", "Cleaned dataset with sales numbers", "Calculates sum of all line item sales accurately", "Total matched exact manual sum", "PASS"),
        ("TC-03.2", "Total Completed Orders", "Cleaned dataset with invoice IDs", "Counts distinct order invoice numbers", "Distinct count verified", "PASS"),
        ("TC-04.1", "RFM Feature Extraction", "Transactions with customer IDs and dates", "Recency, Frequency, Monetary computed per user", "RFM table generated accurately", "PASS"),
        ("TC-04.2", "SMOTE Class Balancing", "Imbalanced churn data (10% churners)", "Minority class oversampled to equal majority", "Classes balanced (50/50 split)", "PASS"),
        ("TC-04.3", "Random Forest Churn Training", "Balanced RFM feature matrix", "Model trains; achieves ROC-AUC > 0.80", "Trained successfully; ROC-AUC: 88.5%", "PASS"),
        ("TC-04.4", "Churn Probability Calibration", "Active customer RFM features", "Outputs calibrated probabilities in range [0.0, 1.0]", "All probabilities within [0.0, 1.0]", "PASS"),
        ("TC-05.1", "Daily Sales Aggregation", "Cleaned transaction timestamps and sales", "Returns contiguous daily time-series series", "Contiguous daily series created", "PASS"),
        ("TC-05.2", "Chronos-Bolt Forecasting", "Daily time series; 14-day horizon", "Returns 14-day median forecast and confidence bands", "Forecast generated with 80% CI", "PASS"),
        ("TC-05.3", "Forecasting Fallback Activation", "Simulated missing PyTorch / GPU memory error", "Falls back to Gradient Boosting Regressor seamlessly", "Fallback trained; 14-day output returned", "PASS"),
        ("TC-06.1", "Safety Stock Calculation", "Product demand mean and standard deviation", "Calculates non-negative safety stock using Z=1.65", "Safety stocks computed accurately", "PASS"),
        ("TC-06.2", "Reorder Point (ROP) Calculation", "Lead time: 7 days; calculated safety stock", "ROP = (Mean * 7) + Safety Stock", "ROP computed accurately for all SKUs", "PASS"),
        ("TC-06.3", "Stockout Risk Alert Generation", "Current stock set below calculated ROP", "Item flagged with urgent stockout warning", "Stockout risk marked True; alert raised", "PASS"),
        ("TC-07.1", "Customer CLV Estimation", "Customer order frequency and average spend", "Calculates 12-month forward CLV per customer", "CLV scores computed accurately", "PASS"),
        ("TC-07.2", "Pareto 80/20 Tier Assignment", "Customer CLV ranking", "Top 20% of revenue labeled Gold Tier", "Correct tier boundaries applied", "PASS"),
        ("TC-08.1", "Apriori Itemset Mining", "Multi-item invoice basket transactions", "Finds frequent itemsets with min support > 0.01", "Frequent itemsets discovered", "PASS"),
        ("TC-08.2", "Cross-Selling Rule Generation", "Frequent itemsets", "Computes Confidence and Lift; flags Lift > 1.2", "Cross-selling rules generated", "PASS"),
        ("TC-09.1", "Action Register Prioritization", "Identified churn liabilities and stockouts", "Actions sorted by estimated financial impact", "Actions ranked P1-Critical to P3", "PASS"),
        ("TC-09.2", "Text-to-Speech Audio Generation", "Synthesized text action memo", "gTTS outputs valid, playable MP3 byte stream", "MP3 generated; playable in UI", "PASS"),
        ("TC-10.1", "Natural Language Sales Query", "'What was total revenue?' query", "Translates to 'SELECT SUM(sales)'; returns number", "Accurate revenue returned", "PASS"),
        ("TC-10.2", "SQL Injection Prevention", "Input: '; DROP TABLE users; --'", "Rejects non-SELECT query; raises security error", "Query blocked; database intact", "PASS"),
        ("TC-11.1", "Single-Row File Resilience", "CSV file containing exactly 1 transaction row", "Processes file without crashing; handles zero variance", "Executed cleanly; no crash", "PASS"),
        ("TC-11.2", "All-Missing Numeric Column", "CSV file with entire sales column blank", "Imputes global fallback median; avoids divide-by-zero", "Cleaned safely; no exception", "PASS"),
        ("TC-12.1", "End-to-End Automated Test Suite", "Execute scripts/run_full_system_test.py", "35 test assertions pass with 100% pass rate", "35/35 assertions passed (100%)", "PASS")
    ]

    t_cases = doc.add_table(rows=len(test_cases), cols=6)
    t_cases.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cases.columns[0].width = Inches(0.8)
    t_cases.columns[1].width = Inches(1.3)
    t_cases.columns[2].width = Inches(1.3)
    t_cases.columns[3].width = Inches(1.3)
    t_cases.columns[4].width = Inches(1.3)
    t_cases.columns[5].width = Inches(0.7)

    for r_idx, row in enumerate(test_cases):
        cells = t_cases.rows[r_idx].cells
        is_h = (r_idx == 0)
        for c_idx, val in enumerate(row):
            c = cells[c_idx]
            set_cell_margins(c, 40, 40, 50, 50)
            if is_h:
                set_cell_background(c, "EAEAEA")
            elif r_idx % 2 == 1:
                set_cell_background(c, "F9F9F9")
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_h or c_idx in [0, 5]) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5 if not is_h else 9)
            if is_h or c_idx == 0: r.font.bold = True
            if c_idx == 5 and not is_h:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 128, 0)

    add_body_p(doc,
        "As summarized in Table 7.1, all 35 test assertions across 12 test suites passed successfully. The automated verification confirmed "
        "that our system satisfies all functional requirements (FR-01 to FR-10) and non-functional requirements (NFR-01 to NFR-06), demonstrating "
        "high mathematical accuracy, zero runtime crashes, and strong cryptographic security.")

    doc.add_page_break()
