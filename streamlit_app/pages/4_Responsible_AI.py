import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.styles import inject, add_sidebar
from utils.helpers import load_csv

st.set_page_config(page_title="Responsible AI — TriageIQ", page_icon="🎯", layout="wide")

inject("""
.principles{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:#1e2235;border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.principle{background:#080a0f;padding:22px}
.p-num{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#1e2235;font-weight:600;margin-bottom:10px}
.principle h4{font-family:'Barlow Condensed',sans-serif;font-size:1.05rem;font-weight:700;color:#f0f0f0;text-transform:uppercase;letter-spacing:.06em;margin:0 0 8px}
.principle p{font-family:'Barlow',sans-serif;font-size:.82rem;color:#6b7280;line-height:1.65;margin:0}
.cost-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#1e2235;border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:16px}
.cost-cell{background:#080a0f;padding:22px}
.cc-type{font-family:'JetBrains Mono',monospace;font-size:.58rem;text-transform:uppercase;letter-spacing:.14em;margin-bottom:8px}
.cc-label{font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;font-weight:700;text-transform:uppercase;margin-bottom:10px}
.cc-body{font-family:'Barlow',sans-serif;font-size:.82rem;color:#6b7280;line-height:1.6}
.cost-high{border-top:3px solid #ef4444}
.cost-low{border-top:3px solid #f59e0b}
.cost-high .cc-type,.cost-high .cc-label{color:#ef4444}
.cost-low .cc-type,.cost-low .cc-label{color:#f59e0b}
.tradeoff{background:#0c0e14;border:1px solid #1e2235;border-radius:2px;padding:20px 22px;margin-bottom:24px}
.tt{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.14em;margin-bottom:12px}
.tr-row{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.tr-label{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#6b7280;min-width:180px}
.tr-val{font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700}
.tr-note{font-family:'Barlow',sans-serif;font-size:.78rem;color:#374151}
.tr-foot{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#374151;border-top:1px solid #1e2235;padding-top:10px;margin-top:10px}
.risk-table{border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.risk-hdr{display:grid;grid-template-columns:200px 1fr 1fr;background:#0c0e14;border-bottom:1px solid #1e2235;padding:10px 16px;gap:16px}
.risk-hdr span{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.1em}
.risk-row{display:grid;grid-template-columns:200px 1fr 1fr;padding:14px 16px;gap:16px;border-bottom:1px solid #1e2235;align-items:start}
.risk-row:last-child{border-bottom:none}
.risk-row:hover{background:#0c0e14}
.risk-area-cell{font-family:'Barlow Condensed',sans-serif;font-size:.88rem;font-weight:700;color:#e2e8f0;text-transform:uppercase;letter-spacing:.04em;line-height:1.3}
.risk-txt{font-family:'Barlow',sans-serif;font-size:.78rem;color:#6b7280;line-height:1.5}
.risk-mit{font-family:'Barlow',sans-serif;font-size:.78rem;color:#4a5568;line-height:1.5}
.exec-table{border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:24px}
.exec-row{display:grid;grid-template-columns:160px 1fr;border-bottom:1px solid #1e2235}
.exec-row:last-child{border-bottom:none}
.exec-row:hover{background:#0c0e14}
.exec-area{background:#0c0e14;padding:14px 16px;border-right:1px solid #1e2235;font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center}
.exec-summary{padding:14px 16px;font-family:'Barlow',sans-serif;font-size:.82rem;color:#6b7280;line-height:1.5;display:flex;align-items:center}
.about-box{background:#0c0e14;border:1px solid #1e2235;border-radius:2px;padding:24px}
.about-box h4{font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;font-weight:700;color:#f0f0f0;text-transform:uppercase;letter-spacing:.06em;margin:0 0 12px}
.about-box p{font-family:'Barlow',sans-serif;font-size:.83rem;color:#6b7280;line-height:1.7;margin:0}
""")

add_sidebar()

st.html("""
<div class="tiq-page-header">
  <div class="tiq-eyebrow">Section 04 // Ethics &amp; Governance</div>
  <div class="tiq-h1">Responsible AI</div>
  <div class="tiq-sub">Design principles, asymmetric cost framing, and full risk register from the notebook.</div>
</div>
""")

st.html('<div class="tiq-section">Design Principles</div>')
st.html("""
<div class="principles">
  <div class="principle"><div class="p-num">P-01</div><h4>Human-in-the-Loop Always</h4>
    <p>All AI outputs are recommendations. Every classification, routing suggestion, and response draft requires human agent review before any action. The model never auto-routes or auto-sends without agent confirmation.</p></div>
  <div class="principle"><div class="p-num">P-02</div><h4>Asymmetric Cost Design</h4>
    <p>False negatives on High-priority tickets carry significantly higher cost than false positives. The model is tuned to maximise recall on urgent tickets at the cost of more false alarms — deliberate and disclosed.</p></div>
  <div class="principle"><div class="p-num">P-03</div><h4>Transparent Thresholds</h4>
    <p>Every prediction surfaces the raw P(High) score and the threshold band it falls into. Agents see exactly why a ticket was scored High, Needs Review, or Normal — not just a label.</p></div>
  <div class="principle"><div class="p-num">P-04</div><h4>Honest Limitations</h4>
    <p>SLA ML prediction was evaluated and dropped — both models scored ~0.50 AUC (coin flip). Transparent rule-based scoring is used instead. No stronger claims are made than the evidence supports.</p></div>
  <div class="principle"><div class="p-num">P-05</div><h4>Low-Confidence Flagging</h4>
    <p>Routing predictions below 50% confidence trigger a manual triage flag. The Needs Review band is always sent to human review — never auto-routed regardless of routing confidence.</p></div>
  <div class="principle"><div class="p-num">P-06</div><h4>Multilingual Awareness</h4>
    <p>Models trained on a multilingual dataset. Non-English tickets may yield lower confidence. Not validated for production use in non-English environments without additional testing and monitoring.</p></div>
</div>
""")

st.html('<div class="tiq-section">Asymmetric Cost Structure</div>')
st.html("""
<div class="cost-grid">
  <div class="cost-cell cost-high">
    <div class="cc-type">False Negative</div><div class="cc-label">High Cost</div>
    <div class="cc-body">A High-priority ticket classified as Normal or Needs Review, falling into the standard queue.<br><br>
    <b style="color:#e2e8f0">Consequences:</b> SLA breach · Customer churn · Revenue impact · Management escalation · Reputational damage.</div>
  </div>
  <div class="cost-cell cost-low">
    <div class="cc-type">False Positive</div><div class="cc-label">Low Cost</div>
    <div class="cc-body">A Normal ticket flagged as High or Needs Review, reviewed unnecessarily.<br><br>
    <b style="color:#e2e8f0">Consequences:</b> Agent spends ~30 extra seconds. Fully recoverable. Acceptable in exchange for near-elimination of missed urgent tickets.</div>
  </div>
</div>
<div class="tradeoff">
  <div class="tt">Model Tradeoff at Selected Threshold (0.55)</div>
  <div class="tr-row"><span class="tr-label">High Priority Recall</span><span class="tr-val" style="color:#21C354">~95%</span><span class="tr-note">Catches 19 of 20 urgent tickets</span></div>
  <div class="tr-row"><span class="tr-label">High Priority Precision</span><span class="tr-val" style="color:#f59e0b">~46%</span><span class="tr-note">~Half of flagged tickets are not truly High — acceptable false alarm rate</span></div>
  <div class="tr-row"><span class="tr-label">Overall Accuracy</span><span class="tr-val" style="color:#6b7280">55%</span><span class="tr-note">Lower than balanced model — intentional design choice</span></div>
  <div class="tr-foot">This tradeoff is deliberate, disclosed, and consistent with the asymmetric cost structure above.</div>
</div>
""")

# ── Risk Register — columns: risk_area, why_it_matters, mitigation ─────────────
st.html('<div class="tiq-section">Risk Register</div>')
rai_df = load_csv("final_responsible_ai_summary.csv")
if rai_df.empty:
    st.html('<div class="tiq-missing">final_responsible_ai_summary.csv not found</div>')
else:
    rai_df.columns = [c.lower().strip() for c in rai_df.columns]
    rows = "".join(f"""<div class="risk-row">
      <div class="risk-area-cell">{r['risk_area']}</div>
      <div class="risk-txt">{r['why_it_matters']}</div>
      <div class="risk-mit">{r['mitigation']}</div>
    </div>""" for _, r in rai_df.iterrows())
    st.html(f"""<div class="risk-table">
      <div class="risk-hdr"><span>Risk Area</span><span>Why It Matters</span><span>Mitigation</span></div>
      {rows}</div>""")

# ── Executive Summary — columns: area, summary ─────────────────────────────────
st.html('<div class="tiq-section">Executive Summary</div>')
exec_df = load_csv("final_executive_summary.csv")
if exec_df.empty:
    st.html('<div class="tiq-missing">final_executive_summary.csv not found</div>')
else:
    exec_df.columns = [c.lower().strip() for c in exec_df.columns]
    rows = "".join(f"""<div class="exec-row">
      <div class="exec-area">{r['area']}</div>
      <div class="exec-summary">{r['summary']}</div>
    </div>""" for _, r in exec_df.iterrows())
    st.html(f'<div class="exec-table">{rows}</div>')

# ── About ──────────────────────────────────────────────────────────────────────
st.html('<div class="tiq-section">About</div>')
st.html("""
<div class="about-box">
  <h4>TriageIQ // BUDT751 — Harnessing AI For Business // Group 2</h4>
  <p>AI-powered triage intelligence layer for IT helpdesk operations managers. Classifies incoming tickets by priority, routes them to the correct support group, scores SLA risk, and generates a first-response draft for human review.<br><br>
  <b style="color:#e2e8f0">Training data:</b> Multilingual helpdesk tickets (~28k) for priority and routing models. Mendeley helpdesk dataset (200k tickets, 2016–2023) for dashboard analytics.<br><br>
  <b style="color:#e2e8f0">Models:</b> TF-IDF + SGDClassifier (scikit-learn 1.6.1). Rule-based SLA scoring. ML SLA evaluated and discarded.<br><br>
  <b style="color:#e2e8f0">Generative AI:</b> OpenAI gpt-4o-mini for response drafts. Template fallback when API key unavailable. All drafts require human review before sending.</p>
</div>
""")
