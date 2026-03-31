# 📈 BourseInsight — Analyse de Performance & Risque
### Bourse de Casablanca | 2022 — 2026


---

##  Objectif du projet

Ce projet vise à construire un pipeline de données complet pour **analyser la performance et le risque des sociétés cotées à la Bourse de Casablanca** sur la période 2022-2026.

Il répond à 4 questions clés :
-  Quelles sociétés ont généré le **meilleur rendement** ?
-  Quelles actions présentent le **risque le plus élevé** ?
-  Le risque pris est-il **suffisamment récompensé** ?
-  Quels titres sont les plus **liquides et actifs** ?

---

##  Architecture du Pipeline
```
PDFs Officiels (600+)
        ↓
Téléchargement automatique (Python + requests)
        ↓
Extraction OCR (Mistral AI)
        ↓
Nettoyage & Préparation (Python + Pandas)
        ↓
PostgreSQL 18.1 (8 tables)
        ↓
Calcul KPIs (Python + SQL)
        ↓
Dashboard Power BI (5 pages)
```

---

##  Données

| Table | Lignes | Source | Description |
|-------|--------|--------|-------------|
| `indices` | 20 804 | PDFs BCFR | MASI et indices sectoriels quotidiens |
| `actions` | 46 585 | PDFs BCFR | Actions cotées au marché principal |
| `droits` | 7 176 | PDFs BCFR | Droits d'attribution et souscription |
| `obligations` | 15 790 | PDFs BCFR | Emprunts obligataires cotés |
| `physionomie` | 411 686 | PDFs BCFR | Transactions et volumes journaliers |
| `kpis_societes` | 78 | Calcul Python | 11 KPIs par société |
| `kpi_synthese_indices` | 60 | Vue SQL | Synthèse KPIs par indice |

**Total : 538 790 lignes de données**

---

##  KPIs Calculés

### Performance
| KPI | Formule |
|-----|---------|
| Rendement Annualisé | `Moyenne(rendements) × 252` |
| Rendement Cumulé | `Prod(1 + ri) - 1` |

### Risque
| KPI | Formule |
|-----|---------|
| Volatilité | `Écart-type(rendements) × √252` |
| Max Drawdown | `Min((cumul - peak) / peak)` |
| Bêta | `Cov(action, MASI) / Var(MASI)` |
| VaR 95% | `Percentile 5% des rendements` |
| CVaR 95% | `Moyenne des pertes au-delà de la VaR` |

### Rendement / Risque
| KPI | Formule |
|-----|---------|
| Ratio de Sharpe | `(Rendement - Rf) / Volatilité` |
| Ratio de Sortino | `(Rendement - Rf) / Volatilité négative` |
| Ratio Calmar | `Rendement / |Max Drawdown|` |
| Tracking Error | `Écart-type(ri - rMASI) × √252` |

> Taux sans risque utilisé : **3.5%** (Bons du Trésor marocain 52 semaines)

---

##  Structure du projet
```
bourse-casablanca-analytics/
│
├── DATA_BULLETINS_WITH_TYPE/    # Fichiers Markdown par catégorie
│   ├── Indices/
│   ├── Actions/
│   ├── Droits/
│   ├── Obligations/
│   └── Physionomie/
│
├── base/                        # CSV finaux nettoyés
│   ├── Indices_FINAL.csv
│   ├── Actions_FINAL.csv
│   ├── Droits_FINAL.csv
│   ├── Obligations_FINAL.csv
│   └── Physionomie_FINAL.csv
│
├── les nootebooks/             # Notebooks Jupyter
│   ├── automatisation.ipynb     # Téléchargement PDFs
│   ├── markdown.ipynb           # Extraction OCR
│   ├── conversion_csv.ipynb      # Conversion et fusion CSV
│   ├──API.ipynb
│   ├── les EDA
│        
│                      
│   └── KPIs_Societes.ipynb      # Calcul des KPIs
│
├── remplissage/                 # Scripts nettoyage
│   ├── indices.ipynb
│   ├── actions.ipynb
│   ├── droits.ipynb
│   ├── obligations.ipynb
│   └── physionomie.ipynb
│
├── scripts/
│   ├── load_to_postgresql.py    # Chargement PostgreSQL
│   ├── ajout_date_seance.py     # Ajout colonne Date_Seance
│   ├── calcul_kpis.py           # Calcul KPIs Python
│   ├── kpis_sql.sql             # Vues SQL KPIs
│   └── temps_reel.py            # Données temps réel Yahoo Finance
│
├──DOCUMENTATION_TECHNIQUE_Confluence
├── KPIs_Societes.ipynb
├── README.md
└── 
```

---

##  Installation

### Prérequis
- Python 3.10+
- PostgreSQL 18.1
- Power BI Desktop
- JupyterLab

### Dépendances Python
```bash
pip install pandas numpy sqlalchemy psycopg2-binary yfinance requests jupyter
```

### Configuration PostgreSQL
```bash
# Créer la base de données dans pgAdmin
CREATE DATABASE bourse_casablanca;

# Charger les données
python scripts/load_to_postgresql.py
```

### Lancement
```bash
# 1. Télécharger les PDFs
jupyter nbconvert --to notebook --execute "les nootebooks/automatisation.ipynb"

# 2. Extraire les données OCR
jupyter nbconvert --to notebook --execute "les nootebooks/markdown.ipynb"

# 3. Convertir en CSV
jupyter nbconvert --to notebook --execute "les nootebooks/conversion_csv.ipynb"

# 4. Nettoyer les données
python remplissage/nulls_actions.py
python remplissage/nulls_indices.py
python remplissage/nulls_droits.py
python remplissage/nulls_obligations.py
python remplissage/nulls_physionomie.py

# 5. Charger dans PostgreSQL
python scripts/load_to_postgresql.py

# 6. Calculer les KPIs
jupyter nbconvert --to notebook --execute "les nootebooks/KPIs_Societes.ipynb"
```

---

##  Dashboard Power BI

Le dashboard est organisé en **5 pages** :

| Page | Titre | KPIs |
|------|-------|------|
| 1 | Vue Globale du Marché | Valeur MASI, Tendance, Volatilité |
| 2 | Performance des Sociétés | Sharpe, Rendement, Scatter R/R |
| 3 | Analyse du Risque | Max Drawdown, VaR 95%, Bêta |
| 4 | Analyse Sectorielle | Treemap, Volatilité sectorielle |
| 5 | Liquidité & Transactions | Volume, Transactions, ADV |

---

##  Résultats clés

### Top 5 sociétés (Ratio de Sharpe)

| Société | Rendement | Volatilité | Sharpe |
|---------|-----------|------------|--------|
| SGTM S.A | 539% | 92.6% | 5.78 |
| TIMAR | 95.7% | 25.5% | 3.61 |
| CASH PLUS S.A | 273.9% | 100.6% | 2.69 |
| JET CONTRACTORS | 106.8% | 41.3% | 2.50 |
| AUTO NEJMA | 89.0% | 37.8% | 2.26 |

### MASI — Marché global
- **Tendance** : BULLISH (56% séances positives)
- **Gain max journalier** : +5.08%
- **Perte max journalière** : -5.64%
- **Volatilité journalière** : 0.78%

### Top secteur : MINES (+42.79% rendement annuel moyen)

---

##  Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.10+ |
| OCR | Mistral AI (mistral-ocr-latest) |
| Data manipulation | Pandas, NumPy |
| Base de données | PostgreSQL 18.1 |
| ORM | SQLAlchemy + psycopg2 |
| Finance data | yfinance |
| Notebooks | JupyterLab |
| Visualisation | Power BI Desktop |
| Versionnage | GitHub |

---

##  Licence

Ce projet est réalisé dans le cadre d'un **projet de fin de formation Data Analyst**.

---

*BourseInsight — Analyse & Performance du Marché Marocain*
