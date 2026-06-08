# TriageIQ — File Placement Guide

## models/
Place both pkl files here:
- final_priority_model.pkl
- final_grouped_queue_routing_model.pkl

## data/
Place all output CSVs from the notebook here:
- triageiq_dashboard_data.csv
- triageiq_dashboard_data_with_rule_sla.csv
- final_business_kpi_cards.csv
- final_business_kpi_summary.csv
- triageiq_demo_tickets.csv
- triageiq_demo_predictions_with_responses.csv
- final_demo_prediction_summary.csv
- triageiq_app_config.csv
- final_model_comparison_summary.csv
- final_model_performance_all.csv
- routing_confidence_bucket_summary.csv
- routing_group_mapping.csv
- final_executive_summary.csv
- final_project_narrative_summary.csv
- final_responsible_ai_summary.csv

## .streamlit/secrets.toml
Add your OpenAI API key:
OPENAI_API_KEY = "your-key-here"
