import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# ==========================================
# 1. FIG 5.1: ACTIVITY DIAGRAM (White Background)
# ==========================================
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(11, 10), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 13)
    ax.axis('off')

    # Start Node
    start = patches.Circle((5.5, 12.3), 0.22, facecolor='black', edgecolor='black')
    ax.add_patch(start)
    ax.text(5.5, 12.7, "Start Session", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827')

    activities = [
        {"id": "A1", "text": "1. User Authentication &\nRBAC Credential Check", "pos": (4.0, 10.9), "w": 3.0, "h": 0.9},
        {"id": "A2", "text": "2. Select Preloaded Scenario or\nUpload Heterogeneous CSV", "pos": (4.0, 9.4), "w": 3.0, "h": 0.9},
        {"id": "A3", "text": "3. Automated Schema Harmonization &\nIsolation Forest Outlier Filtering", "pos": (4.0, 7.9), "w": 3.0, "h": 0.9},
    ]

    for a in activities:
        box = patches.FancyBboxPatch(
            a["pos"], a["w"], a["h"],
            boxstyle="round,pad=0.1,rounding_size=0.2",
            edgecolor="#2563EB", facecolor="#EFF6FF", linewidth=1.8
        )
        ax.add_patch(box)
        ax.text(a["pos"][0] + a["w"]/2, a["pos"][1] + a["h"]/2, a["text"],
                ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1E3A8A")

    # Connectors Start -> A1 -> A2 -> A3
    ax.annotate("", xy=(5.5, 11.8), xytext=(5.5, 12.1), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    ax.annotate("", xy=(5.5, 10.3), xytext=(5.5, 10.9), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    ax.annotate("", xy=(5.5, 8.8), xytext=(5.5, 9.4), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))

    # Fork Bar (Parallel Execution)
    fork_bar = patches.Rectangle((1.0, 7.2), 9.0, 0.12, facecolor="#1F2937", edgecolor="#1F2937")
    ax.add_patch(fork_bar)
    ax.annotate("", xy=(5.5, 7.32), xytext=(5.5, 7.9), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    ax.text(5.5, 7.45, "[Parallel Inference Fork]", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#4B5563")

    # 4 Parallel Threads
    threads = [
        {"title": "4A: Churn Modeling", "desc": "SMOTE Balancing +\nRF Probabilities & XAI", "x": 1.0, "col": "#DCFCE7", "bdr": "#16A34A"},
        {"title": "4B: Sales Forecaster", "desc": "Chronos-Bolt &\nTree Multi-Horizon", "x": 3.3, "col": "#FEF3C7", "bdr": "#D97706"},
        {"title": "4C: Inventory ROP", "desc": "Silver-Meal Formula\n& Safety Stocking", "x": 5.6, "col": "#F3E8FF", "bdr": "#9333EA"},
        {"title": "4D: CLV & Basket", "desc": "12-Month CLV &\nApriori Rules Mining", "x": 7.9, "col": "#E0E7FF", "bdr": "#3730A3"},
    ]

    for t in threads:
        ax.annotate("", xy=(t["x"] + 1.05, 6.3), xytext=(t["x"] + 1.05, 7.2), arrowprops=dict(arrowstyle="->", lw=1.5, color=t["bdr"]))
        box = patches.FancyBboxPatch(
            (t["x"], 5.1), 2.1, 1.2,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            edgecolor=t["bdr"], facecolor=t["col"], linewidth=1.6
        )
        ax.add_patch(box)
        ax.text(t["x"] + 1.05, 5.95, t["title"], ha='center', va='center', fontsize=8, fontweight='bold', color="#111827")
        ax.text(t["x"] + 1.05, 5.45, t["desc"], ha='center', va='center', fontsize=7.2, color="#374151")

    # Join Bar
    join_bar = patches.Rectangle((1.0, 4.4), 9.0, 0.12, facecolor="#1F2937", edgecolor="#1F2937")
    ax.add_patch(join_bar)
    for t in threads:
        ax.annotate("", xy=(t["x"] + 1.05, 4.52), xytext=(t["x"] + 1.05, 5.1), arrowprops=dict(arrowstyle="->", lw=1.5, color=t["bdr"]))
    ax.text(5.5, 4.25, "[Join Parallel Threads]", ha='center', va='top', fontsize=8, fontweight='bold', color="#4B5563")

    # Activity 5: Prescriptive Synthesis
    ax.annotate("", xy=(5.5, 3.4), xytext=(5.5, 4.4), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    a5_box = patches.FancyBboxPatch(
        (3.7, 2.5), 3.6, 0.9,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        edgecolor="#E11D48", facecolor="#FFE4E6", linewidth=1.8
    )
    ax.add_patch(a5_box)
    ax.text(5.5, 2.95, "5. Unified Prescriptive Engine:\nCross-Module Risk Ranking & ROI Scoring", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#881337")

    # Activity 6: Multi-Modal Output & Audio
    ax.annotate("", xy=(5.5, 1.9), xytext=(5.5, 2.5), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    a6_box = patches.FancyBboxPatch(
        (3.5, 1.0), 4.0, 0.9,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        edgecolor="#0284C7", facecolor="#E0F2FE", linewidth=1.8
    )
    ax.add_patch(a6_box)
    ax.text(5.5, 1.45, "6. Render Reactive Plotly Visuals, Memo &\nSynthesize gTTS Executive Audio Narration", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#0369A1")

    # End Node (Bullseye)
    ax.annotate("", xy=(5.5, 0.5), xytext=(5.5, 1.0), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E3A8A"))
    end_outer = patches.Circle((5.5, 0.3), 0.22, facecolor='white', edgecolor='black', linewidth=1.5)
    end_inner = patches.Circle((5.5, 0.3), 0.14, facecolor='black', edgecolor='black')
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)
    ax.text(5.5, 0.0, "End Session", ha='center', va='center', fontsize=9, fontweight='bold', color='#111827')

    ax.set_title("Figure 5.1: Activity Diagram for MasterMind AI Analytical Lifecycle", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig5_1_activity_diagram.png", dpi=300, facecolor='white')
    plt.close()
    print("Saved diagrams/fig5_1_activity_diagram.png")

# ==========================================
# 2. FIG 5.2: USE CASE DIAGRAM (White Background)
# ==========================================
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # System Boundary Box
    boundary = patches.FancyBboxPatch(
        (2.8, 0.4), 6.0, 8.2,
        boxstyle="round,pad=0.15,rounding_size=0.2",
        edgecolor="#1E3A8A", facecolor="#FAFAFA", linewidth=2.2
    )
    ax.add_patch(boundary)
    ax.text(5.8, 8.35, "MasterMind AI Platform Boundary", ha='center', va='center', fontsize=11, fontweight='bold', color="#1E3A8A")

    # Use Cases (Ovals)
    use_cases = [
        {"name": "UC-01: Authenticate & Authorize (PBKDF2)", "y": 7.7, "color": "#E0E7FF"},
        {"name": "UC-02: Upload & Harmonize Multi-Schema CSV", "y": 7.0, "color": "#FEF3C7"},
        {"name": "UC-03: View Executive Descriptive KPIs & Visuals", "y": 6.3, "color": "#EFF6FF"},
        {"name": "UC-04: Execute Churn Prediction & Inspect XAI", "y": 5.6, "color": "#DCFCE7"},
        {"name": "UC-05: Multi-Horizon Sales Forecasting (Chronos)", "y": 4.9, "color": "#DCFCE7"},
        {"name": "UC-06: Inventory ROP & Safety Stock Optimization", "y": 4.2, "color": "#DCFCE7"},
        {"name": "UC-07: 12-Month CLV & Pareto Segmentation", "y": 3.5, "color": "#DCFCE7"},
        {"name": "UC-08: Association Mining & Sentiment NLP", "y": 2.8, "color": "#DCFCE7"},
        {"name": "UC-09: Prescriptive Decision Memo & Audio Playback", "y": 2.1, "color": "#FFE4E6"},
        {"name": "UC-10: Conversational Assistant & Viva Defense QA", "y": 1.4, "color": "#F3E8FF"},
        {"name": "UC-11: Data Drift Audit & Statistical Validation", "y": 0.7, "color": "#F1F5F9"},
    ]

    for uc in use_cases:
        oval = patches.FancyBboxPatch(
            (3.2, uc["y"] - 0.22), 5.2, 0.48,
            boxstyle="round,pad=0.1,rounding_size=0.25",
            edgecolor="#475569", facecolor=uc["color"], linewidth=1.3
        )
        ax.add_patch(oval)
        ax.text(5.8, uc["y"], uc["name"], ha='center', va='center', fontsize=8, fontweight='bold', color="#1E293B")

    # Helper function to draw stick figures
    def draw_actor(x, y, label, col="#1E40AF"):
        head = patches.Circle((x, y + 0.35), 0.18, facecolor="white", edgecolor=col, linewidth=1.8)
        ax.add_patch(head)
        ax.plot([x, x], [y + 0.17, y - 0.25], color=col, lw=1.8) # body
        ax.plot([x - 0.25, x + 0.25], [y + 0.05, y + 0.05], color=col, lw=1.8) # arms
        ax.plot([x, x - 0.2], [y - 0.25, y - 0.6], color=col, lw=1.8) # left leg
        ax.plot([x, x + 0.2], [y - 0.25, y - 0.6], color=col, lw=1.8) # right leg
        ax.text(x, y - 0.82, label, ha='center', va='center', fontsize=8, fontweight='bold', color="#111827")

    # Actors
    draw_actor(1.2, 7.3, "C-Suite Executive /\nBusiness Leader", "#6D28D9")
    draw_actor(1.2, 2.5, "BI Specialist /\nData Analyst", "#1E40AF")
    draw_actor(10.3, 7.3, "System Administrator /\nSecurity Officer", "#B45309")
    draw_actor(10.3, 2.5, "Supply Chain &\nStore Manager", "#15803D")

    # Actor Connections
    # Executive -> UC-01, UC-03, UC-09, UC-10
    for y_tgt in [7.7, 6.3, 2.1, 1.4]:
        ax.plot([1.5, 3.2], [7.1, y_tgt], color="#6D28D9", lw=1.2, linestyle="--")

    # Data Analyst -> UC-01, UC-02, UC-04, UC-05, UC-07, UC-08, UC-10, UC-11
    for y_tgt in [7.7, 7.0, 5.6, 4.9, 3.5, 2.8, 1.4, 0.7]:
        ax.plot([1.5, 3.2], [2.5, y_tgt], color="#1E40AF", lw=1.2)

    # Admin -> UC-01, UC-11
    for y_tgt in [7.7, 0.7]:
        ax.plot([10.0, 8.4], [7.1, y_tgt], color="#B45309", lw=1.2)

    # Supply Chain Manager -> UC-01, UC-05, UC-06, UC-09
    for y_tgt in [7.7, 4.9, 4.2, 2.1]:
        ax.plot([10.0, 8.4], [2.5, y_tgt], color="#15803D", lw=1.2)

    ax.set_title("Figure 5.2: Use Case Diagram of MasterMind AI Platform", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig5_2_use_case_diagram.png", dpi=300, facecolor='white')
    plt.close()
    print("Saved diagrams/fig5_2_use_case_diagram.png")

# ==========================================
# 3. FIG 5.3: CLASS DIAGRAM (White Background)
# ==========================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')

    classes = [
        {"name": "AuthManager (src/auth_db.py)", "pos": (0.5, 5.8), "w": 3.3, "h": 2.7, "col": "#EDE9FE", "bdr": "#7C3AED",
         "attrs": ["- db_path: str", "- salt_iterations: int = 100000", "- current_user: str", "- current_role: str"],
         "methods": ["+ hash_password(pwd): (bytes, bytes)", "+ verify_user(uname, pwd): (bool, role)", "+ log_activity(uname, role, action, meta)", "+ get_audit_trail(limit): DataFrame"]},

        {"name": "DataHarmonizer (src/data_processor.py)", "pos": (4.3, 5.8), "w": 3.4, "h": 2.7, "col": "#FEF3C7", "bdr": "#D97706",
         "attrs": ["- schema_aliases: dict", "- outlier_contamination: float = 0.05", "- canonical_cols: list"],
         "methods": ["+ harmonize_dataset(df): (df, mapping, type)", "+ filter_outliers(df): (df, anomalies)", "+ synthesize_rfm(df): DataFrame", "+ get_data_quality_report(): dict"]},

        {"name": "MLIntelligenceSuite (src/analyzer.py)", "pos": (8.2, 5.8), "w": 3.3, "h": 2.7, "col": "#DCFCE7", "bdr": "#16A34A",
         "attrs": ["- model_churn: RandomForestClassifier", "- smote_sampler: SMOTE", "- forecaster: ChronosBolt", "- clv_model: GradientBoostingRegressor"],
         "methods": ["+ train_churn_model(X, y): (clf, metrics)", "+ predict_churn_risk(df): (df, xai_feat)", "+ forecast_demand(df, steps): DataFrame", "+ compute_clv_tiers(df): DataFrame"]},

        {"name": "InventoryOptimizer (src/inventory_optimizer.py)", "pos": (0.5, 1.0), "w": 3.3, "h": 3.8, "col": "#E0F2FE", "bdr": "#0284C7",
         "attrs": ["- service_level_z: float = 1.645", "- holding_cost_pct: float = 0.20", "- order_cost: float = 50.0"],
         "methods": ["+ calculate_rop(mean_d, std_d, lead_time): float", "+ compute_safety_stock(std_d, lead_time): float", "+ evaluate_stockout_risk(inv_df): list", "+ recommend_reorder_qty(eoq_params): dict"]},

        {"name": "DecisionEngine (src/decision_engine.py)", "pos": (4.3, 1.0), "w": 3.4, "h": 3.8, "col": "#FFE4E6", "bdr": "#E11D48",
         "attrs": ["- risk_weights: dict", "- roi_multipliers: dict", "- max_priority_count: int = 5"],
         "methods": ["+ aggregate_cross_module_risks(data): list", "+ compute_revenue_impact(risk_item): float", "+ generate_decision_memo(): str", "+ simulate_what_if_scenario(sliders): dict"]},

        {"name": "NLAssistantBot (src/nl_assistant.py)", "pos": (8.2, 1.0), "w": 3.3, "h": 3.8, "col": "#F5F3FF", "bdr": "#9333EA",
         "attrs": ["- academic_qa_bank: dict", "- speech_voice: str = 'en'", "- tts_engine: gTTS"],
         "methods": ["+ answer_query(query, context): str", "+ explain_academic_concept(topic): str", "+ synthesize_speech(text): bytes", "+ query_sql_in_memory(sql_str): DataFrame"]}
    ]

    for c in classes:
        # Outer box
        box = patches.FancyBboxPatch(
            c["pos"], c["w"], c["h"],
            boxstyle="round,pad=0.05,rounding_size=0.1",
            edgecolor=c["bdr"], facecolor="white", linewidth=1.8
        )
        ax.add_patch(box)

        # Title Header
        header = patches.FancyBboxPatch(
            c["pos"], c["w"], 0.45,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            edgecolor=c["bdr"], facecolor=c["col"], linewidth=1.2
        )
        # Position header at the top
        header_y = c["pos"][1] + c["h"] - 0.45
        header.set_y(header_y)
        ax.add_patch(header)
        ax.text(c["pos"][0] + c["w"]/2, header_y + 0.22, c["name"], ha='center', va='center', fontsize=7.8, fontweight='bold', color="#1E293B")

        # Dividing Line 1 (Attributes)
        curr_y = header_y - 0.15
        for attr in c["attrs"]:
            ax.text(c["pos"][0] + 0.15, curr_y, attr, ha='left', va='center', fontsize=7, color="#334155")
            curr_y -= 0.22

        # Dividing line between attrs and methods
        curr_y -= 0.05
        ax.plot([c["pos"][0] + 0.05, c["pos"][0] + c["w"] - 0.05], [curr_y, curr_y], color=c["bdr"], lw=0.8, linestyle=":")
        curr_y -= 0.18

        # Methods
        for m in c["methods"]:
            ax.text(c["pos"][0] + 0.15, curr_y, m, ha='left', va='center', fontsize=7, color="#0F172A")
            curr_y -= 0.22

    # Associations
    # DataHarmonizer -> MLIntelligenceSuite (Dependency / Association)
    ax.annotate("", xy=(8.2, 7.15), xytext=(7.7, 7.15), arrowprops=dict(arrowstyle="->", lw=1.6, color="#16A34A"))
    ax.text(7.95, 7.3, "feeds", ha='center', va='bottom', fontsize=7, fontweight='bold', color="#16A34A")

    # MLIntelligenceSuite -> DecisionEngine (Dependency)
    ax.annotate("", xy=(7.7, 3.8), xytext=(8.4, 5.8), arrowprops=dict(arrowstyle="->", lw=1.6, color="#E11D48"))
    ax.text(8.2, 4.8, "supplies metrics", ha='left', va='center', fontsize=7, fontweight='bold', color="#E11D48")

    # InventoryOptimizer -> DecisionEngine
    ax.annotate("", xy=(4.3, 3.0), xytext=(3.8, 3.0), arrowprops=dict(arrowstyle="->", lw=1.6, color="#E11D48"))
    ax.text(4.05, 3.15, "stockout risks", ha='center', va='bottom', fontsize=7, fontweight='bold', color="#E11D48")

    # DecisionEngine -> NLAssistantBot
    ax.annotate("", xy=(8.2, 3.0), xytext=(7.7, 3.0), arrowprops=dict(arrowstyle="<->", lw=1.6, color="#9333EA"))
    ax.text(7.95, 3.15, "synthesizes audio", ha='center', va='bottom', fontsize=7, fontweight='bold', color="#9333EA")

    ax.set_title("Figure 5.3: Object-Oriented Class Diagram of MasterMind AI Core Architecture", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig5_3_class_diagram.png", dpi=300, facecolor='white')
    plt.close()
    print("Saved diagrams/fig5_3_class_diagram.png")

# ==========================================
# 4. FIG 5.4: SEQUENCE DIAGRAM (White Background)
# ==========================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 9.5), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 10.5)
    ax.axis('off')

    actors = [
        {"name": "User / Executive\n(Actor)", "x": 1.0, "col": "#EDE9FE"},
        {"name": "Streamlit App\n(Presentation UI)", "x": 3.0, "col": "#E0F2FE"},
        {"name": "AuthManager\n(Security Control)", "x": 5.0, "col": "#FEF3C7"},
        {"name": "DataHarmonizer\n(ETL Engine)", "x": 7.0, "col": "#DCFCE7"},
        {"name": "ML & Decision\nEngines (Analytics)", "x": 9.0, "col": "#FFE4E6"},
        {"name": "Audio & Speech\n(gTTS / Voice API)", "x": 10.5, "col": "#F3E8FF"},
    ]

    # Draw Actor Boxes & Lifelines
    for a in actors:
        box = patches.FancyBboxPatch(
            (a["x"] - 0.7, 9.5), 1.4, 0.75,
            boxstyle="round,pad=0.08,rounding_size=0.1",
            edgecolor="#334155", facecolor=a["col"], linewidth=1.5
        )
        ax.add_patch(box)
        ax.text(a["x"], 9.87, a["name"], ha='center', va='center', fontsize=7.5, fontweight='bold', color="#0F172A")
        # Lifeline (dashed line down)
        ax.plot([a["x"], a["x"]], [0.8, 9.5], color="#94A3B8", lw=1.2, linestyle="--")

    # Sequence Messages
    messages = [
        {"y": 9.0, "x1": 1.0, "x2": 3.0, "text": "1: Submit Login Credentials (uname, pwd)", "style": "->", "ret": False},
        {"y": 8.5, "x1": 3.0, "x2": 5.0, "text": "2: verify_user(uname, pwd) [PBKDF2-SHA256]", "style": "->", "ret": False},
        {"y": 8.0, "x1": 5.0, "x2": 3.0, "text": "3: Auth Token & Role Granted (Admin/Exec)", "style": "->", "ret": True},
        {"y": 7.4, "x1": 1.0, "x2": 3.0, "text": "4: Upload Raw CSV / Select Retail Dataset", "style": "->", "ret": False},
        {"y": 6.8, "x1": 3.0, "x2": 7.0, "text": "5: harmonize_dataset(df) & filter_outliers()", "style": "->", "ret": False},
        {"y": 6.2, "x1": 7.0, "x2": 3.0, "text": "6: Return Cleaned Canonical Schema Frame", "style": "->", "ret": True},
        {"y": 5.6, "x1": 3.0, "x2": 9.0, "text": "7: Execute Parallel Inference (Churn, Forecast, ROP, CLV)", "style": "->", "ret": False},
        {"y": 4.8, "x1": 9.0, "x2": 9.0, "text": "8: DecisionEngine synthesizes cross-module risks & ROI", "style": "loop", "ret": False},
        {"y": 4.1, "x1": 9.0, "x2": 3.0, "text": "9: Return Scored Registers, Forecast Intervals & Decision Memo", "style": "->", "ret": True},
        {"y": 3.4, "x1": 3.0, "x2": 10.5, "text": "10: synthesize_speech(decision_summary_text)", "style": "->", "ret": False},
        {"y": 2.8, "x1": 10.5, "x2": 3.0, "text": "11: Return Streaming MP3 Audio Buffer", "style": "->", "ret": True},
        {"y": 2.1, "x1": 3.0, "x2": 1.0, "text": "12: Render Reactive Charts, Memo & Autoplay Audio Brief", "style": "->", "ret": True},
        {"y": 1.4, "x1": 1.0, "x2": 3.0, "text": "13: Dictate Voice Query via Web Speech API Mic", "style": "->", "ret": False},
    ]

    for m in messages:
        if m["style"] == "loop":
            # Self call on analytics engine
            ax.plot([m["x1"], m["x1"] + 0.4, m["x1"] + 0.4, m["x1"]], [m["y"] + 0.15, m["y"] + 0.15, m["y"] - 0.15, m["y"] - 0.15],
                    color="#E11D48", lw=1.5)
            ax.annotate("", xy=(m["x1"], m["y"] - 0.15), xytext=(m["x1"] + 0.05, m["y"] - 0.15), arrowprops=dict(arrowstyle="->", lw=1.5, color="#E11D48"))
            ax.text(m["x1"] + 0.5, m["y"], m["text"], ha='left', va='center', fontsize=7.5, fontweight='bold', color="#BE123C")
        else:
            col = "#2563EB" if not m["ret"] else "#16A34A"
            ls = "-" if not m["ret"] else "--"
            ax.annotate("", xy=(m["x2"], m["y"]), xytext=(m["x1"], m["y"]),
                        arrowprops=dict(arrowstyle="->", lw=1.5, color=col, linestyle=ls))
            mid_x = (m["x1"] + m["x2"]) / 2
            ax.text(mid_x, m["y"] + 0.12, m["text"], ha='center', va='bottom', fontsize=7.5, fontweight='bold', color="#1E293B")

    ax.set_title("Figure 5.4: Sequence Diagram for End-to-End Analytics & Decision Generation Workflow", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig5_4_sequence_diagram.png", dpi=300, facecolor='white')
    plt.close()
    print("Saved diagrams/fig5_4_sequence_diagram.png")

if __name__ == "__main__":
    generate_activity_diagram()
    generate_use_case_diagram()
    generate_class_diagram()
    generate_sequence_diagram()
    print("All Detailed Design diagrams generated successfully!")
