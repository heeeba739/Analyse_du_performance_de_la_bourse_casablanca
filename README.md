# Analyse_du_performance_de_la_bourse_casablanca
#  BourseInsight Analytics : Analyse de la Bourse de Casablanca 🇲🇦

##  Présentation du Projet
Ce projet, réalisé dans le cadre de ma formation chez **Simplon**, vise à automatiser la collecte, le traitement et la visualisation des données boursières de la **Bourse de Casablanca (MASI)**. 

L'objectif est de fournir une aide à la décision via des indicateurs de performance et de risque précis, extraits de plus de 20 000 lignes de données historiques.

---

##  Stack Technique
* **Ingestion de données :** Python (Pandas, SQLAlchemy,numpy,OCR)
* **Stockage :** PostgreSQL (Gestion de 20 804 lignes d'indices)
* **Nettoyage :** SQL (Window Functions pour la reconstruction chronologique)
* **Visualisation :** Power BI (Modèle en étoile)

---

---

##  Gestion du Risque
Le risque est monitoré à travers plusieurs métriques :
* **Volatilité des Indices :** Mesure de l'écart-type des rendements.
* **Drawdown :** Analyse des périodes de baisse maximale.


---

##  Analyse & Storytelling
Le projet ne se contente pas d'afficher des chiffres, il raconte une histoire :
1. **Extraction :** Automatisation de la lecture des bulletins de côte (PDF/CSV).
2. **Traitement :** Normalisation des données et injection dans un entrepôt PostgreSQL.
3. **Insight :** Création de tableaux de bord interactifs pour comparer les performances du **MASI 20** vs les **Small Caps**.

---

##  Structure du Repo
* `les nootebooks` : contient tous les scripts concernant telechargement,extractions et nettoyage des donneés 
* `remplissage` : Notebooks des EDA de chaque csv 
* `KPIs_Societes.csv` : csv des kpis calculees dans vs_code avec code python
* `Kpis_Societes.ipynb` : script de calcul des kpis 
* `bourse_casablanca.pbix`: la visualisation des kpis calculees 
*`load_to_postgresql.py`: script pour connecter vs_code avec postgresql
---

##  Auteur
**Hiba** - Apprenante Data @Simplon
