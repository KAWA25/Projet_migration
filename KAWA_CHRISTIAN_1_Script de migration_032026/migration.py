# Definition des bibiothèques
import pandas as pd
from pymongo import MongoClient

def migrate_csv_to_mongo(csv_path, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
    try:
        # 1. Chargement des données avec Pandas
        print(f"--- Lecture du fichier {csv_path} ---")
        df = pd.read_csv(csv_path)

        # 2. Nettoyage / Transformation (Optionnel)
        # Exemple : Remplacer les valeurs vides (NaN) par None pour MongoDB
        df = df.where(pd.notnull(df), None)

        # 3. Connexion à MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # 4. Conversion du DataFrame en liste de dictionnaires (format JSON/BSON)
        data_dict = df.to_dict(orient='records')

        # 5. Insertion massive (Bulk Write)
        print(f"--- Insertion de {len(data_dict)} documents dans {collection_name} ---")
        result = collection.insert_many(data_dict)
        
        print(f"Migration réussie ! ID du premier document : {result.inserted_ids[0]}")

    except Exception as e:
        print(f"Erreur lors de la migration : {e}")
    finally:
        client.close()

# --- Paramètres à modifier ---
CSV_FILE = 'healthcare_dataset.csv'
DATABASE = 'local'
COLLECTION = 'Medical-data'
# Pour Atlas, remplacez par votre URI : "mongodb+srv://user:pass@cluster.mongodb.net/"
URI = "mongodb://localhost:27017/"
URI = "mongodb://host.docker.internal:27017"

migrate_csv_to_mongo(CSV_FILE, DATABASE, COLLECTION, URI)