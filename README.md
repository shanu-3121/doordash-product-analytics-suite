# 🍔 AI-Powered Product Analytics Intelligence Suite
### DoorDash Case Study | Cloud ETL · Snowflake · dbt · Python · SQL · Streamlit · Gemini AI

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Snowflake](https://img.shields.io/badge/Cloud-Snowflake-lightblue)
![dbt](https://img.shields.io/badge/Transform-dbt-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

---

## 🏗️ Architecture Overview

This project mirrors the analytics stack used by product analysts at DoorDash, Amazon, and Meta — from raw data ingestion through cloud transformation to AI-assisted business insights.

Raw CSV Data (641K+ events)
↓
Snowflake Cloud Data Warehouse
↓
dbt Transformation Pipeline (staging → intermediate → mart)
↓
Streamlit Dashboard + Gemini AI Copilot

---

## 🗄️ Cloud Data Pipeline (Snowflake + dbt)

**641,480 events** loaded into Snowflake across 4 raw tables, then transformed through a 3-layer dbt pipeline:

| Layer | Models | Purpose |
|-------|--------|---------|
| **Staging** | stg_users, stg_orders, stg_funnel, stg_ab_test | Clean and standardize raw data |
| **Intermediate** | int_orders_users, int_user_metrics | Join tables, calculate user metrics |
| **Mart** | mart_dashpass_analysis, mart_ab_test_results | Final analytics-ready tables |

---

## 📊 Key Business Findings

| Metric | Finding |
|--------|---------|
| 💰 DashPass LTV Gap | DashPass users generate **$6,883 total spend vs $683** for regular users — a **10x gap** |
| 🔄 Week-1 Retention | Users who order **3+ times in Week 1** retain at **100% on Day 30** |
| 🧪 A/B Test Result | New 2-step checkout lifts conversion **+7.4%** (52.1% → 59.5%), p < 0.001 |
| 📉 Funnel Drop-off | **23.7%** of users who reach checkout never complete their order |
| ⚠️ Churn Risk | 3,753 At Risk + Churning users represent **~$650K in recoverable revenue** |
| 🔍 LTV by Channel | Organic search users generate highest LTV at **$189 per user** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Cloud Data Warehouse | Snowflake |
| Data Transformation | dbt (staging → intermediate → mart) |
| ETL Pipeline | Python, Snowflake Connector, Pandas |
| Analytics & SQL | Python, SQL, SciPy |
| Dashboard | Streamlit, Plotly |
| AI Copilot | Google Gemini API |
| Data Generation | Faker, Olist (99K real orders) |

---

## 📁 Project Structure

```
doordash-product-suite/
├── app.py                    # Streamlit dashboard (7 tabs)
├── generate_data.py          # Data generation script
├── sql_analytics.py          # 10 business SQL queries
├── load_to_snowflake.py      # ETL pipeline to Snowflake
├── data_users.csv            # 10,000 user profiles
├── data_orders.csv           # 66,557 order events
├── data_funnel.csv           # 554,923 funnel events
├── data_ab_test.csv          # 10,000 A/B test records
└── doordash_dbt/             # dbt project
    └── models/
        ├── staging/          # Raw data cleaning layer
        ├── intermediate/     # Joins & aggregations layer
        └── mart/             # Final analytics tables
```

---

## 🚀 Dashboard Tabs

1. **📈 Executive Summary** — KPI cards, revenue by cuisine, city treemap
2. **🔽 Funnel Analysis** — User journey waterfall with drop-off highlights
3. **🔄 Cohort Retention** — Monthly retention heatmap
4. **⭐ DashPass Intelligence** — DashPass vs Regular LTV comparison
5. **⚠️ Churn Risk** — RFM segmentation treemap + scatter plot
6. **🧪 A/B Test Results** — Checkout experiment with statistical proof
7. **🤖 AI Copilot** — Gemini-powered plain-English business insights

---

## 💡 Business Recommendations

| Finding | Recommendation |
|---------|---------------|
| 23.7% checkout drop-off | Ship new 2-step checkout — proven +7.4% lift |
| 10x DashPass LTV gap | Offer 30-day free trial to convert Regular users |
| Week 1 behavior predicts retention | Trigger "Order 3x this week, get free delivery" promo |
| 3,753 At Risk users | Launch win-back campaign before they go Lost |
| Organic search highest LTV | Reallocate 15% of paid social budget to SEO |

---

## 🏃 How To Run Locally

```bash
git clone https://github.com/shanu-3121/doordash-product-analytics-suite.git
cd doordash-product-analytics-suite
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Data

- **99,441** real orders from the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **554,923** simulated behavioral events generated with Faker
- **641,480 total events** loaded into Snowflake

---

## 👤 About

**Shanu Venkatesan**
MS Management of Technology — NYU Tandon School of Engineering
2 years market & pricing analytics experience

[LinkedIn](https://linkedin.com/in/shanu-venkatesan-analyst) |
[GitHub](https://github.com/shanu-3121)

---

*Built to mirror real product analytics workflows at DoorDash, Amazon, and Meta.*
