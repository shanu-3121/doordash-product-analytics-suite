# 🍔 AI-Powered Product Analytics Intelligence Suite
### DoorDash Case Study | Python · SQL · Streamlit · Gemini AI

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![SQL](https://img.shields.io/badge/SQL-SQLite-green)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

---

## 🎯 Project Overview

An end-to-end product analytics platform that mirrors the internal 
analytics workflows used at companies like DoorDash, Amazon, and Meta. 
Built on **99K real e-commerce orders** combined with **554K simulated 
behavioral events**, this project demonstrates how a Product Analyst 
thinks — from raw data to business decisions.

**Live Demo:** [Click here to view the dashboard](#) ← replace with your Streamlit link

---

## 📊 What's Inside

| Layer | What It Does |
|-------|-------------|
| **Data Foundation** | 99K real orders (Olist) + 554K Faker-generated behavioral events |
| **SQL Analytics** | 10 complex business queries across funnel, retention, churn & LTV |
| **A/B Testing** | Statistical significance testing with $966M projected revenue impact |
| **Interactive Dashboard** | 7-tab Streamlit app with filters by city, device, cuisine & user type |
| **AI Copilot** | Google Gemini-powered assistant answering plain-English business questions |

---

## 🔍 Key Business Findings

- **Funnel Drop-off:** 23.7% of users who reach checkout never complete their order
- **DashPass Impact:** DashPass users generate $415 revenue per user vs $125 for regular users — a 3.3x gap
- **Reorder Propensity:** Users who order 3+ times in Week 1 show 100% Day-30 retention
- **Churn Risk:** 3,753 At Risk + Churning users represent ~$650K in recoverable revenue
- **A/B Test:** New 2-step checkout lifts conversion by +7.4% (p < 0.001) — $966M annual impact at DoorDash scale
- **LTV by Channel:** Organic search users generate highest LTV at $189 per user

---

## 🛠️ Tech Stack
```
Python          — Data generation, analysis, and app backend
SQL (SQLite)    — 10 business queries across 4 tables
Faker           — Realistic behavioral event simulation
Streamlit       — Interactive web dashboard
Plotly          — Interactive visualizations
Google Gemini   — AI copilot for plain-English insights
Pandas          — Data manipulation and analysis
SciPy           — Statistical significance testing
```

---

## 📁 Project Structure
```
doordash-product-analytics-suite/
│
├── app.py                  # Main Streamlit dashboard (7 tabs)
├── generate_data.py        # Faker data generation script
├── sql_analytics.py        # 10 SQL business queries
├── ab_test_analysis.py     # A/B statistical significance test
│
├── data_users.csv          # 10,000 user profiles
├── data_orders.csv         # 66,557 order events
├── data_funnel.csv         # 554,923 funnel events
├── data_ab_test.csv        # 10,000 A/B test records
│
├── archive/                # Real Olist e-commerce dataset
├── .streamlit/             # Streamlit theme configuration
└── .gitignore              # Protecting API keys
```

---

## 🚀 Dashboard Tabs

1. **📈 Executive Summary** — KPI cards, revenue by cuisine, city treemap
2. **🔽 Funnel Analysis** — User journey waterfall with drop-off highlights
3. **🔄 Cohort Retention** — Monthly retention heatmap
4. **⭐ DashPass Intelligence** — DashPass vs Regular comparison + trends
5. **⚠️ Churn Risk** — RFM segmentation treemap + scatter plot
6. **🧪 A/B Test Results** — Checkout experiment with statistical proof
7. **🤖 AI Copilot** — Ask business questions, get data-backed answers

---

## 💡 Business Recommendations

| Finding | Recommendation |
|---------|---------------|
| 23.7% checkout drop-off | Ship new 2-step checkout — proven +7.4% lift |
| DashPass 3.3x revenue gap | Offer 30-day free trial to convert Regular users |
| Week 1 behavior predicts retention | Trigger "Order 3x this week, get free delivery" promo |
| 3,753 At Risk users | Launch win-back campaign before they go Lost |
| Organic search highest LTV | Reallocate 15% of paid social budget to SEO |

---

## 🏃 How To Run Locally
```bash
# Clone the repository
git clone https://github.com/shanu-3121/doordash-product-analytics-suite.git
cd doordash-product-analytics-suite

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Generate the data
python generate_data.py

# Run the app
streamlit run app.py
```

---

## 👤 About

**Shanu Venkatesan**  
MS Management of Technology — NYU Tandon School of Engineering  
2 years market & pricing analytics experience  

[LinkedIn](https://linkedin.com/in/shanu-venkatesan-analyst) | 
[GitHub](https://github.com/shanu-3121)

---

*This project mirrors real product analytics workflows used at 
DoorDash, Amazon, Meta, and HubSpot — built to demonstrate 
end-to-end analytical thinking from raw data to business decisions.*
