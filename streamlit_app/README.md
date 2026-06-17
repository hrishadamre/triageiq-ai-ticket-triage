# TriageIQ Streamlit App

This folder contains the Streamlit app for the TriageIQ project.

The app loads the final trained models and final output files generated from the modeling notebook. It is used to run the dashboard, live ticket triage demo, model performance view, and responsible AI view.

The app does not retrain models.

---

## Folder Structure

```text
streamlit_app/
├── app.py
├── README.md
├── data/
├── models/
├── pages/
└── utils/
```

---

## Required Files

### Models

Place these files inside:

```text
streamlit_app/models/
```

```text
final_priority_model.pkl
final_grouped_queue_routing_model.pkl
```

### Data

Place the final CSV output files inside:

```text
streamlit_app/data/
```

Important files include:

```text
triageiq_dashboard_data.csv
triageiq_dashboard_data_with_rule_sla.csv
final_business_kpi_cards.csv
final_model_comparison_summary.csv
final_model_performance_all.csv
routing_confidence_bucket_summary.csv
triageiq_demo_predictions_with_responses.csv
final_responsible_ai_summary.csv
triageiq_app_config.csv
```

---

## Run the App

Run these commands from the **root project folder**, not from inside `streamlit_app`.

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app/app.py
```

### Windows / Anaconda Prompt

```bash
cd path\to\triageiq-ai-ticket-triage
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

The app will open at a local URL, usually:

```text
http://localhost:8501
```

---

## Optional OpenAI API Key

The app can run without an OpenAI API key.

An API key is only needed if the optional LLM-assisted response feature is enabled.

Create this file only if needed:

```text
streamlit_app/.streamlit/secrets.toml
```

Add:

```toml
OPENAI_API_KEY = "your-key-here"
```

---
