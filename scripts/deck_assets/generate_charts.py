"""Generate matplotlib chart assets for Panchaayat pitch deck."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ASSETS = Path(__file__).parent
BLUE = "#2563eb"
BLUE_LIGHT = "#dbeafe"
AMBER = "#f59e0b"
GREEN = "#10b981"
SLATE = "#64748b"
DARK = "#0f172a"


LIGHT_BG = "#f8fafc"
INDIGO = "#6366f1"


def save(fig, name, transparent=True):
    path = ASSETS / name
    fig.savefig(path, dpi=200, bbox_inches="tight",
                facecolor="none" if transparent else "white",
                edgecolor="none", transparent=transparent)
    plt.close(fig)
    return path


def chart_market():
    fig, ax = plt.subplots(figsize=(10, 5))
    categories = ["India MSMEs\n(no helpdesk)", "Consumer complaint\nplatforms", "Global CX\nsoftware TAM"]
    values = [63, 12, 50]
    colors = [BLUE, AMBER, GREEN]
    bars = ax.barh(categories, values, color=colors, height=0.55, edgecolor="white", linewidth=2)
    ax.set_xlabel("Market size (₹ Lakh Cr / $B — illustrative)", fontsize=11, color=SLATE)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{val}M+" if val == 63 else f"${val}B+", va="center", fontsize=12, fontweight="bold", color=DARK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=SLATE)
    ax.set_xlim(0, 75)
    save(fig, "chart_market.png")


def chart_workflow():
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    steps = [
        ("Share", BLUE, "1"),
        ("Discuss", "#6366f1", "2"),
        ("Brand\nResponds", "#0ea5e9", "3"),
        ("Propose\nResolution", AMBER, "4"),
        ("You\nConfirm", GREEN, "5"),
    ]
    xs = np.linspace(1.2, 10.8, 5)
    for i, (label, color, icon) in enumerate(steps):
        x = xs[i]
        circle = plt.Circle((x, 2), 0.55, color=color, zorder=2)
        ax.add_patch(circle)
        ax.text(x, 2, icon, ha="center", va="center", fontsize=16, fontweight="bold", color="white", zorder=3)
        ax.text(x, 0.85, label, ha="center", va="top", fontsize=10, fontweight="bold", color=DARK)
        if i < 4:
            ax.annotate("", xy=(xs[i + 1] - 0.6, 2), xytext=(x + 0.6, 2),
                        arrowprops=dict(arrowstyle="->", color=SLATE, lw=2))
    ax.text(6, 3.5, "Consumer Resolution Loop — only YOU close the case", ha="center",
            fontsize=14, fontweight="bold", color=DARK)
    save(fig, "chart_workflow.png")


def chart_comparison():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis("off")
    competitors = ["Google\nReviews", "MouthShut", "NCH/\nE-Jagriti", "Zendesk", "Panchaayat"]
    features = ["Public discussion", "Resolution loop", "Consumer confirms", "SME case mgmt", "India-first SEO"]
    data = np.array([
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ])
    # Build checkmark matrix manually
    cell_w, cell_h = 1.4, 0.7
    start_x, start_y = 2.5, 4.2
    for j, comp in enumerate(competitors):
        weight = "bold" if comp == "Panchaayat" else "normal"
        color = BLUE if comp == "Panchaayat" else DARK
        ax.text(start_x + j * cell_w + cell_w / 2, start_y + 0.3, comp, ha="center", va="center",
                fontsize=9, fontweight=weight, color=color)
    for i, feat in enumerate(features):
        y = start_y - (i + 1) * cell_h
        ax.text(0.2, y + cell_h / 2, feat, ha="left", va="center", fontsize=10, color=DARK)
        for j in range(5):
            x = start_x + j * cell_w
            rect = FancyBboxPatch((x, y), cell_w - 0.05, cell_h - 0.05, boxstyle="round,pad=0.02",
                                   facecolor=BLUE_LIGHT if j == 4 else "#f8fafc",
                                   edgecolor="#e2e8f0", linewidth=1)
            ax.add_patch(rect)
            has = (i == 0 and j in [0, 1, 4]) or (i == 1 and j in [1, 4]) or (i == 2 and j == 4) or \
                  (i == 3 and j in [3, 4]) or (i == 4 and j == 4)
            if has:
                ax.text(x + cell_w / 2, y + cell_h / 2, "✓", ha="center", va="center",
                        fontsize=14, color=GREEN if j == 4 else SLATE, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.0)
    save(fig, "chart_comparison.png")


def chart_roadmap():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    quarters = [
        ("Q2 '26", "10 SME pilots\nPostgres + PWA"),
        ("Q3 '26", "Email-to-case\nHindi UI"),
        ("Q4 '26", "Social scraping\n100 paying SMEs"),
        ("Q1 '27", "Enterprise API\n5 logos"),
        ("Q2 '27", "Mobile apps\nTier-2 cities"),
    ]
    xs = np.linspace(1.5, 9.5, 5)
    ax.plot([1, 10], [2, 2], color=BLUE, linewidth=3, zorder=1)
    for i, (q, desc) in enumerate(quarters):
        x = xs[i]
        ax.scatter([x], [2], s=200, color=AMBER if i == 0 else BLUE, zorder=3, edgecolors="white", linewidths=2)
        ax.text(x, 2.55, q, ha="center", fontsize=11, fontweight="bold", color=DARK)
        ax.text(x, 1.2, desc, ha="center", va="top", fontsize=9, color=SLATE,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=BLUE_LIGHT, edgecolor="#e2e8f0"))
    save(fig, "chart_roadmap.png")


def chart_metrics():
    fig, axes = plt.subplots(1, 4, figsize=(11, 3))
    metrics = [
        ("MVP", "Live", BLUE),
        ("8", "Demo personas", AMBER),
        ("6", "Seeded brands", GREEN),
        ("3", "SaaS tiers", "#6366f1"),
    ]
    for ax, (big, label, color) in zip(axes, metrics):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.02",
                               facecolor="white", edgecolor=color, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(0.5, 0.58, big, ha="center", va="center", fontsize=28, fontweight="bold", color=color)
        ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=10, color=SLATE)
    fig.suptitle("Current Traction", fontsize=15, fontweight="bold", color=DARK, y=1.02)
    save(fig, "chart_metrics.png")


def chart_revenue():
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ["SaaS\nSubscriptions", "Enterprise\nAPI", "Contextual\nAds", "Analytics\n(future)"]
    sizes = [55, 25, 12, 8]
    colors = [BLUE, AMBER, GREEN, SLATE]
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct="%1.0f%%", colors=colors,
                                       startangle=90, pctdistance=0.75,
                                       textprops={"fontsize": 10, "color": DARK})
    for at in autotexts:
        at.set_fontweight("bold")
        at.set_color("white")
    save(fig, "chart_revenue.png")


if __name__ == "__main__":
    chart_market()
    chart_workflow()
    chart_comparison()
    chart_roadmap()
    chart_metrics()
    chart_revenue()
    print("Charts saved to", ASSETS)
