import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure diagrams directory exists
os.makedirs("diagrams", exist_ok=True)

# Set common font styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# ==========================================
# 1. FIG 4.1: CONTEXT DIAGRAM (Level-0 DFD)
# ==========================================
def generate_context_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Central System
    center_circle = patches.FancyBboxPatch(
        (3.8, 2.7), 3.4, 2.1,
        boxstyle="round,pad=0.2,rounding_size=0.4",
        edgecolor="#1E3A8A", facecolor="#DBEAFE", linewidth=2.5
    )
    ax.add_patch(center_circle)
    ax.text(5.5, 3.9, "0.0\nMasterMind AI Platform", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(5.5, 3.2, "(AI-Powered E-Commerce BI\n& Predictive Analytics)", ha='center', va='center', fontsize=9.5, style='italic', color="#1E40AF")

    # Entities (Rectangles)
    entities = [
        {"name": "Enterprise Data Sources\n(Multi-Schema CSV / POS)", "pos": (0.6, 5.2), "size": (2.4, 1.2), "color": "#FEF3C7", "border": "#B45309"},
        {"name": "Executive & C-Suite\n(Strategic Decision Makers)", "pos": (8.0, 5.2), "size": (2.4, 1.2), "color": "#EDE9FE", "border": "#6D28D9"},
        {"name": "BI & Data Analysts\n(Technical Evaluators)", "pos": (0.6, 1.1), "size": (2.4, 1.2), "color": "#E0E7FF", "border": "#3730A3"},
        {"name": "Operations & Inventory\nManagers (Supply Chain)", "pos": (8.0, 1.1), "size": (2.4, 1.2), "color": "#DCFCE7", "border": "#15803D"},
    ]

    for ent in entities:
        rect = patches.FancyBboxPatch(
            ent["pos"], ent["size"][0], ent["size"][1],
            boxstyle="round,pad=0.1,rounding_size=0.15",
            edgecolor=ent["border"], facecolor=ent["color"], linewidth=2
        )
        ax.add_patch(rect)
        cx = ent["pos"][0] + ent["size"][0] / 2
        cy = ent["pos"][1] + ent["size"][1] / 2
        ax.text(cx, cy, ent["name"], ha='center', va='center', fontsize=9.5, fontweight='bold', color="#1F2937")

    # Arrows and Labels
    # 1. Data Sources -> System
    ax.annotate("", xy=(3.8, 4.3), xytext=(2.9, 5.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#B45309"))
    ax.text(3.1, 4.9, "Raw Orders, Customers,\nProducts, Reviews", ha='right', va='center', fontsize=8, color="#78350F", fontweight='bold')

    # 2. System -> Executive
    ax.annotate("", xy=(8.0, 5.4), xytext=(7.1, 4.3), arrowprops=dict(arrowstyle="->", lw=1.8, color="#6D28D9"))
    ax.text(7.7, 4.9, "Executive Decision Memo,\nKPIs & Voice Narration", ha='left', va='center', fontsize=8, color="#4C1D95", fontweight='bold')

    # Executive -> System (Feedback/Filter)
    ax.annotate("", xy=(7.0, 4.0), xytext=(8.0, 5.1), arrowprops=dict(arrowstyle="->", lw=1.2, color="#6D28D9", linestyle="--"))
    ax.text(7.6, 4.35, "Scenario Sliders", ha='left', va='center', fontsize=7.5, color="#6D28D9")

    # 3. BI Analyst <-> System
    ax.annotate("", xy=(3.8, 3.2), xytext=(2.9, 2.1), arrowprops=dict(arrowstyle="->", lw=1.8, color="#3730A3"))
    ax.text(3.1, 2.8, "Uploads, SQL Queries,\nWhat-If Parameters", ha='right', va='center', fontsize=8, color="#312E81", fontweight='bold')

    ax.annotate("", xy=(2.9, 1.8), xytext=(3.9, 2.9), arrowprops=dict(arrowstyle="->", lw=1.8, color="#3730A3"))
    ax.text(3.2, 2.2, "PSI Drift Metrics, XAI Plots,\nHarmonized Data Exports", ha='right', va='center', fontsize=7.5, color="#3730A3")

    # 4. System -> Operations Manager
    ax.annotate("", xy=(8.0, 2.0), xytext=(7.1, 3.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#15803D"))
    ax.text(7.7, 2.7, "Reorder Triggers (ROP),\nStockout Risk Schedules", ha='left', va='center', fontsize=8, color="#14532D", fontweight='bold')

    ax.set_title("Figure 4.1: Context Diagram (Level-0 DFD) of MasterMind AI Platform", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig4_1_context_diagram.png", dpi=300)
    plt.close()
    print("Saved diagrams/fig4_1_context_diagram.png")

# ==========================================
# 2. FIG 4.2: SYSTEM PERSPECTIVE DIAGRAM
# ==========================================
def generate_perspective_diagram():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    tiers = [
        {"title": "1. User & Client Interface Tier", "y": 6.3, "h": 1.25, "bg": "#EFF6FF", "border": "#3B82F6",
         "items": ["Modern Web Browser (Chrome / Edge / Firefox)", "Microphone Audio (Web Speech API)", "Interactive Audio Speaker (gTTS Narration)"]},
        {"title": "2. Web Presentation & Application Tier", "y": 4.5, "h": 1.4, "bg": "#F5F3FF", "border": "#8B5CF6",
         "items": ["Streamlit Reactive Application Server (Port 8501)", "Session State Management & Page Routing (16 Functional Views)", "Plotly Dynamic Charting & Custom CSS Glassmorphism Engine"]},
        {"title": "3. Analytics & Machine Learning Inference Tier", "y": 2.2, "h": 1.9, "bg": "#F0FDF4", "border": "#22C55E",
         "items": ["Schema Harmonization & Outlier Imputation (Isolation Forest)", "Random Forest Churn Engine with SMOTE & Feature Importance", "Amazon Chronos-Bolt Foundation Forecaster & Ensemble Regressors", "CLV Prediction Engine & Pareto Tiering", "Silver-Meal Inventory Reorder Engine (ROP & Safety Stock)", "Apriori Association Mining & VADER Aspect Sentiment Engine"]},
        {"title": "4. Enterprise Data & Persistence Tier", "y": 0.4, "h": 1.4, "bg": "#FFFBEB", "border": "#F59E0B",
         "items": ["SQLite Relational Database (ecommerce_bi.db - PBKDF2 Auth & Immutable Audit)", "Persistent Serialization Store (models/*.pkl, scaler binaries)", "Standardized Analytical Store (Pandas In-Memory Frames, CSV/PDF Artifacts)"]}
    ]

    for t in tiers:
        # Tier container
        box = patches.FancyBboxPatch(
            (0.8, t["y"]), 9.4, t["h"],
            boxstyle="round,pad=0.15,rounding_size=0.18",
            edgecolor=t["border"], facecolor=t["bg"], linewidth=2
        )
        ax.add_patch(box)
        # Title badge
        title_box = patches.FancyBboxPatch(
            (1.0, t["y"] + t["h"] - 0.28), 4.2, 0.35,
            boxstyle="round,pad=0.08,rounding_size=0.1",
            edgecolor=t["border"], facecolor=t["border"], linewidth=1
        )
        ax.add_patch(title_box)
        ax.text(1.1, t["y"] + t["h"] - 0.11, t["title"], fontsize=9.5, fontweight='bold', color="white")

        # Content bullets
        num_items = len(t["items"])
        if num_items <= 3:
            for idx, itm in enumerate(t["items"]):
                item_box = patches.FancyBboxPatch(
                    (1.1 + idx * 3.0, t["y"] + 0.15), 2.8, t["h"] - 0.55,
                    boxstyle="round,pad=0.05,rounding_size=0.1",
                    edgecolor="#CBD5E1", facecolor="white", linewidth=1.2
                )
                ax.add_patch(item_box)
                ax.text(1.1 + idx * 3.0 + 1.4, t["y"] + 0.15 + (t["h"] - 0.55)/2, itm,
                        ha='center', va='center', fontsize=8, fontweight='semibold', color="#1F2937", wrap=True)
        else:
            # 2x3 grid for intelligence tier
            coords = [
                (1.1, t["y"] + 0.8), (4.1, t["y"] + 0.8), (7.1, t["y"] + 0.8),
                (1.1, t["y"] + 0.15), (4.1, t["y"] + 0.15), (7.1, t["y"] + 0.15)
            ]
            for idx, itm in enumerate(t["items"]):
                pos = coords[idx]
                item_box = patches.FancyBboxPatch(
                    pos, 2.8, 0.55,
                    boxstyle="round,pad=0.05,rounding_size=0.08",
                    edgecolor="#CBD5E1", facecolor="white", linewidth=1.2
                )
                ax.add_patch(item_box)
                ax.text(pos[0] + 1.4, pos[1] + 0.27, itm, ha='center', va='center', fontsize=7.5, fontweight='semibold', color="#1F2937")

    # Connectors between tiers
    for y_conn in [6.15, 4.35, 2.05]:
        ax.annotate("", xy=(5.5, y_conn - 0.15), xytext=(5.5, y_conn + 0.15),
                    arrowprops=dict(arrowstyle="<->", lw=2, color="#475569"))

    ax.set_title("Figure 4.2: System Perspective & Tiered Deployment Architecture", fontsize=13, fontweight='bold', pad=15, color="#111827")
    plt.tight_layout()
    plt.savefig("diagrams/fig4_2_system_perspective.png", dpi=300)
    plt.close()
    print("Saved diagrams/fig4_2_system_perspective.png")

# ==========================================
# 3. FIG 4.3: SYSTEM ARCHITECTURE DIAGRAM
# ==========================================
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    layers = [
        {"name": "Layer 1: Presentation & User Experience", "y": 7.1, "color": "#E0F2FE", "border": "#0284C7",
         "mods": ["Executive KPI Cards", "Plotly Charts", "Audio Narration Player", "Web Speech Mic UI"]},
        {"name": "Layer 2: Security, RBAC & Session Management", "y": 5.75, "color": "#F3E8FF", "border": "#9333EA",
         "mods": ["PBKDF2-SHA256 Auth", "RBAC Permission Gate", "Session State Cache", "Immutable Audit Logger"]},
        {"name": "Layer 3: Data Ingestion & Schema Harmonization", "y": 4.4, "color": "#FEF3C7", "border": "#D97706",
         "mods": ["Multi-Schema Harmonizer", "RFM Feature Generator", "Isolation Forest Filter", "Data Quality Profiler"]},
        {"name": "Layer 4: AI, ML & Analytical Intelligence Engines", "y": 2.5, "color": "#DCFCE7", "border": "#16A34A",
         "mods": ["Churn Classifier (RF/SMOTE)", "Demand Forecaster (Chronos)", "CLV Lifetime Predictor",
                  "Safety Stock / ROP Optimizer", "Apriori Cross-Sell Engine", "Aspect Sentiment NLP", "PSI / KS Drift Monitor", "Natural Language Viva QA"]},
        {"name": "Layer 5: Prescriptive Synthesis & Decision Register", "y": 1.25, "color": "#FFE4E6", "border": "#E11D48",
         "mods": ["Cross-Module Risk Aggregator", "Revenue Impact Assessor", "Prioritized Decision Memo", "What-If Simulator"]},
        {"name": "Layer 6: Persistence & Storage Engine", "y": 0.15, "color": "#F1F5F9", "border": "#475569",
         "mods": ["SQLite Relational DB", "Joblib Model Binaries", "Pandas DataFrames", "Audit Event Logs"]}
    ]

    for layer in layers:
        h = 1.05 if len(layer["mods"]) <= 4 else 1.6
        box = patches.FancyBboxPatch(
            (0.5, layer["y"]), 10.0, h,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            edgecolor=layer["border"], facecolor=layer["color"], linewidth=1.8
        )
        ax.add_patch(box)
        ax.text(0.7, layer["y"] + h - 0.22, layer["name"], fontsize=9.5, fontweight='bold', color=layer["border"])

        if len(layer["mods"]) <= 4:
            for idx, m in enumerate(layer["mods"]):
                mb = patches.FancyBboxPatch(
                    (0.7 + idx * 2.4, layer["y"] + 0.12), 2.25, 0.55,
                    boxstyle="round,pad=0.05,rounding_size=0.08",
                    edgecolor="#94A3B8", facecolor="white", linewidth=1.2
                )
                ax.add_patch(mb)
                ax.text(0.7 + idx * 2.4 + 1.12, layer["y"] + 0.39, m, ha='center', va='center', fontsize=8, fontweight='semibold', color="#1E293B")
        else:
            # 2 rows of 4
            row1 = layer["mods"][:4]
            row2 = layer["mods"][4:]
            for idx, m in enumerate(row1):
                mb = patches.FancyBboxPatch(
                    (0.7 + idx * 2.4, layer["y"] + 0.78), 2.25, 0.52,
                    boxstyle="round,pad=0.05,rounding_size=0.08",
                    edgecolor="#94A3B8", facecolor="white", linewidth=1.2
                )
                ax.add_patch(mb)
                ax.text(0.7 + idx * 2.4 + 1.12, layer["y"] + 1.04, m, ha='center', va='center', fontsize=7.8, fontweight='semibold', color="#1E293B")
            for idx, m in enumerate(row2):
                mb = patches.FancyBboxPatch(
                    (0.7 + idx * 2.4, layer["y"] + 0.14), 2.25, 0.52,
                    boxstyle="round,pad=0.05,rounding_size=0.08",
                    edgecolor="#94A3B8", facecolor="white", linewidth=1.2
                )
                ax.add_patch(mb)
                ax.text(0.7 + idx * 2.4 + 1.12, layer["y"] + 0.40, m, ha='center', va='center', fontsize=7.8, fontweight='semibold', color="#1E293B")

    # Connectors between layers
    for y_c in [7.0, 5.65, 4.25, 2.38, 1.15]:
        ax.annotate("", xy=(5.5, y_c - 0.12), xytext=(5.5, y_c + 0.12),
                    arrowprops=dict(arrowstyle="<->", lw=1.8, color="#64748B"))

    ax.set_title("Figure 4.3: High-Level Modular System Architecture of MasterMind AI", fontsize=13, fontweight='bold', pad=15, color="#0F172A")
    plt.tight_layout()
    plt.savefig("diagrams/fig4_3_system_architecture.png", dpi=300)
    plt.close()
    print("Saved diagrams/fig4_3_system_architecture.png")

# ==========================================
# 4. FIG 4.4: ANALYTICAL PIPELINE FLOWCHART
# ==========================================
def generate_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    steps = [
        {"id": "Step 1", "title": "Data Ingestion &\nValidation", "desc": "CSV multi-schema scan,\nnull handling & type casting", "pos": (0.6, 4.5), "col": "#E0E7FF", "brd": "#4338CA"},
        {"id": "Step 2", "title": "Schema Harmonization\n& Outlier Filtering", "desc": "Canonical mapping &\nIsolation Forest cleaning", "pos": (3.2, 4.5), "col": "#FEF3C7", "brd": "#D97706"},
        {"id": "Step 3", "title": "Feature Engineering\n& Aggregation", "desc": "RFM computation &\ntime-series daily aggregation", "pos": (5.8, 4.5), "col": "#DCFCE7", "brd": "#15803D"},
        {"id": "Step 4", "title": "Multi-Model ML\nInference", "desc": "Churn (RF), Chronos-Bolt,\nCLV, ROP, Apriori & NLP", "pos": (8.4, 4.5), "col": "#F3E8FF", "brd": "#7E22CE"},
        {"id": "Step 5", "title": "Prescriptive Synthesis\n& Decision Matrix", "desc": "Cross-module ROI ranking &\nrisk mitigation generation", "pos": (8.4, 1.5), "col": "#FFE4E6", "brd": "#BE123C"},
        {"id": "Step 6", "title": "Dashboard Rendering\n& Voice Delivery", "desc": "Plotly views, Decision Memo,\ngTTS Audio & Audit Logging", "pos": (4.5, 1.5), "col": "#E0F2FE", "brd": "#0369A1"},
    ]

    for s in steps:
        box = patches.FancyBboxPatch(
            s["pos"], 2.0, 1.6,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            edgecolor=s["brd"], facecolor=s["col"], linewidth=2
        )
        ax.add_patch(box)
        # Badge
        badge = patches.FancyBboxPatch(
            (s["pos"][0] + 0.2, s["pos"][1] + 1.25), 0.8, 0.25,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            edgecolor=s["brd"], facecolor=s["brd"], linewidth=1
        )
        ax.add_patch(badge)
        ax.text(s["pos"][0] + 0.6, s["pos"][1] + 1.37, s["id"], ha='center', va='center', fontsize=7.5, fontweight='bold', color="white")

        ax.text(s["pos"][0] + 1.0, s["pos"][1] + 0.9, s["title"], ha='center', va='center', fontsize=8.5, fontweight='bold', color="#111827")
        ax.text(s["pos"][0] + 1.0, s["pos"][1] + 0.35, s["desc"], ha='center', va='center', fontsize=7.5, color="#374151")

    # Connectors
    # Step 1 -> Step 2
    ax.annotate("", xy=(3.2, 5.3), xytext=(2.6, 5.3), arrowprops=dict(arrowstyle="->", lw=2, color="#4338CA"))
    # Step 2 -> Step 3
    ax.annotate("", xy=(5.8, 5.3), xytext=(5.2, 5.3), arrowprops=dict(arrowstyle="->", lw=2, color="#D97706"))
    # Step 3 -> Step 4
    ax.annotate("", xy=(8.4, 5.3), xytext=(7.8, 5.3), arrowprops=dict(arrowstyle="->", lw=2, color="#15803D"))
    # Step 4 -> Step 5 (Down)
    ax.annotate("", xy=(9.4, 3.1), xytext=(9.4, 4.5), arrowprops=dict(arrowstyle="->", lw=2, color="#7E22CE"))
    # Step 5 -> Step 6 (Left)
    ax.annotate("", xy=(6.5, 2.3), xytext=(8.4, 2.3), arrowprops=dict(arrowstyle="->", lw=2, color="#BE123C"))

    ax.set_title("Figure 4.4: End-to-End Analytical Processing Pipeline Flowchart", fontsize=13, fontweight='bold', pad=15, color="#0F172A")
    plt.tight_layout()
    plt.savefig("diagrams/fig4_4_analytical_pipeline.png", dpi=300)
    plt.close()
    print("Saved diagrams/fig4_4_analytical_pipeline.png")

if __name__ == "__main__":
    generate_context_diagram()
    generate_perspective_diagram()
    generate_architecture_diagram()
    generate_pipeline_diagram()
    print("All diagrams generated successfully!")
