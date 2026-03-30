import pandas as pd
from sqlalchemy import create_engine
import time
import os
import urllib.parse

# CONFIGURATION - CHEMIN EXACT WINDOWS
HOST     = "127.0.0.1"
PORT     = 5432
DATABASE = "bourse_casablanca"
USER     = "postgres"
PASSWORD = "Hiba41hh07@"  

# Encodage du MDP pour le caractère '@'
SAFE_PASSWORD = urllib.parse.quote_plus(PASSWORD)

CHEMIN = r"D:\rouge_file\Analyse_du_performance_de_la_bourse_casablanca\base"

# MAPPING CSV -> TABLE
TABLES_MAPPING = {
    "Actions_FINAL.csv"     : "actions",
    "Droits_FINAL.csv"      : "droits",
    "Indices_FINAL.csv"     : "indices",
    "Obligations_FINAL.csv" : "obligations",
    "Physionomie_FINAL.csv" : "physionomie",
}

# CONNEXION POSTGRESQL
conn_url = f'postgresql+psycopg2://{USER}:{SAFE_PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(conn_url, connect_args={'host': '127.0.0.1'})

print("--- Tentative de connexion à PostgreSQL ---")
try:
    with engine.connect() as conn:
        print(" Connexion réussie !\n")
except Exception as e:
    print(f" Erreur de connexion : {e}")
    exit()

# CHARGEMENT DES DONNÉES
for fichier, table_name in TABLES_MAPPING.items():
    # Utilisation de os.path.join pour construire le chemin proprement
    chemin_complet = os.path.join(CHEMIN, fichier)
    
    print(f" Vérification : {fichier}...")
    
    if os.path.exists(chemin_complet):
        print(f" Chargement en cours vers la table [{table_name}]...")
        debut = time.time()
        try:
            # Lecture (on essaie utf-8, si ça rate on passe en latin-1)
            try:
                df = pd.read_csv(chemin_complet, low_memory=False, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(chemin_complet, low_memory=False, encoding='latin-1')

            # Nettoyage des colonnes (minuscules, pas d'espaces)
            df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
            
            # Insertion dans la base
            df.to_sql(
                name      = table_name,
                con       = engine,
                if_exists = 'replace',
                index     = False,
                chunksize = 5000,
                method    = 'multi'
            )

            duree = round(time.time() - debut, 2)
            print(f"    Terminé : {len(df):,} lignes insérées en {duree}s\n")

        except Exception as e:
            print(f"    Erreur technique sur ce fichier : {e}\n")
    else:
        print(f"   Introuvable ! Vérifie l'orthographe exacte du fichier.\n")

print(" PROCESSUS DE CHARGEMENT FINI")
