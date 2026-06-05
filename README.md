````markdown
# TriageIQ — AI-Powered Support Ticket Triage

> A human-in-the-loop AI workflow that helps support teams prioritize, route, and respond to incoming tickets faster and more consistently.

---

## Project Snapshot

| Area | Details |
|---|---|
| Project Type | Machine Learning + Business Analytics + AI Workflow |
| Domain | Customer Support / IT Service Management |
| Goal | Assist support teams with ticket priority detection, queue routing, SLA risk scoring, and response drafting |
| Main Users | Support agents, helpdesk teams, operations managers, customer support leads |
| Tools Used | Python, Pandas, Scikit-learn, XGBoost, TF-IDF, Streamlit |
| Final Output | Trained models, dashboard-ready files, demo predictions, responsible AI summary |

---

## Why This Project Matters

Support teams often spend a lot of time manually reading tickets, deciding urgency, routing issues to the correct team, and writing first responses.

This can lead to:

- Missed urgent tickets
- Delayed first response
- Incorrect routing
- Repeated handoffs between teams
- SLA risk
- Lower customer satisfaction

**TriageIQ** helps reduce this manual effort by providing AI-assisted recommendations while keeping humans in control.

---

## What TriageIQ Does

TriageIQ takes a support ticket as input and returns:

| Output | Description |
|---|---|
| Priority Prediction | Classifies the ticket as `High`, `Needs Review`, or `Normal` |
| Routing Group | Recommends the broad support group that should handle the issue |
| SLA Risk | Scores whether the ticket is at Low, Medium, or High SLA risk |
| Final Recommendation | Suggests what the support team should do next |
| Response Draft | Generates a first-response draft for human review |

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

## Key Business Questions Answered

| Business Question              | TriageIQ Output      |
| ------------------------------ | -------------------- |
| Is this ticket urgent?         | Priority prediction  |
| Which team should handle it?   | Routing group        |
| Is this ticket at SLA risk?    | SLA risk score       |
| What should the agent do next? | Final recommendation |
| What can the agent send first? | Draft response       |

---

## Core Features

### 1. Priority Detection

The priority model predicts whether a ticket is likely to be urgent.

The model is designed to prioritize **high recall**, because missing a truly urgent ticket is more costly than sending an extra ticket for human review.

Final priority labels:

```text
High
Needs Review
Normal
```

---

### 2. Grouped Queue Routing

The routing model recommends a broad support group.

The original queue labels were highly overlapping, so similar queues were grouped into more realistic first-level routing groups.

| Original Queues                                                 | Grouped Routing Label       |
| --------------------------------------------------------------- | --------------------------- |
| Technical Support, IT Support, Product Support, Service Outages | Technical / Product Support |
| Billing and Payments                                            | Billing                     |
| Customer Service, Returns, General Inquiry                      | Customer Service            |
| Sales, Human Resources                                          | Business Support            |

This improves routing reliability and makes the output easier for business users to interpret.

---

### 3. SLA Risk Scoring

SLA breach means the support team misses its promised response or resolution deadline.

Logistic Regression and XGBoost were tested for SLA breach prediction, but the models performed close to random. Instead of overclaiming weak model performance, the final system uses a transparent rule-based SLA risk score.

The SLA score considers:

* Predicted priority
* Issue complexity
* Subscription type
* Customer segment
* Previous ticket count
* Support channel

Final SLA risk labels:

```text
Low SLA Risk
Medium SLA Risk
High SLA Risk
```

---

### 4. Human-in-the-Loop Response Drafting

TriageIQ generates a first-response draft using the ticket details, predicted priority, routing group, and SLA risk.

The response is **not automatically sent**.

It is intended to be reviewed and edited by a human support agent.

---

## Final Model Results

### Priority Detection

| Metric               | Result |
| -------------------- | -----: |
| High-Priority Recall |   ~95% |
| ROC-AUC              |   ~80% |

**Interpretation:**
The model is strong at catching urgent tickets. This supports the business goal of reducing missed high-priority issues.

---

### Baseline Routing Model

| Metric      | Result |
| ----------- | -----: |
| Accuracy    |   ~55% |
| Weighted F1 |   ~55% |

**Interpretation:**
The baseline model struggled because the original queue labels were too similar and overlapping.

---

### Improved Grouped Routing Model

| Metric      | Result |
| ----------- | -----: |
| Accuracy    | ~80.6% |
| Weighted F1 | ~80.1% |

**Interpretation:**
Grouping overlapping support queues significantly improved routing performance.

---

### Routing Confidence Analysis

| Confidence Bucket | Accuracy |
| ----------------- | -------: |
| Low Confidence    |     ~50% |
| Medium Confidence |     ~72% |
| High Confidence   |   ~95.6% |

**Interpretation:**
High-confidence predictions are much safer for auto-routing. Medium and low confidence predictions should involve human review.

---

### SLA ML Experiment

| Model               | ROC-AUC |
| ------------------- | ------: |
| Logistic Regression |   ~0.49 |
| XGBoost             |   ~0.50 |

**Interpretation:**
The SLA machine learning models did not show reliable predictive power. The final system uses explainable rule-based scoring instead.

---

## Technical Approach

| Step                | Description                                                                                   |
| ------------------- | --------------------------------------------------------------------------------------------- |
| Data Loading        | Loaded multilingual ticket, IT ticket, and customer support datasets                          |
| Data Cleaning       | Standardized text, labels, dates, categories, and target fields                               |
| Feature Engineering | Created cleaned ticket text, keyword flags, priority labels, routing groups, and SLA features |
| Priority Modeling   | Trained supervised text classifiers using TF-IDF features                                     |
| Routing Modeling    | Built baseline and improved grouped routing models                                            |
| SLA Analysis        | Tested ML models and selected rule-based scoring due to weak predictive signal                |
| Final Workflow      | Combined priority, routing, SLA risk, recommendation, and response drafting                   |
| Streamlit Prep      | Saved only final models and dashboard-ready output files                                      |

---

## Tech Stack

| Category         | Tools                                       |
| ---------------- | ------------------------------------------- |
| Language         | Python                                      |
| Data Processing  | Pandas, NumPy                               |
| Machine Learning | Scikit-learn, XGBoost                       |
| Text Features    | TF-IDF                                      |
| Modeling         | Logistic Regression, Linear Models, XGBoost |
| Visualization    | Matplotlib, Plotly                          |
| App Prototype    | Streamlit                                   |
| Environment      | Google Colab                                |

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
│   └── TriageIQ_Final_Notebook.ipynb
│
├── streamlit_app/
│   ├── app.py
│   │
│   ├── pages/
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Live_Triage_Demo.py
│   │   ├── 3_Model_Performance.py
│   │   └── 4_Responsible_AI.py
│   │
│   ├── models/
│   │   ├── final_priority_model.pkl
│   │   └── final_grouped_queue_routing_model.pkl
│   │
│   └── outputs/
│       ├── triageiq_dashboard_data.csv
│       ├── triageiq_dashboard_data_with_rule_sla.csv
│       ├── final_business_kpi_cards.csv
│       ├── final_business_kpi_summary.csv
│       ├── triageiq_demo_tickets.csv
│       ├── triageiq_demo_predictions_with_responses.csv
│       ├── final_demo_prediction_summary.csv
│       ├── triageiq_app_config.csv
│       ├── final_model_comparison_summary.csv
│       ├── final_model_performance_all.csv
│       ├── routing_confidence_bucket_summary.csv
│       ├── routing_group_mapping.csv
│       ├── final_executive_summary.csv
│       ├── final_project_narrative_summary.csv
│       └── final_responsible_ai_summary.csv
│
├── reports/
│   ├── TriageIQ_Project_Report.pdf
│   └── TriageIQ_Final_Presentation.pdf
│
├── assets/
│   ├── workflow_diagram.png
│   ├── dashboard_preview.png
│   ├── live_triage_demo.png
│   └── model_performance_summary.png
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

| File                                    | Purpose                           |
| --------------------------------------- | --------------------------------- |
| `final_priority_model.pkl`              | Predicts ticket priority          |
| `final_grouped_queue_routing_model.pkl` | Predicts grouped routing category |

---

### Streamlit / Dashboard Files

| File                                        | Purpose                              |
| ------------------------------------------- | ------------------------------------ |
| `triageiq_dashboard_data.csv`               | Main dashboard dataset               |
| `triageiq_dashboard_data_with_rule_sla.csv` | Dashboard data with SLA risk scoring |
| `final_business_kpi_cards.csv`              | KPI values for dashboard cards       |
| `final_business_kpi_summary.csv`            | Business KPI explanation             |
| `triageiq_app_config.csv`                   | App thresholds and configuration     |

---

### Demo and Reporting Files

| File                                           | Purpose                               |
| ---------------------------------------------- | ------------------------------------- |
| `triageiq_demo_tickets.csv`                    | Sample tickets used for demo          |
| `triageiq_demo_predictions_with_responses.csv` | Full demo prediction output           |
| `final_demo_prediction_summary.csv`            | Short demo summary                    |
| `final_model_comparison_summary.csv`           | Final model/component summary         |
| `final_model_performance_all.csv`              | Detailed model performance table      |
| `routing_confidence_bucket_summary.csv`        | Accuracy by routing confidence bucket |
| `final_responsible_ai_summary.csv`             | Responsible AI risks and mitigations  |

---

## Streamlit App Plan

The Streamlit app is designed to use the saved model and output files. It does not retrain models.

Recommended pages:

| Page              | Purpose                                                       |
| ----------------- | ------------------------------------------------------------- |
| Dashboard         | Shows KPIs and ticket trends                                  |
| Live Triage Demo  | Lets users enter a new ticket and receive AI-assisted outputs |
| Model Performance | Shows final model results and confidence analysis             |
| Responsible AI    | Explains risks, limitations, and mitigation steps             |

---

## Streamlit App Flow

```text
Load final models
      ↓
Load final dashboard files
      ↓
Display support KPIs and charts
      ↓
User enters ticket subject and body
      ↓
Predict priority
      ↓
Predict routing group
      ↓
Calculate SLA risk
      ↓
Generate recommendation and response draft
      ↓
Human reviews output
```

---

## Example Triage Output

Example ticket:

```text
Subject: API returning 500 errors
Body: Our production API integration is failing with repeated 500 errors and blocking order processing.
```

Example TriageIQ output:

| Output         | Example                                         |
| -------------- | ----------------------------------------------- |
| Priority       | High / Needs Review                             |
| Routing Group  | Technical / Product Support                     |
| SLA Risk       | High SLA Risk                                   |
| Recommendation | Escalate or monitor closely                     |
| Response Draft | Professional customer response for agent review |

---

## Responsible AI Design

TriageIQ is intentionally designed as a human-in-the-loop system.

Key safeguards:

* AI-generated responses are not automatically sent
* Low-confidence routing predictions require review
* SLA risk uses transparent rules when ML performance is weak
* Priority predictions include a `Needs Review` zone
* Final decisions remain with support agents
* Limitations of synthetic and anonymized data are clearly stated

---

## Limitations

| Limitation                | Explanation                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| Synthetic/anonymized data | Some datasets may not fully reflect real production ticket behavior       |
| Grouped routing labels    | The model predicts broad routing groups, not every detailed sub-team      |
| SLA ML weakness           | SLA breach prediction did not perform well, so rule-based scoring is used |
| Human review required     | The system is not intended to fully automate support decisions            |
| Production readiness      | Real deployment would require company-specific ticket data and monitoring |

---

## Future Improvements

* Integrate an LLM for ticket summarization and response drafting
* Add real company ticket data for retraining and validation
* Build an agent feedback loop to improve predictions over time
* Monitor model performance by channel, customer segment, and language
* Improve SLA prediction using operational features such as queue backlog and agent workload
* Deploy the Streamlit app as an internal support operations demo

---

## Resume-Ready Project Summary

Built **TriageIQ**, an AI-powered support ticket triage system using Python, TF-IDF, supervised machine learning, and rule-based SLA scoring to predict ticket priority, route support requests, identify SLA risk, and generate human-reviewed response drafts.

Improved routing performance by grouping overlapping support queues into business-friendly categories and applying confidence-based human review logic.

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/your-username/triageiq-ai-ticket-triage.git
cd triageiq-ai-ticket-triage
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run streamlit_app/app.py
```

---

## Project Status

| Component               | Status                           |
| ----------------------- | -------------------------------- |
| Data cleaning notebook  | Complete                         |
| Priority model          | Complete                         |
| Grouped routing model   | Complete                         |
| SLA risk scoring        | Complete                         |
| Final output files      | Complete                         |
| Streamlit app           | Planned / In progress            |
| Report and presentation | Complete / Add to reports folder |

---

## Author

**Hrishad Amre**
Master’s in Information Systems
Robert H. Smith School of Business, University of Maryland

```
```
