# 📈 BourseInsight — Performance & Risk Analysis
### Casablanca Stock Exchange | 2022 — 2026

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.1-336791) ![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811) ![Looker Studio](https://img.shields.io/badge/Looker_Studio-Dashboard-4285F4) ![Mistral AI](https://img.shields.io/badge/Mistral_AI-OCR-orange)

---

## 🎯 Project Overview

**BourseInsight** is an end-to-end data pipeline designed to **analyze the performance and risk of 78 companies listed on the Casablanca Stock Exchange (BVC)** over the period 2022–2026.

The Bourse de Casablanca publishes daily bulletins exclusively as raw PDF files — no API, no structured data. This project automates the entire process from PDF collection to interactive financial dashboards.

### Key Questions Answered
-  Which companies delivered the **best risk-adjusted returns**?
-  Which stocks carry the **highest risk exposure**?
-  Is the risk taken **adequately compensated**?
-  Which securities are the most **liquid and actively traded**?

---

## 🏗️ Pipeline Architecture

```
Official PDF Bulletins (600+)
        ↓
Automated PDF Collection (Python + requests)
        ↓
OCR Text Extraction (Mistral AI)
        ↓
Data Cleaning & Preprocessing (Python + Pandas)
        ↓
PostgreSQL Data Warehouse (8 tables — 540K+ rows)
        ↓
KPI Computation (Python + SQL)
        ↓
Interactive Dashboards (Power BI + Looker Studio)
```

---

## 🗄️ Data

| Table | Rows | Source | Description |
|-------|------|--------|-------------|
| `indices` | 20,804 | BVC PDFs | MASI and daily sector indices |
| `actions` | 46,585 | BVC PDFs | Equities listed on the main market |
| `droits` | 7,176 | BVC PDFs | Subscription and attribution rights |
| `obligations` | 15,790 | BVC PDFs | Listed corporate bonds |
| `physionomie` | 411,686 | BVC PDFs | Daily transactions and volumes |
| `kpis_societes` | 78 | Python computation | 11 KPIs per company |
| `kpi_synthese_indices` | 60 | SQL view | KPI summary per index |

**Total: 538,790 rows of financial data**

### Data Quality
| Issue | Before Cleaning | After Cleaning |
|-------|----------------|----------------|
| Parasite rows | +3,000 | 0 |
| Duplicates | +31,715 | 0 |
| Unnamed columns | 21 | 0 |
| Encoding variants | 50+ | Standardized UTF-8 |

---

## 📊 KPIs Computed

### Performance
| KPI | Formula |
|-----|---------|
| Annualized Return | `Mean(returns) × 252` |
| Cumulative Return | `Prod(1 + ri) - 1` |

### Risk
| KPI | Formula |
|-----|---------|
| Volatility | `Std(returns) × √252` |
| Max Drawdown | `Min((cumsum - peak) / peak)` |
| Beta | `Cov(stock, MASI) / Var(MASI)` |
| VaR 95% | `5th percentile of returns` |
| CVaR 95% | `Mean of losses beyond VaR` |

### Risk-Adjusted Performance
| KPI | Formula |
|-----|---------|
| Sharpe Ratio | `(Return - Rf) / Volatility` |
| Sortino Ratio | `(Return - Rf) / Downside Volatility` |
| Calmar Ratio | `Return / |Max Drawdown|` |
| Tracking Error | `Std(ri - rMASI) × √252` |

> Risk-free rate: **3.5%** (Moroccan Treasury Bills — 52 weeks)

---

## 🏆 Key Results

### Top 5 Companies by Sharpe Ratio

| Company | Ann. Return | Volatility | Sharpe Ratio |
|---------|------------|------------|--------------|
| SGTM S.A | 539% | 92.6% | 5.78 |
| TIMAR | 95.7% | 25.5% | 3.61 |
| CASH PLUS S.A | 273.9% | 100.6% | 2.69 |
| JET CONTRACTORS | 106.8% | 41.3% | 2.50 |
| AUTO NEJMA | 89.0% | 37.8% | 2.26 |

### Market Overview — MASI Index
- **Trend**: BULLISH (+100% growth between 2022–2025, 56% positive sessions)
- **Best daily gain**: +5.08% | **Worst daily loss**: -5.64%
- **Daily volatility**: 0.78%
- **Total market volume**: 1.42T | 1.03Bn contracts processed

### Sector Highlights
-  **BMC (Mining)** leads with avg annualized return of **83%**
-  **18–22% of stocks are illiquid** — critical signal for investors
-  Most sectors show a Sharpe Ratio close to 0 → risk is rarely well-compensated

---

##  Project Structure

```
bourse-casablanca-analytics/
│
├── DATA_BULLETINS_WITH_TYPE/    # Markdown files by category
│   ├── Indices/
│   ├── Actions/
│   ├── Droits/
│   ├── Obligations/
│   └── Physionomie/
│
├── base/                        # Final cleaned CSV files
│   ├── Indices_FINAL.csv
│   ├── Actions_FINAL.csv
│   ├── Droits_FINAL.csv
│   ├── Obligations_FINAL.csv
│   └── Physionomie_FINAL.csv
│
├── notebooks/
│   ├── automatisation.ipynb     # Automated PDF download
│   ├── markdown.ipynb           # OCR extraction
│   ├── conversion_csv.ipynb     # CSV conversion & merging
│   ├── API.ipynb                # API integration
│   ├── EDA/                     # Exploratory Data Analysis
│   └── KPIs_Societes.ipynb      # KPI computation
│
├── cleaning/
│   ├── indices.ipynb
│   ├── actions.ipynb
│   ├── droits.ipynb
│   ├── obligations.ipynb
│   └── physionomie.ipynb
│
├── scripts/
│   ├── load_to_postgresql.py    # PostgreSQL data loading
│   ├── ajout_date_seance.py     # Date column processing
│   ├── calcul_kpis.py           # KPI computation
│   ├── kpis_sql.sql             # SQL KPI views
│   └── temps_reel.py            # Real-time data via Yahoo Finance
│
├── TECHNICAL_DOCUMENTATION/
├── KPIs_Societes.csv
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 18.1
- Power BI Desktop
- JupyterLab

### Python Dependencies
```bash
pip install pandas numpy sqlalchemy psycopg2-binary yfinance requests jupyter
```

### PostgreSQL Setup
```sql
-- Create the database in pgAdmin
CREATE DATABASE bourse_casablanca;
```

```bash
# Load the data
python scripts/load_to_postgresql.py
```

### Run the Pipeline
```bash
# Step 1 — Download PDFs
jupyter nbconvert --to notebook --execute "notebooks/automatisation.ipynb"

# Step 2 — OCR extraction
jupyter nbconvert --to notebook --execute "notebooks/markdown.ipynb"

# Step 3 — Convert to CSV
jupyter nbconvert --to notebook --execute "notebooks/conversion_csv.ipynb"

# Step 4 — Clean the data
python cleaning/indices.py
python cleaning/actions.py
python cleaning/droits.py
python cleaning/obligations.py
python cleaning/physionomie.py

# Step 5 — Load into PostgreSQL
python scripts/load_to_postgresql.py

# Step 6 — Compute KPIs
jupyter nbconvert --to notebook --execute "notebooks/KPIs_Societes.ipynb"
```

---

## 📊 Dashboards

### Power BI (5 pages)
| Page | Title | KPIs |
|------|-------|------|
| 1 | Market Overview | MASI value, trend, volatility |
| 2 | Company Performance | Sharpe, return, Risk/Return scatter |
| 3 | Risk Analysis | Max Drawdown, VaR 95%, Beta |
| 4 | Sector Analysis | Treemap, sector volatility |
| 5 | Liquidity & Transactions | Volume, transactions, ADV |

### Looker Studio (3 pages)
| Page | Title | Content |
|------|-------|---------|
| 1 | Overview & Performance | Top 10 Sharpe, return by sector, Risk vs Return |
| 2 | Risk Analysis | Max Drawdown, VaR 95%, Beta distribution |
| 3 | Company Ranking | Full ranking of 78 companies, Volatility vs Sharpe |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| OCR | Mistral AI (mistral-ocr-latest) |
| Data Manipulation | Pandas, NumPy |
| Database | PostgreSQL 18.1 |
| ORM | SQLAlchemy + psycopg2 |
| Finance Data | yfinance |
| Notebooks | JupyterLab |
| Visualization | Power BI Desktop, Looker Studio |
| Version Control | GitHub |

---

## 📄 License

This project was developed as a **graduation project** for the Data Analyst program at Simplon Maghreb × Jobintech (RNCP Level 6).

---

*BourseInsight — Turning Moroccan Market Data into Financial Insights 🇲🇦*
