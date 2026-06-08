import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.styles import inject, add_sidebar
from utils.helpers import triageiq_predict, PRIORITY_COLORS, SLA_COLORS, ROUTING_COLORS

st.set_page_config(page_title="Live Demo — TriageIQ", page_icon="🎯", layout="wide")

inject("""
.verdict-strip{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-bottom:16px}
.verdict-cell{padding:22px 20px;border-right:1px solid #1e2235}
.verdict-cell:last-child{border-right:none}
.vc-label{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#4a5568;text-transform:uppercase;letter-spacing:.14em;margin-bottom:10px}
.vc-value{font-family:'Barlow Condensed',sans-serif;font-size:1.9rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;line-height:1;margin-bottom:8px}
.vc-bar-bg{background:#1e2235;height:3px;border-radius:1px;margin-bottom:8px}
.vc-bar{height:3px;border-radius:1px}
.vc-detail{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#4a5568;line-height:1.6}
.vc-method{display:inline-block;margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#374151;border:1px solid #1e2235;padding:2px 6px;border-radius:2px}
.rec-strip{border:1px solid #f59e0b33;border-left:3px solid #f59e0b;background:#0e0c07;border-radius:2px;padding:16px 20px;margin-bottom:16px}
.rec-label{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.14em;margin-bottom:6px}
.rec-value{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:700;color:#f0f0f0;text-transform:uppercase}
.rec-reason{font-family:'Barlow',sans-serif;font-size:.78rem;color:#4a5568;margin-top:4px}
.alert-high{border:1px solid #ef444466;border-left:3px solid #ef4444;background:#0f0505;border-radius:2px;padding:14px 18px;margin-bottom:14px;font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#ef4444;letter-spacing:.06em}
.alert-review{border:1px solid #f59e0b44;border-left:3px solid #f59e0b;background:#0e0c07;border-radius:2px;padding:14px 18px;margin-bottom:14px;font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#f59e0b;letter-spacing:.06em}
.draft-panel{border:1px solid #1e2235;border-radius:2px;overflow:hidden;margin-top:16px}
.draft-hdr{background:#0c0e14;padding:10px 16px;border-bottom:1px solid #1e2235;display:flex;align-items:center;justify-content:space-between}
.draft-hdr-title{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.14em}
.draft-hdr-src{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#374151}
.draft-body{background:#080a0f;padding:20px;font-family:'Barlow',sans-serif;font-size:.88rem;color:#9ca3af;line-height:1.75;white-space:pre-wrap}
.draft-ftr{background:#0c0e14;padding:8px 16px;border-top:1px solid #1e2235;font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#374151}
""")

add_sidebar()

def get_openai_client():
    try:
        from openai import OpenAI
        key = st.secrets.get("OPENAI_API_KEY", "")
        return OpenAI(api_key=key) if key else None
    except Exception:
        return None

def enhance_with_openai(client, result):
    if not client:
        return result["first_response_draft"], False
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a professional IT helpdesk support agent. Write a concise, empathetic first-response email. Max 150 words. Never promise specific resolution times. End with: Best regards, TriageIQ Support Team"},
                {"role":"user","content":f"Subject: {result['subject']}\nBody: {result['body']}\nPriority: {result['predicted_priority']}\nTeam: {result['predicted_routing_team']}\nSLA: {result['sla_risk_level']}\nAction: {result['final_recommendation']}\n\nWrite the response email."}
            ],
            max_tokens=300, temperature=0.4
        )
        return r.choices[0].message.content.strip(), True
    except Exception:
        return result["first_response_draft"], False

PRESETS = {
    "— select a demo ticket —": {},
    "🔴  Payment gateway down (HIGH)": {"subject":"Payment gateway down for all customers","body":"Customers are unable to complete checkout. Multiple users are reporting failed payment transactions since this morning.","channel":"web form","subscription_type":"enterprise","customer_segment":"corporate","previous_tickets":8,"issue_complexity_score":9},
    "🟢  Password reset (NORMAL)": {"subject":"Need password reset","body":"I forgot my password and cannot log in to my account. Please help me reset it.","channel":"email","subscription_type":"basic","customer_segment":"individual","previous_tickets":1,"issue_complexity_score":2},
    "🟡  Laptop screen flickering (NEEDS REVIEW)": {"subject":"Laptop screen flickering during meetings","body":"My laptop screen keeps flickering whenever I connect it to the external monitor during client meetings.","channel":"chat","subscription_type":"premium","customer_segment":"small business","previous_tickets":3,"issue_complexity_score":5},
    "🔴  API 500 errors blocking production (HIGH)": {"subject":"API returning 500 errors","body":"Our production API integration is failing with repeated 500 errors. This is blocking order processing for our operations team.","channel":"web form","subscription_type":"enterprise","customer_segment":"corporate","previous_tickets":5,"issue_complexity_score":8},
    "🟢  Invoice question (NORMAL)": {"subject":"Question about invoice","body":"I have a question about a recent invoice charge. Can someone explain what this fee is for?","channel":"email","subscription_type":"basic","customer_segment":"individual","previous_tickets":0,"issue_complexity_score":2},
}

st.html("""
<div class="tiq-page-header">
  <div class="tiq-eyebrow">Section 02 // Live Inference</div>
  <div class="tiq-h1">Live Demo</div>
  <div class="tiq-sub">Submit a ticket and watch the full triage pipeline run in real time.</div>
</div>
""")

st.html('<div class="tiq-section">Ticket Input</div>')

preset_key = st.selectbox("Load demo ticket", list(PRESETS.keys()), label_visibility="collapsed")
p = PRESETS[preset_key]

CHANNELS = ["web form","email","chat","phone","social media"]
SUBS     = ["basic","premium","enterprise"]
SEGS     = ["individual","small business","business","corporate","enterprise"]

col_l, col_r = st.columns([3, 2])
with col_l:
    subject = st.text_input("Subject", value=p.get("subject",""), placeholder="e.g. Payment gateway down for all customers")
    body    = st.text_area("Body", value=p.get("body",""), height=130, placeholder="Describe the issue...")
with col_r:
    channel           = st.selectbox("Channel",          CHANNELS, index=CHANNELS.index(p.get("channel","web form")))
    subscription_type = st.selectbox("Subscription",     SUBS,     index=SUBS.index(p.get("subscription_type","premium")))
    customer_segment  = st.selectbox("Customer Segment", SEGS,     index=SEGS.index(p.get("customer_segment","small business")))
    previous_tickets  = st.number_input("Previous Tickets", 0, 50, int(p.get("previous_tickets", 2)))
    issue_complexity  = st.slider("Complexity (1–10)", 1, 10, int(p.get("issue_complexity_score", 5)))

run = st.button("▶  RUN TRIAGE", type="primary", use_container_width=True)

if run:
    if not subject.strip() or not body.strip():
        st.error("Subject and body are required.")
        st.stop()

    with st.spinner("Running triage pipeline..."):
        result = triageiq_predict(
            subject=subject, body=body, channel=channel,
            subscription_type=subscription_type, customer_segment=customer_segment,
            previous_tickets=previous_tickets, issue_complexity_score=issue_complexity
        )
        draft = result["first_response_draft"]
        used_ai = False

    st.html('<div class="tiq-section">Triage Output</div>')

    if result["predicted_priority"] == "High":
        st.html('<div class="alert-high">⚠ HIGH PRIORITY — ESCALATE TO HUMAN AGENT IMMEDIATELY. CONFIRMATION REQUIRED BEFORE ANY ACTION.</div>')
    elif result["predicted_priority"] == "Needs Review":
        st.html('<div class="alert-review">△ NEEDS REVIEW — SEND TO HUMAN TRIAGE BEFORE ROUTING. CONFIDENCE IN REVIEW BAND.</div>')

    pc = PRIORITY_COLORS.get(result["predicted_priority"], "#888")
    rc = ROUTING_COLORS.get(result["predicted_routing_team"], "#888")
    sc = SLA_COLORS.get(result["sla_risk_level"], "#888")
    ph = int(result["priority_high_probability"] * 100)
    rh = int(result["routing_confidence"] * 100)
    sh = int(result["sla_breach_probability"] * 100)

    st.html(f"""
    <div class="verdict-strip">
      <div class="verdict-cell">
        <div class="vc-label">01 // Priority</div>
        <div class="vc-value" style="color:{pc}">{result['predicted_priority']}</div>
        <div class="vc-bar-bg"><div class="vc-bar" style="width:{ph}%;background:{pc}"></div></div>
        <div class="vc-detail">P(High) = {result['priority_high_probability']:.2%}<br>{result['priority_action']}</div>
      </div>
      <div class="verdict-cell">
        <div class="vc-label">02 // Routing</div>
        <div class="vc-value" style="color:{rc};font-size:1.3rem">{result['predicted_routing_team']}</div>
        <div class="vc-bar-bg"><div class="vc-bar" style="width:{rh}%;background:{rc}"></div></div>
        <div class="vc-detail">Confidence = {result['routing_confidence']:.2%}<br>{result['routing_action']}</div>
        <span class="vc-method">{result['routing_method']}</span>
      </div>
      <div class="verdict-cell">
        <div class="vc-label">03 // SLA Risk</div>
        <div class="vc-value" style="color:{sc};font-size:1.3rem">{result['sla_risk_level']}</div>
        <div class="vc-bar-bg"><div class="vc-bar" style="width:{sh}%;background:{sc}"></div></div>
        <div class="vc-detail">Score = {result['sla_risk_score']}/10 · Breach prob = {result['sla_breach_probability']:.0%}<br>{result['sla_action']}</div>
        <span class="vc-method">Rule-based scoring</span>
      </div>
    </div>
    <div class="rec-strip">
      <div class="rec-label">Final Recommendation</div>
      <div class="rec-value">{result['final_recommendation']}</div>
      <div class="rec-reason">Human review required · {result['human_review_reason']}</div>
    </div>
    """)

    
    st.html(f"""
    <div class="draft-panel">
      <div class="draft-hdr">
        <span class="draft-hdr-title">AI-Generated First Response Draft</span>
      </div>
      <div class="draft-body">{draft}</div>
      <div class="draft-ftr">⚠ THIS DRAFT MUST BE REVIEWED BY A SUPPORT AGENT BEFORE SENDING</div>
    </div>
    """)
