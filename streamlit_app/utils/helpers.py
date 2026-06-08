# =============================================================================
# utils/helpers.py
# TriageIQ — Shared Logic
# Ported directly from 2_0_TriageIQ.ipynb (Sections 4, 5B, 6, 7)
# =============================================================================

import re
import pickle
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

warnings.filterwarnings("ignore")

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR  = BASE_DIR / "data"

PRIORITY_MODEL_PATH = MODEL_DIR / "final_priority_model.pkl"
ROUTING_MODEL_PATH  = MODEL_DIR / "final_grouped_queue_routing_model.pkl"

# =============================================================================
# BUSINESS THRESHOLDS
# Sourced from Cell [9] — PATCH: Business-Friendly Priority Thresholds
# =============================================================================

NORMAL_PRIORITY_THRESHOLD = 0.20
HIGH_PRIORITY_THRESHOLD   = 0.55
AUTO_ROUTE_CONFIDENCE_THRESHOLD  = 0.80
MANUAL_REVIEW_ROUTING_THRESHOLD  = 0.50

# =============================================================================
# MODEL LOADING
# =============================================================================

_priority_model = None
_routing_model  = None

def load_models():
    global _priority_model, _routing_model
    if _priority_model is None:
        with open(PRIORITY_MODEL_PATH, "rb") as f:
            _priority_model = pickle.load(f)
    if _routing_model is None:
        with open(ROUTING_MODEL_PATH, "rb") as f:
            _routing_model = pickle.load(f)
    return _priority_model, _routing_model

# =============================================================================
# TEXT CLEANING — Cell [1]
# =============================================================================

def clean_text_basic(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# =============================================================================
# PRIORITY CLASSIFICATION — Cell [9]
# =============================================================================

def classify_priority_from_probability(prob_high):
    if prob_high >= HIGH_PRIORITY_THRESHOLD:
        return "High"
    elif prob_high >= NORMAL_PRIORITY_THRESHOLD:
        return "Needs Review"
    return "Normal"

def get_priority_action(priority_label):
    if priority_label == "High":
        return "Escalate immediately"
    elif priority_label == "Needs Review":
        return "Send to human triage review"
    return "Normal priority queue"

# =============================================================================
# ROUTING WITH KEYWORD OVERRIDE — Cell [17] Part C
# =============================================================================

ACCESS_KEYWORDS = [
    "password","login","log in","sign in","account access",
    "reset","locked","authentication","permission",
    "cannot access","can't access"
]

BILLING_KEYWORDS = [
    "invoice","billing","charge","refund","payment",
    "transaction","checkout","fee"
]

def route_with_business_override(routing_text, routing_model):
    text_lower = str(routing_text).lower()
    if any(kw in text_lower for kw in ACCESS_KEYWORDS):
        return "Technical / Product Support", 0.90, "Keyword override: access/account issue"
    elif any(kw in text_lower for kw in BILLING_KEYWORDS):
        return "Billing", 0.90, "Keyword override: billing/payment issue"
    else:
        predicted_queue = routing_model.predict([routing_text])[0]
        proba = routing_model.predict_proba([routing_text])[0]
        routing_confidence = float(np.max(proba))
        return predicted_queue, routing_confidence, "ML grouped routing model"

def get_queue_action(routing_confidence):
    if routing_confidence >= AUTO_ROUTE_CONFIDENCE_THRESHOLD:
        return "Auto-route approved"
    elif routing_confidence >= MANUAL_REVIEW_ROUTING_THRESHOLD:
        return "Route with agent confirmation"
    return "Manual triage required"

# =============================================================================
# RULE-BASED SLA RISK — Cell [15] Part A
# ML SLA models dropped (both ~0.50 AUC)
# =============================================================================

def rule_based_sla_risk(
    predicted_priority, issue_complexity_score=5,
    subscription_type="premium", customer_segment="small business",
    previous_tickets=2, channel="web form"
):
    score = 0

    if predicted_priority == "High":
        score += 3
    elif predicted_priority == "Needs Review":
        score += 1

    try:
        complexity = float(issue_complexity_score)
    except Exception:
        complexity = 5
    if complexity >= 8:
        score += 3
    elif complexity >= 5:
        score += 1

    sub = str(subscription_type).lower().strip()
    seg = str(customer_segment).lower().strip()
    if sub == "enterprise":
        score += 2
    elif sub == "premium":
        score += 1
    if seg in ["corporate", "enterprise"]:
        score += 2
    elif seg in ["small business", "business"]:
        score += 1

    try:
        prev = float(previous_tickets)
    except Exception:
        prev = 2
    if prev >= 6:
        score += 2
    elif prev >= 3:
        score += 1

    ch = str(channel).lower().strip()
    if ch in ["phone", "chat", "social media"]:
        score += 1

    if score >= 8:
        risk_level = "High SLA Risk"
        action = "Escalate or assign immediately"
    elif score >= 5:
        risk_level = "Medium SLA Risk"
        action = "Review queue and monitor closely"
    else:
        risk_level = "Low SLA Risk"
        action = "Normal handling"

    return {
        "sla_risk_score": score,
        "sla_breach_probability": round(min(score / 10, 0.95), 4),
        "sla_risk_level": risk_level,
        "sla_action": action
    }

# =============================================================================
# RECOMMENDATION + HUMAN REVIEW — Cell [17] Part B
# =============================================================================

def get_final_recommendation(predicted_priority, routing_confidence, sla_risk_level):
    if predicted_priority == "High" or sla_risk_level == "High SLA Risk":
        return "Escalate to human agent immediately"
    elif predicted_priority == "Needs Review":
        return "Send to human triage review before routing"
    elif routing_confidence < MANUAL_REVIEW_ROUTING_THRESHOLD:
        return "Manual triage required due to low routing confidence"
    elif sla_risk_level == "Medium SLA Risk":
        return "Assign quickly and monitor SLA"
    return "Route normally with AI-drafted first response"

def get_human_review_reason(predicted_priority, routing_confidence, sla_risk_level):
    reasons = []
    if predicted_priority in ["High", "Needs Review"]:
        reasons.append("priority requires agent review")
    if routing_confidence < AUTO_ROUTE_CONFIDENCE_THRESHOLD:
        reasons.append("routing confidence is not high enough for automatic routing")
    if sla_risk_level in ["High SLA Risk", "Medium SLA Risk"]:
        reasons.append("SLA risk should be monitored by a support agent")
    reasons.append("AI-generated response should be reviewed before sending")
    return "; ".join(reasons)

# =============================================================================
# TEMPLATE RESPONSE DRAFT — Cell [17] Part D
# Used as fallback if OpenAI call fails
# =============================================================================

def get_response_tone(predicted_priority, sla_risk_level):
    if predicted_priority == "High" or sla_risk_level == "High SLA Risk":
        return "urgent"
    elif predicted_priority == "Needs Review" or sla_risk_level == "Medium SLA Risk":
        return "careful"
    return "standard"

def get_next_step_message(predicted_priority, predicted_queue, sla_risk_level):
    if predicted_priority == "High" or sla_risk_level == "High SLA Risk":
        return (
            f"We are escalating this to the {predicted_queue} team for immediate review. "
            "Our team will prioritize the investigation and provide an update as soon as possible."
        )
    elif predicted_priority == "Needs Review" or sla_risk_level == "Medium SLA Risk":
        return (
            f"We are routing this to the {predicted_queue} team and flagging it for review. "
            "A support agent will verify the details and make sure it is handled within the expected service window."
        )
    return (
        f"We are assigning this to the {predicted_queue} team for review. "
        "They will investigate and follow up with the next update."
    )

def get_routing_specific_info_request(predicted_queue):
    q = str(predicted_queue).lower()
    if "billing" in q:
        return (
            "To help us review this faster, please share the invoice number, payment reference, "
            "transaction date, or a screenshot of the charge if available."
        )
    elif "technical" in q or "product" in q:
        return (
            "To help our technical team investigate faster, please share any error messages, screenshots, "
            "timestamps, affected users, browser/device details, or recent changes."
        )
    elif "customer" in q:
        return (
            "To help us assist you faster, please share your order ID, account details, "
            "or any screenshots related to the request."
        )
    elif "business" in q:
        return (
            "To help route this correctly, please share the department, request type, timeline, "
            "and any relevant business context."
        )
    return (
        "Please share any additional details, screenshots, timestamps, or affected user information "
        "that may help us investigate."
    )

def generate_template_response(triage_result):
    subject           = triage_result.get("subject", "")
    predicted_priority = triage_result.get("predicted_priority", "Normal")
    predicted_queue   = triage_result.get("predicted_routing_team", "Support")
    sla_risk_level    = triage_result.get("sla_risk_level", "Low SLA Risk")

    tone      = get_response_tone(predicted_priority, sla_risk_level)
    next_step = get_next_step_message(predicted_priority, predicted_queue, sla_risk_level)
    extra_info = get_routing_specific_info_request(predicted_queue)

    if tone == "urgent":
        opening = (
            "Thank you for contacting support. We understand that this issue may be urgent "
            "and could affect normal business operations."
        )
    elif tone == "careful":
        opening = "Thank you for reaching out. We have received your ticket and are flagging it for careful review."
    else:
        opening = "Thank you for contacting support. We have received your ticket."

    return f"""Hello,

{opening}

We have received your ticket regarding: "{subject}".

{next_step}

{extra_info}

Best regards,
TriageIQ Support Team""".strip()

# =============================================================================
# MASTER PREDICTION FUNCTION — Cell [17] Part E
# =============================================================================

def triageiq_predict(
    subject, body,
    channel="web form",
    subscription_type="premium",
    customer_segment="small business",
    previous_tickets=2,
    issue_complexity_score=5,
    tags=""
):
    priority_model, routing_model = load_models()

    ticket_text  = clean_text_basic(f"{subject} {body}")
    routing_text = clean_text_basic(f"{subject} {body} {tags}")

    priority_proba   = priority_model.predict_proba([ticket_text])[0]
    probability_high = float(priority_proba[1])
    predicted_priority = classify_priority_from_probability(probability_high)
    priority_action    = get_priority_action(predicted_priority)

    predicted_queue, routing_confidence, routing_method = route_with_business_override(
        routing_text, routing_model
    )
    routing_action = get_queue_action(routing_confidence)

    sla = rule_based_sla_risk(
        predicted_priority=predicted_priority,
        issue_complexity_score=issue_complexity_score,
        subscription_type=subscription_type,
        customer_segment=customer_segment,
        previous_tickets=previous_tickets,
        channel=channel
    )

    final_recommendation = get_final_recommendation(
        predicted_priority, routing_confidence, sla["sla_risk_level"]
    )
    review_reason = get_human_review_reason(
        predicted_priority, routing_confidence, sla["sla_risk_level"]
    )

    result = {
        "subject":                   subject,
        "body":                      body,
        "predicted_priority":        predicted_priority,
        "priority_high_probability": round(probability_high, 4),
        "priority_action":           priority_action,
        "predicted_routing_team":    predicted_queue,
        "routing_confidence":        round(routing_confidence, 4),
        "routing_action":            routing_action,
        "routing_method":            routing_method,
        "sla_risk_score":            sla["sla_risk_score"],
        "sla_breach_probability":    sla["sla_breach_probability"],
        "sla_risk_level":            sla["sla_risk_level"],
        "sla_action":                sla["sla_action"],
        "final_recommendation":      final_recommendation,
        "human_review_required":     True,
        "human_review_reason":       review_reason,
    }
    result["first_response_draft"] = generate_template_response(result)
    return result

# =============================================================================
# DATA LOADING
# =============================================================================

def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def data_missing_warning(filename):
    return (
        f"**{filename}** not found in the `data/` folder. "
        "Export this file from the notebook and place it in `data/` to enable this section."
    )

# =============================================================================
# COLOR HELPERS — consistent across all pages
# =============================================================================

PRIORITY_COLORS = {
    "High":         "#FF4B4B",
    "Needs Review": "#FFA500",
    "Normal":       "#21C354"
}

SLA_COLORS = {
    "High SLA Risk":   "#FF4B4B",
    "Medium SLA Risk": "#FFA500",
    "Low SLA Risk":    "#21C354"
}

ROUTING_COLORS = {
    "Technical / Product Support": "#4B8BFF",
    "Billing":                     "#A855F7",
    "Customer Service":            "#06B6D4",
    "Business Support":            "#F59E0B"
}

def priority_badge(label):
    color = PRIORITY_COLORS.get(label, "#888")
    return f'<span style="background:{color};color:white;padding:3px 10px;border-radius:12px;font-weight:600">{label}</span>'

def sla_badge(label):
    color = SLA_COLORS.get(label, "#888")
    return f'<span style="background:{color};color:white;padding:3px 10px;border-radius:12px;font-weight:600">{label}</span>'
