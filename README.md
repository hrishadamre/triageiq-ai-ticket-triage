````markdown
<div align="center">

# TriageIQ — AI-Powered Support Ticket Triage

### A human-in-the-loop AI system that helps support teams prioritize tickets, route issues, score SLA risk, and draft first responses.

<br>

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn)
![XGBoost](https://img.shields.io/badge/XGBoost-Modeling-green?style=for-the-badge)
![Responsible AI](https://img.shields.io/badge/Responsible_AI-Human_in_the_Loop-purple?style=for-the-badge)

<br>

**Machine Learning | Business Analytics | Support Operations | Streamlit Product Demo**

</div>

---

## Project Overview

**TriageIQ** is an AI-assisted ticket triage system designed for IT helpdesk and customer support teams. The project addresses a common operational challenge: support teams spend significant time manually reading tickets, deciding urgency, routing issues to the correct team, checking SLA risk, and writing first responses.

TriageIQ helps automate the first layer of analysis while keeping humans in control. It predicts ticket priority, recommends a support routing group, scores SLA risk, and generates a first-response draft for agent review.

---

## Business Problem

Support teams often handle hundreds or thousands of tickets every month. Before an issue can be solved, someone must first read the ticket, understand the urgency, assign it to the correct team, and send an initial response.

This manual triage process can create:

| Problem | Business Impact |
|---|---|
| Slow manual triage | Delayed first response and higher operating cost |
| Inconsistent priority decisions | Urgent tickets may be missed or over-escalated |
| Wrong queue routing | Tickets bounce between teams and resolution slows down |
| Limited SLA visibility | Managers react after tickets are already late |
| Repetitive response drafting | Agents spend time writing similar messages repeatedly |

TriageIQ is built to reduce this friction and make early support operations faster, more consistent, and easier to monitor.

---

## What TriageIQ Does

When a support ticket is entered, TriageIQ returns:

| Output | Description |
|---|---|
| **Priority Prediction** | Classifies the ticket as `High`, `Needs Review`, or `Normal` |
| **Routing Group** | Recommends the broad support group that should handle the ticket |
| **SLA Risk Score** | Labels the ticket as `Low`, `Medium`, or `High SLA Risk` |
| **Final Recommendation** | Suggests the next operational action |
| **Response Draft** | Generates a first-response draft for a human agent to review |

---

## End-to-End Workflow

```text
Incoming Ticket
      ↓
Text Cleaning + Feature Preparation
      ↓
Priority Detection Model
      ↓
Grouped Queue Routing Model
      ↓
Rule-Based SLA Risk Scoring
      ↓
Final Recommendation
      ↓
Human-Reviewed Response Draft
````

---

## Key Results

| Component                            | Final Result | Interpretation                                          |
| ------------------------------------ | -----------: | ------------------------------------------------------- |
| **High-Priority Recall**             |         ~95% | Captures most urgent tickets                            |
| **Priority ROC-AUC**                 |         ~80% | Meaningful ability to distinguish urgent tickets        |
| **Baseline Routing Accuracy**        |         ~55% | Original queue labels were highly overlapping           |
| **Grouped Routing Accuracy**         |       ~80.6% | Improved after grouping similar support queues          |
| **Grouped Routing Weighted F1**      |       ~80.1% | Stronger performance across grouped classes             |
| **High-Confidence Routing Accuracy** |       ~95.6% | Supports auto-routing only when confidence is high      |
| **SLA ML ROC-AUC**                   |   ~0.49–0.50 | ML was rejected because performance was close to random |

---

## Why the Results Matter

The priority model is optimized for **high recall** because missing an urgent ticket is more costly than sending an extra ticket to human review.

The routing model improves significantly after grouping overlapping queue labels into business-friendly support routes. This makes the system more realistic for first-level triage.

The SLA machine learning models are intentionally not used in the final workflow because they do not show reliable predictive signal. Instead, TriageIQ uses transparent rule-based SLA scoring.

This makes the final system more credible, explainable, and safer for business use.

---

## Core Capabilities

### 1. Priority Detection

The priority model uses ticket text to classify tickets into:

```text
High
Needs Review
Normal
```

The model is designed to reduce missed urgent tickets. Borderline cases are placed into a **Needs Review** category instead of being ignored or automatically escalated.

---

### 2. Grouped Queue Routing

The first routing model attempted to predict detailed queue labels. However, many labels overlapped, such as Technical Support, IT Support, Product Support, and Service Outages.

To improve routing, similar queues were grouped into broader business-friendly routes.

| Original Queue Labels                                           | Grouped Routing Label       |
| --------------------------------------------------------------- | --------------------------- |
| Technical Support, IT Support, Product Support, Service Outages | Technical / Product Support |
| Billing and Payments                                            | Billing                     |
| Customer Service, Returns, General Inquiry                      | Customer Service            |
| Sales, Human Resources                                          | Business Support            |

This improved routing accuracy from approximately **55%** to **80.6%**.

---

### 3. Routing Confidence Logic

TriageIQ does not treat all routing predictions equally. It uses routing confidence to decide whether human review is needed.

| Confidence Level  | Accuracy | Recommended Action                    |
| ----------------- | -------: | ------------------------------------- |
| Low Confidence    |     ~50% | Manual triage required                |
| Medium Confidence |     ~72% | Route with human review               |
| High Confidence   |   ~95.6% | Candidate for auto-routing with audit |

This supports a practical human-in-the-loop design.

---

### 4. SLA Risk Scoring

SLA breach prediction using Logistic Regression and XGBoost performed close to random. Because of this, the final system uses a transparent rule-based SLA risk score.

The SLA risk score considers:

* Predicted priority
* Issue complexity
* Subscription type
* Customer segment
* Previous ticket count
* Support channel

Final SLA labels:

```text
Low SLA Risk
Medium SLA Risk
High SLA Risk
```

---

### 5. Response Drafting

TriageIQ generates a first-response draft based on the ticket details, predicted priority, routing group, and SLA risk.

The response is not automatically sent. It is designed for **human review** before any customer-facing action.

---

## Streamlit App Preview

> Add screenshots after placing images inside `assets/screenshots/`.

### Dashboard Preview

![Dashboard Preview](assets/screenshots/dashboard_preview.png)

### Live Triage Demo

![Live Triage Demo](assets/screenshots/live_triage_demo.png)

### Model Performance Summary

![Model Performance](assets/screenshots/model_performance_summary.png)

---

## Technical Approach

| Step                      | Description                                                                                   |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **Data Loading**          | Loaded multiple support-ticket datasets for priority, routing, SLA analysis, and dashboarding |
| **Data Cleaning**         | Standardized columns, labels, dates, text fields, and ticket metadata                         |
| **Feature Engineering**   | Created cleaned ticket text, keyword flags, routing groups, priority labels, and SLA features |
| **Priority Modeling**     | Trained TF-IDF based supervised classifiers with recall-focused thresholding                  |
| **Routing Modeling**      | Built baseline routing, then improved performance through grouped business routes             |
| **SLA Modeling**          | Tested Logistic Regression and XGBoost; rejected weak ML and used rule-based scoring          |
| **Final Workflow**        | Combined priority, routing, SLA risk, recommendation logic, and response drafting             |
| **Streamlit Preparation** | Saved final models and dashboard-ready files for app integration                              |

---

## Tech Stack

| Category         | Tools                                                                  |
| ---------------- | ---------------------------------------------------------------------- |
| Language         | Python                                                                 |
| Data Processing  | Pandas, NumPy                                                          |
| Machine Learning | Scikit-learn, XGBoost                                                  |
| Text Features    | TF-IDF                                                                 |
| Modeling         | Logistic Regression, SGD Classifier, Linear Models, XGBoost            |
| Visualization    | Matplotlib, Plotly                                                     |
| App Prototype    | Streamlit                                                              |
| Environment      | Google Colab, VS Code                                                  |
| Responsible AI   | Human-in-the-loop design, confidence thresholds, transparent SLA rules |

---

## Repository Structure

```text
triageiq-ai-ticket-triage/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── TriageIQ_Final_Modeling_Notebook.ipynb
│
├── streamlit_app/
│   ├── app.py
│   ├── README.md
│   │
│   ├── data/
│   │   ├── triageiq_dashboard_data.csv
│   │   ├── triageiq_dashboard_data_with_rule_sla.csv
│   │   ├── final_business_kpi_cards.csv
│   │   ├── final_business_kpi_summary.csv
│   │   ├── triageiq_demo_tickets.csv
│   │   ├── triageiq_demo_predictions_with_responses.csv
│   │   ├── final_demo_prediction_summary.csv
│   │   ├── triageiq_app_config.csv
│   │   ├── final_model_comparison_summary.csv
│   │   ├── final_model_performance_all.csv
│   │   ├── routing_confidence_bucket_summary.csv
│   │   ├── routing_group_mapping.csv
│   │   ├── final_executive_summary.csv
│   │   ├── final_project_narrative_summary.csv
│   │   └── final_responsible_ai_summary.csv
│   │
│   ├── models/
│   │   ├── final_priority_model.pkl
│   │   └── final_grouped_queue_routing_model.pkl
│   │
│   ├── pages/
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Live_Triage_Demo.py
│   │   ├── 3_Model_Performance.py
│   │   └── 4_Responsible_AI.py
│   │
│   └── utils/
│       ├── preprocessing.py
│       ├── prediction.py
│       └── response_generator.py
│
├── reports/
│   ├── TriageIQ_Project_Report.pdf
│   ├── TriageIQ_Final_Presentation.pdf
│   └── TriageIQ_InDepth_Project_Documentation.pdf
│
├── assets/
│   ├── screenshots/
│   │   ├── dashboard_preview.png
│   │   ├── live_triage_demo.png
│   │   ├── model_performance_summary.png
│   │   └── workflow_diagram.png
│   │
│   └── demo/
│       └── demo_video_link.md
│
└── docs/
    ├── technical_implementation.md
    ├── data_dictionary.md
    ├── model_card.md
    └── responsible_ai_notes.md
```

---

## Important Files

### Model Files

| File                                    | Purpose                                   |
| --------------------------------------- | ----------------------------------------- |
| `final_priority_model.pkl`              | Predicts ticket priority                  |
| `final_grouped_queue_routing_model.pkl` | Predicts grouped support routing category |

### App and Dashboard Files

| File                                           | Purpose                                        |
| ---------------------------------------------- | ---------------------------------------------- |
| `triageiq_dashboard_data.csv`                  | Main dashboard dataset                         |
| `triageiq_dashboard_data_with_rule_sla.csv`    | Dashboard data with SLA risk labels            |
| `final_business_kpi_cards.csv`                 | KPI card values for the dashboard              |
| `triageiq_app_config.csv`                      | Thresholds and configuration used by the app   |
| `triageiq_demo_predictions_with_responses.csv` | Demo predictions and generated response drafts |
| `final_model_comparison_summary.csv`           | Final model/component summary                  |
| `routing_confidence_bucket_summary.csv`        | Routing confidence and accuracy analysis       |
| `final_responsible_ai_summary.csv`             | Responsible AI risks and mitigations           |

---

## Streamlit App Flow

The Streamlit app uses saved models and final output files. It does not retrain models.

```text
Load saved models
      ↓
Load final dashboard files
      ↓
Display support KPIs and charts
      ↓
User enters a support ticket
      ↓
Predict priority
      ↓
Predict routing group
      ↓
Calculate SLA risk
      ↓
Generate final recommendation
      ↓
Display response draft for human review
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/triageiq-ai-ticket-triage.git
cd triageiq-ai-ticket-triage
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install requirements

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
python -m streamlit run streamlit_app/app.py
```

The app should open at:

```text
http://localhost:8501
```

---

## Optional LLM Support

TriageIQ can run without an OpenAI API key. The core app uses saved ML models and rule-based logic.

If an OpenAI API key is provided, the app can optionally generate more customized ticket summaries and response drafts.

```text
Without OpenAI key:
ML predictions + rule-based SLA + template response draft

With OpenAI key:
ML predictions + rule-based SLA + LLM-generated summary and response draft
```

If using the LLM feature, create:

```text
streamlit_app/.streamlit/secrets.toml
```

Add:

```toml
OPENAI_API_KEY = "your-key-here"
```

Do not commit this file to GitHub.

---

## Responsible AI Design

TriageIQ is intentionally designed as a human-in-the-loop system.

| Risk                  | Mitigation                                             |
| --------------------- | ------------------------------------------------------ |
| Missed urgent tickets | Prioritize high recall and use a Needs Review category |
| False escalations     | Separate High from Needs Review                        |
| Wrong routing         | Use confidence thresholds and manual review            |
| Weak SLA ML signal    | Use transparent rule-based SLA scoring                 |
| AI response risk      | Require human review before sending responses          |
| Data limitations      | Clearly state synthetic/anonymized data limitations    |

---

## Limitations

| Limitation                | Explanation                                                                     |
| ------------------------- | ------------------------------------------------------------------------------- |
| Synthetic/anonymized data | Some datasets may not fully reflect real production ticket behavior             |
| Grouped routing labels    | The model predicts broad support groups, not every detailed sub-team            |
| SLA ML weakness           | ML did not predict SLA breach reliably, so rule-based scoring is used           |
| Human review required     | The system is designed to assist agents, not replace them                       |
| Production readiness      | Real deployment would require company-specific data, monitoring, and retraining |

---

## Future Improvements

* Integrate with Jira Service Management, Freshservice, Zendesk, or ServiceNow APIs
* Add an agent feedback loop to capture accepted, edited, and rejected predictions
* Improve multilingual routing using language-agnostic embeddings
* Enhance SLA prediction with operational features such as queue backlog and agent workload
* Add richer LLM-assisted summaries and response drafts
* Deploy the Streamlit app as an internal support operations demo
* Add monitoring dashboards for model drift and performance by segment

---

## Recruiter-Friendly Summary

Built **TriageIQ**, an AI-powered support ticket triage system using Python, TF-IDF, supervised machine learning, and rule-based SLA scoring to predict ticket priority, route support requests, identify SLA risk, and generate human-reviewed response drafts.

The project demonstrates applied machine learning, business analytics, model evaluation, responsible AI design, and product thinking through a working Streamlit prototype.

---

## Project Status

| Component                       | Status          |
| ------------------------------- | --------------- |
| Data cleaning and preprocessing | Complete        |
| Priority detection model        | Complete        |
| Grouped routing model           | Complete        |
| SLA risk scoring                | Complete        |
| Streamlit app                   | Working locally |
| Final dashboard files           | Complete        |
| Reports and documentation       | Complete        |
| UI/code enhancement             | In progress     |

---

## Author

**Hrishad Amre**
Master’s in Information Systems
Robert H. Smith School of Business
University of Maryland

```
```
