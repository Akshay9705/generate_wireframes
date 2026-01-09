from __future__ import annotations
import os, textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT_DIR = "wireframes_out"
os.makedirs(OUT_DIR, exist_ok=True)

def wrap(s: str, width: int) -> str:
    return "\n".join(textwrap.wrap(s, width=width))

def box(ax, x, y, w, h, title="", body=None, title_size=11, body_size=9):
    """Draw a labeled rectangle with clipped, wrapped text."""
    rect = Rectangle((x, y), w, h, fill=False, linewidth=1.5)
    ax.add_patch(rect)

    if title:
        t = ax.text(x + 0.01, y + h - 0.015, title, fontsize=title_size,
                    weight="bold", va="top", clip_on=True)
        t.set_clip_path(rect)

    if body:
        body_text = "\n".join([f"• {wrap(line, 28)}" for line in body])
        # Try a couple font sizes to avoid overflow
        for fs in (body_size, body_size-1, body_size-2):
            txt = ax.text(x + 0.01, y + h - 0.06, body_text, fontsize=fs,
                          va="top", clip_on=True)
            txt.set_clip_path(rect)
            # crude overflow heuristic: if too many lines, shrink
            if body_text.count("\n") < 8 or fs == body_size-2:
                break
            txt.remove()

def generate():
    fig = plt.figure(figsize=(13.5, 8))
    ax = plt.gca()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Frame + title
    ax.add_patch(Rectangle((0.03, 0.05), 0.94, 0.92, fill=False, linewidth=2))
    ax.text(0.03, 0.975, "Figure 1 — Conceptual wireframe (illustrative; no real/simulated data)",
            fontsize=10, va="top")
    ax.text(0.03, 0.948, "CFO Dashboard 1: Enterprise Financial Performance Overview",
            fontsize=14, weight="bold", va="top")

    # Left filter pane (distinctive)
    box(ax, 0.05, 0.10, 0.18, 0.82,
        title="Filters (global)",
        body=["Time period", "Channel", "Region / Business unit", "Currency / reporting view"],
        body_size=9)

    # KPI tiles row (top)
    kx, ky, kw, kh = 0.25, 0.83, 0.70, 0.09
    tile_w = kw / 4
    tiles = ["Revenue (aggregated)", "Operating profit", "Operating margin", "Cash from ops"]
    for i, t in enumerate(tiles):
        box(ax, kx + i*tile_w, ky, tile_w-0.005, kh, title=t, body=["Status / direction"])

    # Middle: performance bridge (waterfall placeholder)
    box(ax, 0.25, 0.52, 0.44, 0.28,
        title="Performance bridge (conceptual)",
        body=[
            "Period vs prior / plan variance bridge",
            "Drivers: volume, price/mix, costs",
            "Click to drill: channel → business unit"
        ],
        body_size=9)

    # Right: exceptions & alerts
    box(ax, 0.71, 0.52, 0.24, 0.28,
        title="Exceptions & escalation queue",
        body=[
            "Material variance flags (Top 5)",
            "Risk / control breaches (conceptual)",
            "Owner + status + next review date"
        ],
        body_size=9)

    # Bottom left: comparative views
    box(ax, 0.25, 0.10, 0.44, 0.38,
        title="Channel & business unit comparison",
        body=[
            "Contribution mix by channel",
            "Margin comparison (conceptual bars)",
            "Cost-to-revenue comparison"
        ],
        body_size=9)

    # Bottom right: trend strip + notes
    box(ax, 0.71, 0.10, 0.24, 0.38,
        title="Trends (conceptual)",
        body=[
            "Rolling view: revenue, margin, cash",
            "Annotated events / explanations (text)"
        ],
        body_size=9)

    # Export as SVG + PDF (best for Word)
    base = os.path.join(OUT_DIR, "figure_1_cfo_1_finance_overview")
    plt.savefig(base + ".svg", bbox_inches="tight")
    plt.savefig(base + ".pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved:", base + ".svg")
    print("Saved:", base + ".pdf")

if __name__ == "__main__":
    generate()
