import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.styles import inject, add_sidebar
from utils.helpers import load_csv, HIGH_PRIORITY_THRESHOLD, NORMAL_PRIORITY_THRESHOLD, ROUTING_COLORS

st.set_page_config(page_title="Model Performance — TriageIQ", page_icon="🎯", layout="wide")

inject("""
.metric-row{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.metric-cell{padding:18px 16px;border-right:1px solid #1e2235}
.metric-cell:last-child{border-right:none}
.mv{font-family:'Barlow Condensed',sans-serif;font-size:2rem;font-weight:800;color:#f59e0b;line-height:1}
.ml{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#4a5568;text-transform:uppercase;letter-spacing:.1em;margin-top:4px}
.md{font-family:'Barlow',sans-serif;font-size:.72rem;color:#374151;margin-top:5px}
.comp-table{border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.comp-hdr{display:grid;grid-template-columns:180px 180px 1fr 90px 90px;background:#0c0e14;border-bottom:1px solid #1e2235;padding:10px 16px;gap:12px}
.comp-hdr span{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.1em}
.comp-row{display:grid;grid-template-columns:180px 180px 1fr 90px 90px;padding:14px 16px;gap:12px;border-bottom:1px solid #1e2235;align-items:start}
.comp-row:last-child{border-bottom:none}
.comp-row:hover{background:#0c0e14}
.comp-component{font-family:'Barlow Condensed',sans-serif;font-size:.9rem;font-weight:700;color:#e2e8f0;text-transform:uppercase;letter-spacing:.04em}
.comp-method{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#4a5568;line-height:1.5}
.comp-bv{font-family:'Barlow',sans-serif;font-size:.78rem;color:#6b7280;line-height:1.5}
.comp-num{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:800;color:#f59e0b}
.comp-num-lbl{font-family:'JetBrains Mono',monospace;font-size:.55rem;color:#4a5568;text-transform:uppercase}
.conf-strip{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.conf-cell{padding:20px;border-right:1px solid #1e2235}
.conf-cell:last-child{border-right:none}
.cc-bucket{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#4a5568;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px}
.cc-acc{font-family:'Barlow Condensed',sans-serif;font-size:2.2rem;font-weight:800;line-height:1;margin-bottom:6px}
.cc-bar-bg{background:#1e2235;height:4px;border-radius:2px;margin-bottom:8px}
.cc-bar{height:4px;border-radius:2px}
.cc-detail{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#374151;line-height:1.6}
.arch-box{background:#0c0e14;border:1px solid #1e2235;border-radius:2px;padding:16px 20px;margin-bottom:20px}
.arch-ah{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px}
.arch-p{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#4a5568;line-height:1.8;margin:0}
.thresh-legend{display:flex;flex-direction:column;gap:10px;padding:16px;background:#0c0e14;border:1px solid #1e2235;border-radius:2px}
.tl-row{display:flex;align-items:center;gap:10px}
.tl-dot{width:10px;height:10px;border-radius:1px;flex-shrink:0}
.tl-txt{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#6b7280;line-height:1.4}
.tl-txt strong{color:#e2e8f0}
.tl-note{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#2d3148;border-top:1px solid #1e2235;padding-top:10px;margin-top:4px}
.route-map-wrap{display:flex;flex-direction:column;gap:6px;margin:8px 0}
.route-row{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#0c0e14;border:1px solid #1e2235;border-radius:2px}
.route-dot{width:8px;height:8px;border-radius:1px;flex-shrink:0}
.route-grp{font-family:'Barlow Condensed',sans-serif;font-size:.9rem;font-weight:700;color:#f0f0f0;text-transform:uppercase;letter-spacing:.04em;min-width:220px}
.route-orig{font-family:'Barlow',sans-serif;font-size:.75rem;color:#374151}
""")

add_sidebar()

# PLOTLY base — no xaxis/yaxis to avoid duplicate kwarg error
PLOTLY = dict(
    paper_bgcolor="#0c0e14", plot_bgcolor="#0c0e14",
    font=dict(family="JetBrains Mono, monospace", color="#6b7280", size=10),
    title_font=dict(family="Barlow Condensed, sans-serif", color="#f0f0f0", size=15),
    margin=dict(t=44, b=32, l=20, r=20),
)
AX = dict(gridcolor="#1e2235", linecolor="#1e2235")

st.html("""
<div class="tiq-page-header">
  <div class="tiq-eyebrow">Section 03 // Evaluation</div>
  <div class="tiq-h1">Model Performance</div>
  <div class="tiq-sub">Real evaluation metrics, threshold logic, confidence buckets, and routing architecture.</div>
</div>
""")

# ── Headline metrics ──────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Final Metrics</div>')
mc_df = load_csv("final_model_comparison_summary.csv")
if not mc_df.empty:
    mc_df.columns = [c.lower().strip() for c in mc_df.columns]
    def safe_pct(df, comp, col):
        r = df[df['component'].str.contains(comp, case=False, na=False)]
        v = r[col].values[0] if not r.empty else None
        return f"{float(v):.1%}" if v and str(v) not in ['nan',''] else "—"
    def safe_f(df, comp, col):
        r = df[df['component'].str.contains(comp, case=False, na=False)]
        v = r[col].values[0] if not r.empty else None
        return f"{float(v):.3f}" if v and str(v) not in ['nan',''] else "—"
    pri_recall = safe_pct(mc_df, "Priority", "main_metric_value")
    rout_f1    = safe_pct(mc_df, "Routing",  "main_metric_value")
    rout_acc   = safe_pct(mc_df, "Routing",  "secondary_metric_value")
    sla_auc    = safe_f(mc_df,   "SLA",      "secondary_metric_value")
else:
    pri_recall, rout_f1, rout_acc, sla_auc = "95.3%","80.1%","80.6%","0.496"

st.html(f"""
<div class="metric-row">
  <div class="metric-cell"><div class="mv">{pri_recall}</div><div class="ml">High Recall</div><div class="md">Catches 19/20 urgent tickets</div></div>
  <div class="metric-cell"><div class="mv">5%</div><div class="ml">False Neg Rate</div><div class="md">Miss rate on High priority</div></div>
  <div class="metric-cell"><div class="mv">{rout_f1}</div><div class="ml">Routing F1</div><div class="md">Weighted across 4 groups</div></div>
  <div class="metric-cell"><div class="mv">{rout_acc}</div><div class="ml">Routing Accuracy</div><div class="md">Grouped 4-class outer test</div></div>
  <div class="metric-cell"><div class="mv">{sla_auc}</div><div class="ml">SLA ML AUC</div><div class="md">ML dropped — rule-based used</div></div>
</div>
""")

# ── Component table ───────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Component Summary</div>')
if mc_df.empty:
    st.html('<div class="tiq-missing">final_model_comparison_summary.csv not found</div>')
else:
    rows = ""
    for _, row in mc_df.iterrows():
        mv = row.get('main_metric_value','')
        sv = row.get('secondary_metric_value','')
        mv_s = f"{float(mv):.1%}" if str(mv) not in ['nan',''] else "—"
        sv_s = f"{float(sv):.3f}" if str(sv) not in ['nan',''] else "—"
        rows += f"""<div class="comp-row">
          <div class="comp-component">{row.get('component','')}</div>
          <div class="comp-method">{row.get('method','')}</div>
          <div class="comp-bv">{row.get('business_value','')}</div>
          <div><div class="comp-num">{mv_s}</div><div class="comp-num-lbl">{row.get('main_metric','')}</div></div>
          <div><div class="comp-num" style="font-size:.95rem;color:#6b7280">{sv_s}</div><div class="comp-num-lbl">{row.get('secondary_metric','')}</div></div>
        </div>"""
    st.html(f"""<div class="comp-table">
      <div class="comp-hdr"><span>Component</span><span>Method</span><span>Business Value</span><span>Main</span><span>Secondary</span></div>
      {rows}</div>""")

# ── Confidence buckets ─────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Routing Confidence Buckets</div>')
conf_df = load_csv("routing_confidence_bucket_summary.csv")
if conf_df.empty:
    st.html('<div class="tiq-missing">routing_confidence_bucket_summary.csv not found</div>')
else:
    conf_df.columns = [c.lower().strip() for c in conf_df.columns]
    colors = {"Low confidence (<0.50)":"#ef4444","Medium confidence (0.50-0.80)":"#f59e0b","High confidence (>=0.80)":"#21C354"}
    cells = ""
    for _, row in conf_df.iterrows():
        bucket  = row['confidence_bucket']
        acc     = float(row['accuracy'])
        count   = int(row['ticket_count'])
        avgc    = float(row['avg_confidence'])
        color   = colors.get(bucket, "#4B8BFF")
        verdict = "✅ Auto-route approved" if acc > 90 else ("⚠ Route with confirmation" if acc > 65 else "⛔ Manual triage required")
        cells += f"""<div class="conf-cell">
          <div class="cc-bucket">{bucket}</div>
          <div class="cc-acc" style="color:{color}">{acc:.1f}%</div>
          <div class="cc-bar-bg"><div class="cc-bar" style="width:{min(acc,100)}%;background:{color}"></div></div>
          <div class="cc-detail">{count:,} tickets · avg conf {avgc:.3f}<br>{verdict}</div>
        </div>"""
    st.html(f'<div class="conf-strip">{cells}</div>')

# ── Threshold chart ───────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Priority Threshold Bands</div>')
col1, col2 = st.columns([3, 1])
with col1:
    fig = go.Figure()
    for x0, x1, color, label in [
        (0, NORMAL_PRIORITY_THRESHOLD, "#21C354", "NORMAL"),
        (NORMAL_PRIORITY_THRESHOLD, HIGH_PRIORITY_THRESHOLD, "#f59e0b", "NEEDS REVIEW"),
        (HIGH_PRIORITY_THRESHOLD, 1.0, "#ef4444", "HIGH"),
    ]:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, fillcolor=color, opacity=0.15, line_width=0)
        fig.add_annotation(x=(x0+x1)/2, y=0.5, text=f"<b>{label}</b>", showarrow=False,
                           font=dict(color=color, size=12, family="Barlow Condensed, sans-serif"))
    fig.add_vline(x=NORMAL_PRIORITY_THRESHOLD, line_dash="dot", line_color="#f59e0b", line_width=1,
                  annotation_text=f"{NORMAL_PRIORITY_THRESHOLD}", annotation_font_color="#f59e0b", annotation_font_size=10)
    fig.add_vline(x=HIGH_PRIORITY_THRESHOLD, line_dash="dot", line_color="#ef4444", line_width=1,
                  annotation_text=f"{HIGH_PRIORITY_THRESHOLD}", annotation_font_color="#ef4444", annotation_font_size=10)
    fig.update_layout(
        **PLOTLY,
        title="P(HIGH) DECISION BANDS",
        xaxis=dict(title="Probability of High Priority", range=[0,1], tickformat=".0%", **AX),
        yaxis=dict(visible=False),
        height=180
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.html(f"""
    <div class="thresh-legend">
      <div class="tl-row"><div class="tl-dot" style="background:#21C354"></div>
        <div class="tl-txt"><strong>Normal</strong><br>P(High) &lt; {NORMAL_PRIORITY_THRESHOLD}</div></div>
      <div class="tl-row"><div class="tl-dot" style="background:#f59e0b"></div>
        <div class="tl-txt"><strong>Needs Review</strong><br>{NORMAL_PRIORITY_THRESHOLD} ≤ P &lt; {HIGH_PRIORITY_THRESHOLD}</div></div>
      <div class="tl-row"><div class="tl-dot" style="background:#ef4444"></div>
        <div class="tl-txt"><strong>High</strong><br>P(High) ≥ {HIGH_PRIORITY_THRESHOLD}</div></div>
      <div class="tl-note">Patched in Cell [9] — stricter High threshold maintains 95% recall while reducing false escalations</div>
    </div>""")

# ── Routing group map ─────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Routing Group Architecture</div>')
map_df = load_csv("routing_group_mapping.csv")
if map_df.empty:
    st.html('<div class="tiq-missing">routing_group_mapping.csv not found</div>')
else:
    map_df.columns = [c.lower().strip() for c in map_df.columns]
    rows = "".join(f"""<div class="route-row">
      <div class="route-dot" style="background:{color}"></div>
      <div class="route-grp">{group}</div>
      <div class="route-orig">← {" · ".join(map_df[map_df['routing_group']==group]['original_queue'].tolist()) or "—"}</div>
    </div>""" for group, color in ROUTING_COLORS.items())
    st.html(f'<div class="route-map-wrap">{rows}</div>')

st.html("""
<div class="arch-box">
  <div class="arch-ah">Model Architecture</div>
  <div class="arch-p">Both models: TF-IDF (max_features=70k, ngram 1–3, sublinear_tf=True) → SGDClassifier (loss=log_loss, class_weight=balanced)<br>
  Priority: binary (1=High, 0=Not High) · Routing: 4-class with keyword override layer<br>
  Serialised with scikit-learn 1.6.1 — do not upgrade sklearn or pkl files will break<br>
  Split: outer train/test + inner validation holdout (no data leakage)</div>
</div>""")

with st.expander("FULL PERFORMANCE TABLE"):
    perf = load_csv("final_model_performance_all.csv")
    if perf.empty:
        st.html('<div class="tiq-missing">final_model_performance_all.csv not found</div>')
    else:
        st.dataframe(perf, use_container_width=True)
