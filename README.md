# 📊 AI-Powered Data Analyst Dashboard

An interactive data analyst dashboard built with **Python, pandas, and Streamlit**,
with a natural-language **"Ask your data"** feature powered by a free LLM API (Groq).

Built to demonstrate end-to-end data analyst / BA skills: data cleaning, KPI
definition, aggregation, visualization, and translating a plain-English business
question into an answer grounded in the actual data.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **KPI dashboard** — total sales, profit, average order value, order count, profit margin
- **Interactive filters** — region, category, date range
- **Charts** — monthly sales/profit trend, sales by region, sales by category, top products
- **Data cleaning pipeline** — handles missing values, type conversion, derived columns
- **AI Q&A box** — ask a question like *"Which region has the highest profit margin?"*
  and get a plain-English answer grounded in the filtered data (via Groq's free API)
- Works fully **offline** (dashboard + raw data summary) even without an API key

## Tech stack

| Layer | Tool |
|---|---|
| Data processing | pandas, numpy |
| Visualization | Plotly |
| App / UI | Streamlit |
| AI Q&A | Groq API (`llama-3.1-8b-instant`, free tier) |

## Project structure

```
ai-data-analyst-project/
├── app.py                  # Streamlit dashboard + AI Q&A
├── generate_data.py        # Creates the synthetic dataset (run once)
├── utils/
│   └── data_utils.py       # Cleaning, KPI, and aggregation functions
├── data/
│   └── sample_sales_data.csv
├── requirements.txt
├── .env.example
└── README.md
```

## Setup (all free)

### 1. Clone and set up environment
```bash
git clone https://github.com/<your-username>/ai-data-analyst-project.git
cd ai-data-analyst-project
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate the sample dataset
```bash
python generate_data.py
```

### 3. (Optional) Enable the AI Q&A feature
The dashboard works without this step — you'll just see the raw data
summary instead of an AI-generated answer.

1. Get a **free** API key at [console.groq.com/keys](https://console.groq.com/keys)
   (no credit card required for the free tier).
2. Copy `.env.example` to `.env` and paste your key:
   ```
   GROQ_API_KEY=your_key_here
   ```

### 4. Run the app
```bash
streamlit run app.py
```
Open the local URL Streamlit prints (usually `http://localhost:8501`).

## How the AI Q&A works

Instead of sending the whole dataset to the LLM (slow, expensive, and risks
the model losing track of large tables), the app:
1. Aggregates the currently filtered data into a compact text summary (KPIs,
   sales by region/category, monthly trend).
2. Sends that summary + your question to Groq's free `llama-3.1-8b-instant` model.
3. The model is instructed to answer using only the numbers provided, so
   answers stay grounded in your actual filtered data.

## Deploying for free (optional, to get a live link)

1. Push this repo to GitHub (steps below).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click "New app," pick this repo and `app.py` as the entry point.
4. Add `GROQ_API_KEY` under "Secrets" in the app settings (same syntax as `.env`).
5. Deploy — you'll get a public `*.streamlit.app` URL to put on your resume/LinkedIn.

## Uploading this project to GitHub

```bash
# from inside the ai-data-analyst-project folder
git init
git add .
git commit -m "Initial commit: AI-powered data analyst dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-data-analyst-project.git
git push -u origin main
```

If you don't have a GitHub repo yet:
1. Go to [github.com/new](https://github.com/new)
2. Name it (e.g. `ai-data-analyst-project`), keep it Public, don't initialize
   with a README (you already have one)
3. Click "Create repository," then run the commands above using the URL it gives you

## Possible extensions (good for a v2 commit)

- Swap the synthetic CSV for a real public dataset (e.g. Kaggle's Superstore dataset)
- Add anomaly detection (flag months with unusual profit drops)
- Add a downloadable PDF/Excel export of the filtered view
- Add unit tests for `utils/data_utils.py` with `pytest`

## License

MIT — free to use and adapt.
