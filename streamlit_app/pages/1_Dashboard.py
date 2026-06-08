import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.styles import inject, add_sidebar
from utils.helpers import load_csv, PRIORITY_COLORS, SLA_COLORS, ROUTING_COLORS

st.set_page_config(page_title="Dashboard — TriageIQ", page_icon="🎯", layout="wide")

inject("""
.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:28px}
.kpi-cell{padding:18px 20px;border-right:1px solid #1e2235}
.kpi-cell:last-child{border-right:none}
.kv{font-family:'Barlow Condensed',sans-serif;font-size:2rem;font-weight:800;color:#f59e0b;line-height:1}
.kl{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#4a5568;text-transform:uppercase;letter-spacing:.1em;margin-top:4px}
.km{font-family:'Barlow',sans-serif;font-size:.72rem;color:#374151;margin-top:5px;line-height:1.4}
.bkpi-table{border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.bkpi-hdr{display:grid;grid-template-columns:180px 1fr 1fr 1fr;background:#0c0e14;border-bottom:1px solid #1e2235;padding:10px 16px;gap:16px}
.bkpi-hdr span{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.1em}
.bkpi-row{display:grid;grid-template-columns:180px 1fr 1fr 1fr;padding:14px 16px;gap:16px;border-bottom:1px solid #1e2235}
.bkpi-row:last-child{border-bottom:none}
.bkpi-row:hover{background:#0c0e14}
.bkpi-kpi{font-family:'Barlow Condensed',sans-serif;font-size:.9rem;font-weight:700;color:#e2e8f0;text-transform:uppercase;letter-spacing:.04em}
.bkpi-cell{font-family:'Barlow',sans-serif;font-size:.78rem;color:#6b7280;line-height:1.5}
""")

add_sidebar()

PLOTLY = dict(
    paper_bgcolor="#0c0e14", plot_bgcolor="#0c0e14",
    font=dict(family="JetBrains Mono, monospace", color="#6b7280", size=10),
    title_font=dict(family="Barlow Condensed, sans-serif", color="#f0f0f0", size=15),
    legend=dict(font=dict(color="#6b7280", size=10)),
    margin=dict(t=44, b=32, l=20, r=20),
)
AX = dict(gridcolor="#1e2235", linecolor="#1e2235")

st.html("""
<div class="tiq-page-header">
  <div class="tiq-eyebrow">Section 01 // Analytics</div>
  <div class="tiq-h1">Dashboard</div>
  <div class="tiq-sub">Business KPIs, ticket distribution, SLA exposure, and routing performance.</div>
</div>
""")

# ── KPI Strip ─────────────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Business KPIs</div>')
kpi_df = load_csv("final_business_kpi_cards.csv")
if kpi_df.empty:
    st.html('<div class="tiq-missing">⚠ final_business_kpi_cards.csv not found in data/</div>')
else:
    cells = "".join(f'<div class="kpi-cell"><div class="kv">{r["value"]}</div><div class="kl">{r["kpi"]}</div><div class="km">{r["business_meaning"]}</div></div>'
                    for _, r in kpi_df.iterrows())
    st.html(f'<div class="kpi-strip">{cells}</div>')

# ── KPI Impact Table ──────────────────────────────────────────────────────────
st.html('<div class="tiq-section">How TriageIQ Addresses Each KPI</div>')
bkpi_df = load_csv("final_business_kpi_summary.csv")
if bkpi_df.empty:
    st.html('<div class="tiq-missing">⚠ final_business_kpi_summary.csv not found in data/</div>')
else:
    rows = "".join(f"""<div class="bkpi-row">
      <div class="bkpi-kpi">{r['business_kpi']}</div>
      <div class="bkpi-cell">{r['current_problem']}</div>
      <div class="bkpi-cell">{r['how_triageiq_helps']}</div>
      <div class="bkpi-cell">{r['measurement_method']}</div>
    </div>""" for _, r in bkpi_df.iterrows())
    st.html(f"""<div class="bkpi-table">
      <div class="bkpi-hdr"><span>KPI</span><span>Problem</span><span>How TriageIQ Helps</span><span>Measurement</span></div>
      {rows}</div>""")

# ── Charts ────────────────────────────────────────────────────────────────────
st.html('<div class="tiq-section">Ticket Distribution</div>')
dash_df = load_csv("triageiq_dashboard_data_with_rule_sla.csv")

if dash_df.empty:
    st.html('<div class="tiq-missing">⚠ triageiq_dashboard_data_with_rule_sla.csv not found — add to data/ folder to enable charts</div>')
else:
    col1, col2 = st.columns(2)
    with col1:
        pc = dash_df["priority_3class"].value_counts().reset_index()
        pc.columns = ["Priority","Count"]
        fig = px.pie(pc, names="Priority", values="Count", color="Priority",
                     color_discrete_map=PRIORITY_COLORS, hole=0.5, title="PRIORITY BREAKDOWN")
        fig.update_traces(textfont=dict(family="JetBrains Mono, monospace", size=10))
        fig.update_layout(**PLOTLY)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sc = dash_df["sla_risk_level"].value_counts().reset_index()
        sc.columns = ["SLA Risk","Count"]
        fig2 = px.bar(sc, x="SLA Risk", y="Count", color="SLA Risk",
                      color_discrete_map=SLA_COLORS, title="SLA RISK DISTRIBUTION")
        fig2.update_traces(marker_line_width=0)
        fig2.update_layout(**PLOTLY, showlegend=False, xaxis=AX, yaxis=AX)
        st.plotly_chart(fig2, use_container_width=True)

    st.html('<div class="tiq-section">Response Time &amp; Routing</div>')
    col3, col4 = st.columns(2)

    with col3:
        frt = dash_df["first_response_time_bucket"].value_counts().reset_index()
        frt.columns = ["Bucket","Count"]
        fig3 = px.bar(frt, x="Bucket", y="Count", title="FIRST RESPONSE TIME",
                      color_discrete_sequence=["#f59e0b"])
        fig3.update_traces(marker_line_width=0)
        fig3.update_layout(**PLOTLY, showlegend=False,
                           xaxis=dict(**AX, tickangle=15), yaxis=AX)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        cross = dash_df.groupby(["priority_3class","sla_risk_level"]).size().reset_index(name="Count")
        fig4 = px.bar(cross, x="priority_3class", y="Count", color="sla_risk_level",
                      color_discrete_map=SLA_COLORS, barmode="stack", title="PRIORITY × SLA RISK")
        fig4.update_traces(marker_line_width=0)
        fig4.update_layout(**PLOTLY, xaxis=AX, yaxis=AX)
        st.plotly_chart(fig4, use_container_width=True)

    st.html('<div class="tiq-section">Channel &amp; Region</div>')
    col5, col6 = st.columns(2)

    with col5:
        ch = dash_df["channel"].value_counts().reset_index()
        ch.columns = ["Channel","Count"]
        fig5 = px.pie(ch, names="Channel", values="Count", hole=0.45, title="TICKETS BY CHANNEL",
                      color_discrete_sequence=["#f59e0b","#ef4444","#4B8BFF","#21C354","#A855F7"])
        fig5.update_traces(textfont=dict(family="JetBrains Mono, monospace", size=10))
        fig5.update_layout(**PLOTLY)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        rg = dash_df["region"].value_counts().reset_index()
        rg.columns = ["Region","Count"]
        fig6 = px.bar(rg, x="Count", y="Region", orientation="h", title="TICKETS BY REGION",
                      color_discrete_sequence=["#4B8BFF"])
        fig6.update_traces(marker_line_width=0)
        fig6.update_layout(**PLOTLY, showlegend=False, xaxis=AX, yaxis=AX)
        st.plotly_chart(fig6, use_container_width=True)

    with st.expander("RAW DATA — first 100 rows"):
        st.dataframe(dash_df.head(100), use_container_width=True)
