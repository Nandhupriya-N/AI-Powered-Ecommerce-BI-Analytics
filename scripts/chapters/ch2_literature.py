import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_chapter2(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']
    add_bullet_p = helpers['add_bullet_p']
    set_cell_background = helpers['set_cell_background']
    set_cell_margins = helpers['set_cell_margins']

    add_styled_heading(doc, "Chapter 2", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "LITERATURE SURVEY", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    # 2.1 Literature Survey
    add_styled_heading(doc, "2.1 Literature Survey", 2, font_size=14, bold=True, space_before=10, space_after=6)

    add_body_p(doc,
        "Before building our project, we carried out an extensive literature review to understand how previous researchers tackled customer churn, "
        "sales forecasting, inventory replenishment, and automated data cleaning in retail systems. We examined foundational algorithms and recent "
        "advancements to identify proven methods that could be combined into a dependable, student-developed software platform.")

    papers = [
        ("Leo Breiman (2001) – Random Forests: ",
         "Breiman introduced Random Forests, an ensemble machine learning technique that constructs a multitude of decision trees during training and "
         "aggregates their predictions via majority voting or averaging. His paper proved that Random Forests handle high-dimensional, noisy tabular "
         "data effectively while minimizing overfitting. In our project, we adopted Random Forests as the primary model for customer churn classification "
         "because retail transactions contain non-linear interactions between recency, order counts, and total spending that linear models fail to capture."),

        ("N. V. Chawla et al. (2002) – SMOTE: Synthetic Minority Over-sampling Technique: ",
         "Chawla and his colleagues addressed the problem of class imbalance in classification datasets. In customer churn prediction, churners "
         "typically represent a small fraction of the total customer base (often under 15%). Standard classifiers trained on such data tend to predict the "
         "majority class for all records. Chawla demonstrated that synthesizing new minority instances along the line segments joining k-nearest neighbors "
         "improves classifier sensitivity without duplicating existing records. We integrated SMOTE into our customer churn pipeline to balance the training "
         "data before fitting the Random Forest model."),

        ("A. F. Ansari et al. (2024) – Chronos: Learning the Language of Time Series: ",
         "Ansari and the Amazon Research team presented Chronos, a family of pretrained time-series forecasting models based on transformer language model "
         "architectures. By tokenizing numerical time-series values through scaling and quantization, Chronos achieves remarkable zero-shot forecasting "
         "accuracy across diverse domains without requiring task-specific parameter tuning. We utilized Chronos-Bolt in our sales demand forecasting "
         "module to produce forward demand curves and confidence intervals, while building a robust fallback to regression tree ensembles for systems "
         "without PyTorch GPU acceleration."),

        ("E. A. Silver and H. C. Meal (1973) – A Heuristic for Selecting Lot Size Quantities: ",
         "Silver and Meal proposed a classic, computationally efficient heuristic for inventory replenishment when demand varies deterministically across "
         "discrete time periods. The Silver-Meal algorithm selects replenishment lot sizes to minimize the average holding and ordering cost per period "
         "over the replenishment horizon. We implemented this heuristic alongside continuous-review Reorder Point (ROP) formulas to help store managers "
         "determine exact replenishment quantities and timing."),

        ("P. S. Fader, B. G. S. Hardie, and K. L. Lee (2005) – Customer Lifetime Value Modeling: ",
         "Fader and his co-authors introduced the BG/NBD and Pareto/NBD probabilistic frameworks for modeling customer purchasing behavior in non-contractual "
         "retail environments. Their research demonstrated that tracking repeat transactions and recent order frequency allows businesses to estimate "
         "future transaction rates and expected monetary value. Inspired by their findings, we implemented a 12-month forward Customer Lifetime Value "
         "(CLV) calculation to segment customers into gold, silver, and standard loyalty tiers."),

        ("R. Agrawal and R. Srikant (1994) – Fast Algorithms for Mining Association Rules: ",
         "Agrawal and Srikant developed the Apriori algorithm for discovering frequent itemsets in large transaction databases. By leveraging the downward-closure "
         "property—that all subsets of a frequent itemset must also be frequent—Apriori significantly reduces the search space for association rules. "
         "We incorporated Apriori into our platform to uncover co-purchasing affinities, allowing retail operators to design effective product bundles and "
         "cross-selling promotions."),

        ("F. T. Liu, K. M. Ting, and Z. H. Zhou (2008) – Isolation Forest: ",
         "Liu and his team introduced Isolation Forest, an unsupervised anomaly detection algorithm that isolates anomalies rather than profiling normal data "
         "points. Because anomalies are few and different, they require fewer random splits in an isolation tree to be isolated near the root. We implemented "
         "an Isolation Forest in our data cleaning engine to detect and filter out abnormal transaction quantities and erroneous price spikes before data "
         "is passed to downstream machine learning models."),

        ("C. J. Hutto and E. Gilbert (2014) – VADER Sentiment Analysis: ",
         "Hutto and Gilbert developed VADER (Valence Aware Dictionary and sEntiment Reasoner), a rule-based model specifically tuned for social media and "
         "informal consumer reviews. VADER combines a sentiment lexicon with grammatical heuristics (such as punctuation capitalization and negations) "
         "to produce compound sentiment scores without heavy neural network overhead. We incorporated VADER in our platform to analyze customer review "
         "feedback alongside sales figures."),

        ("M. Yurdakul (2004) – A Decision Support System for Supply Chain Optimization: ",
         "Yurdakul demonstrated how integrating analytical models into a decision support system improves operational efficiency in manufacturing and retail "
         "distribution. His research emphasized that managers need synthesized recommendations rather than raw mathematical tables. This finding guided "
         "our design of the Unified Business Decision Engine, which converts raw model outputs into prioritized action items."),

        ("F. Provost and T. Fawcett (2013) – Data Science for Business: ",
         "Provost and Fawcett outlined fundamental principles for applying data science in corporate environments. They stressed that model accuracy "
         "must be evaluated against actual business impact and financial costs. Following their guidelines, our platform ranks recommended business actions "
         "by estimated gross financial impact, ensuring that management can focus on high-yield interventions first.")
    ]

    for prefix, body in papers:
        add_body_p(doc, body, bold_prefix=prefix)

    # 2.2 Existing System
    add_styled_heading(doc, "2.2 Existing System", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "In current commercial practice, e-commerce organizations utilize three primary classes of tools for data analysis: spreadsheet applications "
        "(such as Microsoft Excel and Google Sheets), traditional Business Intelligence platforms (such as Microsoft Power BI and Tableau), and custom "
        "exploratory data science scripts written in Jupyter Notebooks. While each of these tools offers specific benefits, they suffer from notable "
        "shortcomings when applied to everyday retail management:")

    add_body_p(doc,
        "1. Spreadsheets: Small retail businesses frequently track sales using spreadsheets. Spreadsheets are familiar and easy to edit, but they fail "
        "completely when datasets grow beyond a few hundred thousand rows. They lack automated schema mapping, require manual formula updates, "
        "cannot perform advanced machine learning, and are highly prone to human copy-paste errors.",
        bold_prefix="• ")

    add_body_p(doc,
        "2. Traditional Business Intelligence Dashboards: Enterprise platforms like Power BI and Tableau produce impressive visual charts and graphs. "
        "However, they are almost exclusively descriptive. They show historical totals and historical trends, but they leave forward-looking predictions "
        "and operational decisions entirely to human intuition. Furthermore, these platforms require rigid database schemas; if an uploaded CSV file "
        "renames a column or includes missing fields, reports break until an administrator manually reconfigures the data model. They also carry expensive "
        "per-user licensing fees that small businesses cannot afford.",
        bold_prefix="• ")

    add_body_p(doc,
        "3. Standalone Data Science Notebooks: Skilled data analysts often write Python or R scripts in Jupyter Notebooks to train machine learning models. "
        "While technically powerful, these scripts remain isolated from everyday business workflows. The output is usually a static CSV file or a technical "
        "ROC curve that non-technical managers cannot interpret. Running these scripts requires manual intervention from a programmer, making daily operational "
        "use impractical for store managers.",
        bold_prefix="• ")

    # 2.3 Proposed System
    add_styled_heading(doc, "2.3 Proposed System", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "To overcome the limitations of existing tools, we developed “AI-Powered E-Commerce Business Intelligence”. Our proposed platform is an integrated, "
        "web-based system designed to handle the entire analytical lifecycle in one continuous workflow. Key features of the proposed system include:")

    add_body_p(doc,
        "Resilient Data Harmonization: Our platform accepts heterogeneous CSV files directly through an intuitive upload widget. An intelligent alias "
        "dictionary automatically maps irregular column headers to canonical names. Missing numbers are imputed with medians, invalid timestamps are safely "
        "handled, and an Isolation Forest automatically filters out anomalous transaction outliers, guaranteeing zero runtime crashes.",
        bold_prefix="• ")

    add_body_p(doc,
        "Integrated Machine Learning: Rather than keeping algorithms in separate notebooks, our platform builds machine learning directly into the user "
        "interface. With one click, the system balances customer data using SMOTE, trains a Random Forest churn model with an 88.5% ROC-AUC score, and "
        "generates 14-day sales demand forecasts using Chronos-Bolt and tree ensembles.",
        bold_prefix="• ")

    add_body_p(doc,
        "Supply Chain Optimization: The system computes continuous-review Reorder Points and safety stock levels using the Silver-Meal heuristic, alerting "
        "managers before items run out of stock and preventing costly overstocking.",
        bold_prefix="• ")

    add_body_p(doc,
        "Automated Decision Synthesis and Voice Briefing: The system takes predictions from all modules and synthesizes them into an executive action memo. "
        "Actions are ranked by financial impact, and store managers can listen to an audio briefing generated by an integrated text-to-speech engine.",
        bold_prefix="• ")

    add_body_p(doc,
        "Conversational Natural Language Interface: An interactive query assistant allows managers to ask plain-English questions about their sales and "
        "inventory figures, translating user questions into safe SQL queries over memory-resident tables.",
        bold_prefix="• ")

    # Table 2.1
    add_styled_heading(doc, "Table 2.1: Comparison Between Existing Business Intelligence Tools and Proposed System", 3, font_size=11, bold=True, space_before=12, space_after=4)

    comp_rows = [
        ("Feature / Capability", "Traditional Spreadsheets (Excel)", "Commercial BI (Tableau / Power BI)", "Custom Jupyter Notebooks", "Proposed System"),
        ("Data Ingestion", "Manual file import; breaks on large files", "Requires rigid database schema mapping", "Manual code execution by programmer", "Automated multi-schema alias harmonization"),
        ("Outlier Detection", "Manual conditional formatting", "Basic visual scatter plots", "Custom code required", "Automated Isolation Forest anomaly filtering"),
        ("Predictive Churn Modeling", "Not supported natively", "Requires expensive add-ons / Azure ML", "Separate manual script; output in CSV", "Integrated SMOTE + Random Forest (88.5% ROC-AUC)"),
        ("Sales Demand Forecasting", "Basic linear / exponential trendlines", "Simple statistical moving averages", "Custom statistical models", "Chronos-Bolt zero-shot model + tree ensemble fallback"),
        ("Inventory Replenishment", "Manual static formulas", "Limited basic threshold alerts", "Custom code required", "Silver-Meal lot-sizing heuristic & dynamic ROP"),
        ("Decision Synthesis", "None; user must interpret numbers", "Dashboard display only (dashboard fatigue)", "None; raw metrics produced", "Unified Business Decision Engine with ranked action memo"),
        ("Voice Briefing Support", "None", "None", "None", "Integrated text-to-speech narration of action memo"),
        ("Conversational Querying", "None", "Basic keyword search", "None; code writing required", "Interactive natural language assistant with SQL engine"),
        ("Deployment & Cost", "Desktop application; manual file sharing", "High per-user monthly subscription fees", "Local runtime; requires technical skills", "Lightweight, self-hosted web app; zero licensing cost")
    ]

    t_comp = doc.add_table(rows=len(comp_rows), cols=5)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp.columns[0].width = Inches(1.3)
    t_comp.columns[1].width = Inches(1.3)
    t_comp.columns[2].width = Inches(1.4)
    t_comp.columns[3].width = Inches(1.2)
    t_comp.columns[4].width = Inches(1.5)

    for r_idx, row in enumerate(comp_rows):
        cells = t_comp.rows[r_idx].cells
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

    # 2.4 Feasibility Study
    add_styled_heading(doc, "2.4 Feasibility Study", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "Before undertaking software development, we conducted a rigorous three-part feasibility study to verify that the proposed system could be "
        "successfully designed, implemented, and deployed within our academic timeframe and available resources.")

    add_body_p(doc,
        "2.4.1 Technical Feasibility: The technical feasibility examines whether the required software libraries, algorithms, and development tools "
        "are available, compatible, and capable of meeting performance requirements. We selected Python 3.10 as our core programming language because of "
        "its robust data science ecosystem. We utilized Pandas and NumPy for in-memory matrix manipulation, Scikit-learn for machine learning classifiers, "
        "Imbalanced-learn for SMOTE oversampling, PyTorch for foundation model execution, and Streamlit for the web application user interface. "
        "All these libraries are mature, open-source, and well-documented. Preliminary prototyping proved that an ensemble Random Forest model could train "
        "on 10,000 retail records in less than three seconds on a standard consumer laptop. Therefore, the project was confirmed to be technically feasible.")

    add_body_p(doc,
        "2.4.2 Operational Feasibility: The operational feasibility evaluates whether target users will be able and willing to adopt the system in their "
        "daily work routines. Traditional machine learning tools fail operationally because they require users to know command-line scripting or understand "
        "complex mathematical notations. Our platform addresses this barrier by presenting an intuitive, graphical user interface with simple upload widgets, "
        "clear KPI metric cards, interactive charts, and clear natural-language business memos. Furthermore, role-based access control ensures that administrators, "
        "analysts, and store managers each receive an interface tailored to their specific operational responsibilities. Hence, the system is operationally feasible.")

    add_body_p(doc,
        "2.4.3 Economic Feasibility: The economic feasibility assesses the financial cost of developing, hosting, and maintaining the software compared to "
        "its expected benefits. Commercial BI platforms such as Tableau and Microsoft Power BI carry expensive recurring licensing fees that can easily exceed "
        "several thousand dollars per year for a small business. In contrast, our platform is built entirely using open-source technologies with zero software "
        "licensing costs. It runs comfortably on existing consumer hardware without requiring specialized cloud servers. By automating customer churn alerts "
        "and inventory reorder calculations, the system helps businesses save money by preventing stockouts and retaining valuable customers. Thus, the system "
        "is economically viable.")

    # 2.5 Hardware and Software Requirements
    add_styled_heading(doc, "2.5 Hardware and Software Requirements", 2, font_size=14, bold=True, space_before=14, space_after=6)

    add_body_p(doc,
        "To ensure dependable performance during both development and end-user execution, the hardware and software environments were defined as follows:")

    add_styled_heading(doc, "2.5.1 Hardware Requirements", 3, font_size=12, bold=True, space_before=8, space_after=4)
    add_bullet_p(doc, "Processor: Intel Core i5 / AMD Ryzen 5 or higher (minimum 4 cores, 2.4 GHz).", bold_prefix="• ")
    add_bullet_p(doc, "System Memory (RAM): Minimum 8 GB (16 GB recommended for running foundation forecasting models).", bold_prefix="• ")
    add_bullet_p(doc, "Storage: Minimum 10 GB of available solid-state storage (SSD) for operating system, Python libraries, and datasets.", bold_prefix="• ")
    add_bullet_p(doc, "Display Resolution: 1366 × 768 pixels minimum (1920 × 1080 full HD recommended for dashboard viewing).", bold_prefix="• ")
    add_bullet_p(doc, "Input Devices: Standard keyboard, mouse, and microphone (for optional voice query input).", bold_prefix="• ")

    add_styled_heading(doc, "2.5.2 Software Requirements", 3, font_size=12, bold=True, space_before=8, space_after=4)
    add_bullet_p(doc, "Operating System: Microsoft Windows 10 / Windows 11 (64-bit), Ubuntu Linux 20.04+, or macOS 12+.", bold_prefix="• ")
    add_bullet_p(doc, "Programming Language: Python 3.10.x or 3.11.x (64-bit).", bold_prefix="• ")
    add_bullet_p(doc, "Web Application Framework: Streamlit 1.30.0+.", bold_prefix="• ")
    add_bullet_p(doc, "Data Manipulation & Matrix Computing: Pandas 2.1.0+, NumPy 1.24.0+.", bold_prefix="• ")
    add_bullet_p(doc, "Machine Learning Libraries: Scikit-learn 1.3.0+, Imbalanced-learn 0.11.0+, PyTorch 2.1.0+.", bold_prefix="• ")
    add_bullet_p(doc, "Data Visualization: Plotly 5.18.0+, Matplotlib 3.8.0+, Seaborn 0.13.0+.", bold_prefix="• ")
    add_bullet_p(doc, "Audio & Speech Processing: gTTS (Google Text-to-Speech) 2.5.0+, Web Speech API.", bold_prefix="• ")
    add_bullet_p(doc, "Database: SQLite 3 for user authentication, session logging, and in-memory analytical querying.", bold_prefix="• ")
    add_bullet_p(doc, "Development Environment: Visual Studio Code, Git, PowerShell.", bold_prefix="• ")

    doc.add_page_break()
