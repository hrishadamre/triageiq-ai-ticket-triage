import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.styles import inject, add_sidebar

st.set_page_config(
    page_title="TriageIQ",
    page_icon="🎯",
    layout="wide",

)

inject("""
.tiq-header{display:flex;align-items:center;gap:20px;padding:48px 0 16px;border-bottom:1px solid #1e2235;margin-bottom:12px}
.tiq-logo{width:52px;height:52px;background:linear-gradient(135deg,#f59e0b,#ef4444);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);flex-shrink:0}
.tiq-wordmark h1{font-family:'Barlow Condensed',sans-serif;font-size:3rem;font-weight:800;letter-spacing:.08em;color:#f0f0f0;text-transform:uppercase;margin:0;line-height:1}
.tiq-tagline{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#f59e0b;letter-spacing:.18em;text-transform:uppercase;margin-top:4px}
.tiq-online{margin-left:auto;display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#4ade80;letter-spacing:.1em}
.tiq-online-dot{width:8px;height:8px;border-radius:50%;background:#4ade80;box-shadow:0 0 8px #4ade80;animation:hpulse 2s infinite}
@keyframes hpulse{0%,100%{opacity:1}50%{opacity:.4}}
.stat-strip{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin:28px 0}
.stat-cell{padding:20px 24px;border-right:1px solid #1e2235;position:relative}
.stat-cell:last-child{border-right:none}
.stat-cell::before{content:attr(data-i);position:absolute;top:8px;right:12px;font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#1e2235;font-weight:600}
.sv{font-family:'Barlow Condensed',sans-serif;font-size:2.8rem;font-weight:800;color:#f59e0b;line-height:1;margin-bottom:4px}
.sl{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#4a5568;text-transform:uppercase;letter-spacing:.12em}
.sd{font-family:'Barlow',sans-serif;font-size:.78rem;color:#374151;margin-top:6px}
.pipeline{display:flex;align-items:stretch;border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin:16px 0 32px}
.pipe-step{flex:1;padding:18px 14px;border-right:1px solid #1e2235;position:relative}
.pipe-step:last-child{border-right:none}
.pn{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#2d3148;font-weight:600;margin-bottom:8px}
.pi{font-size:1.3rem;margin-bottom:6px}
.pm{font-family:'Barlow Condensed',sans-serif;font-size:.85rem;font-weight:700;color:#e2e8f0;text-transform:uppercase;letter-spacing:.05em}
.pd{font-family:'Barlow',sans-serif;font-size:.72rem;color:#4a5568;margin-top:4px;line-height:1.4}
.pipe-on{background:#0e1117}
.pipe-on .pm{color:#f59e0b}
.pipe-on::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:#f59e0b}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#1e2235;border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin:16px 0 32px}
.feat-cell{background:#080a0f;padding:28px 24px;transition:background .2s}
.feat-cell:hover{background:#0c0e14}
.feat-num{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#1e2235;font-weight:600;margin-bottom:14px}
.feat-cell h3{font-family:'Barlow Condensed',sans-serif;font-size:1.15rem;font-weight:700;color:#f0f0f0;text-transform:uppercase;letter-spacing:.06em;margin:0 0 10px}
.feat-cell p{font-family:'Barlow',sans-serif;font-size:.85rem;color:#6b7280;line-height:1.65;margin:0}
.feat-tag{display:inline-block;margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#f59e0b;border:1px solid #f59e0b33;padding:2px 8px;border-radius:2px}
.footnote{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2d3148;border-top:1px solid #1e2235;padding-top:20px;margin-top:40px;line-height:1.8}
""")

add_sidebar()

st.html("""
<div class="tiq-header">
  <div class="tiq-logo"></div>
  <div class="tiq-wordmark">
    <h1>TriageIQ</h1>
    <div class="tiq-tagline">Triage Intelligence System // BUDT751 // Group 2</div>
  </div>
  <div class="tiq-online"><div class="tiq-online-dot"></div>SYSTEM ONLINE</div>
</div>
<div class="stat-strip">
  <div class="stat-cell" data-i="01"><div class="sv">95%</div><div class="sl">High Priority Recall</div><div class="sd">Catches 19 of 20 urgent tickets</div></div>
  <div class="stat-cell" data-i="02"><div class="sv">81%</div><div class="sl">Routing Accuracy</div><div class="sd">4-class grouped queue model</div></div>
  <div class="stat-cell" data-i="03"><div class="sv">&lt;2s</div><div class="sl">Triage Time</div><div class="sd">Per ticket, end-to-end</div></div>
  <div class="stat-cell" data-i="04"><div class="sv">100%</div><div class="sl">Human Review</div><div class="sd">All outputs require agent sign-off</div></div>
</div>
""")

st.html('<div class="tiq-section">Prediction Pipeline</div>')
st.html("""
<div class="pipeline">
  <div class="pipe-step"><div class="pn">01</div><div class="pi">📥</div><div class="pm">Ingest</div><div class="pd">Subject + body received</div></div>
  <div class="pipe-step pipe-on"><div class="pn">02</div><div class="pi">⚡</div><div class="pm">Priority</div><div class="pd">TF-IDF + SGD binary classifier</div></div>
  <div class="pipe-step pipe-on"><div class="pn">03</div><div class="pi">🗂</div><div class="pm">Routing</div><div class="pd">Keyword override → ML 4-class</div></div>
  <div class="pipe-step pipe-on"><div class="pn">04</div><div class="pi">🚦</div><div class="pm">SLA Risk</div><div class="pd">Rule-based score (ML dropped)</div></div>
  <div class="pipe-step pipe-on"><div class="pn">05</div><div class="pi">✍</div><div class="pm">Draft</div><div class="pd">OpenAI gpt-4o-mini response</div></div>
  <div class="pipe-step"><div class="pn">06</div><div class="pi">👤</div><div class="pm">Agent</div><div class="pd">Reviews &amp; takes action</div></div>
</div>
""")

st.html('<div class="tiq-section">Core Capabilities</div>')
st.html("""
<div class="feat-grid">
  <div class="feat-cell"><div class="feat-num">F-01</div><h3>Priority Classification</h3>
    <p>Binary text classifier with calibrated threshold bands. Outputs High, Needs Review, or Normal — tuned to minimise missed urgent tickets at the cost of false alarms.</p>
    <span class="feat-tag">95% HIGH RECALL</span></div>
  <div class="feat-cell"><div class="feat-num">F-02</div><h3>Intelligent Routing</h3>
    <p>Keyword override catches obvious billing and access tickets at 90% confidence, then falls back to a grouped 4-class ML model. 81% accuracy on outer test set.</p>
    <span class="feat-tag">81% ACCURACY</span></div>
  <div class="feat-cell"><div class="feat-num">F-03</div><h3>SLA Risk Scoring</h3>
    <p>Transparent rule-based scoring across priority, complexity, subscription tier, customer segment, ticket history, and channel. ML SLA evaluated and discarded (AUC ~0.50).</p>
    <span class="feat-tag">RULE-BASED</span></div>
  <div class="feat-cell"><div class="feat-num">F-04</div><h3>AI Response Draft</h3>
    <p>OpenAI generates a routing-aware first-response calibrated to urgency, assigned team, and SLA risk. Template fallback if API unavailable. Human review required before sending.</p>
    <span class="feat-tag">GPT-4O-MINI</span></div>
  <div class="feat-cell"><div class="feat-num">F-05</div><h3>Human-in-the-Loop</h3>
    <p>Every prediction surfaces raw probability and routing confidence. Low-confidence predictions trigger mandatory review. High-priority tickets require agent confirmation before action.</p>
    <span class="feat-tag">ALWAYS ON</span></div>
  <div class="feat-cell"><div class="feat-num">F-06</div><h3>Responsible AI</h3>
    <p>Asymmetric cost framing — a missed urgent ticket costs more than a false alarm. Transparent thresholds, honest limitations disclosed, no stronger claims than the data supports.</p>
    <span class="feat-tag">TRANSPARENT</span></div>
</div>
""")

st.html("""
<div class="footnote">
  TRIAGEIQ // BUDT751 — Harnessing AI For Business // Group 2 &nbsp;·&nbsp;
  Models: TF-IDF + SGDClassifier (sklearn 1.6.1) &nbsp;·&nbsp;
  Generative: OpenAI gpt-4o-mini &nbsp;·&nbsp;
  All AI outputs require human review &nbsp;·&nbsp;
  SLA: rule-based (ML dropped, AUC ~0.50)
</div>
""")
