# Projet_migration
Migrez des données médicales à l'aide du NoSQL via Docker




## 1-	Contexte 

Le client est confronté à des problèmes de scalabilité sur la gestion quotidienne de ses données.
L’objectif est de proposer une solution Big Data scalable horizontalement basée sur MongoDB
Taches : 
-	Migration des données via Docker
-	Documentation Github
-	Etude de déploiement AWS

## 2- Analyse du dataset pour justifier l’utilisation de MongoDB

Le CSV contient des informations des patients mêlant :
- Environ 55 500 lignes de données
- 15 colonnes
- Données des patients, hospitalisation, facturation et tests
- Identité : Name, Age, Gender
- Hospitalisation : Hospital, Insurance provider, Room Nimber, Admission type, médication, discharge date, medication
- Données médicales : Blood Type, Médical condition, Date of admission Doctor
- Facturation : Billing amount,
- Résultats : Test results
Données flexible, semi-structurées, susceptibles d’évoluer (nouveaux champs médicaux, nouveaux tests, etc.)

## 3- Démarche Technique

## 4- Conception du Schéma MongoDB

## 5- Script de migration automatisé

De base il faut installer pandas à l’aide de la commande 
  - Pip install pymogo pandas


Script de migration 
- Nom : migration.py
- DATABASE : local
- COLLECTION : Medical-data
- CSV_FILE : 'healthcare_dataset.csv'

       # 1. Definition des bibiothèques
       import pandas as pd
       from pymongo import MongoClient

       def migrate_csv_to_mongo(csv_path, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
        try:
        # 2. Chargement des données avec Pandas
        print(f"--- Lecture du fichier {csv_path} ---")
        df = pd.read_csv(csv_path)

        # 3. Nettoyage / Transformation (Optionnel)
        # Exemple : Remplacer les valeurs vides (NaN) par None pour MongoDB
        df = df.where(pd.notnull(df), None)

        # 4. Connexion à MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # 5. Conversion du DataFrame en liste de dictionnaires (format JSON/BSON)
        data_dict = df.to_dict(orient='records')

        # 6. Insertion massive (Bulk Write)
        print(f"--- Insertion de {len(data_dict)} documents dans {collection_name} ---")
        result = collection.insert_many(data_dict)
        
        print(f"Migration réussie ! ID du premier document : {result.inserted_ids[0]}")

        except Exception as e:
        print(f"Erreur lors de la migration : {e}")
        finally:
        client.close()
  
        # 7. Paramètres à modifier
        CSV_FILE = 'healthcare_dataset.csv'
        DATABASE = 'local'
        COLLECTION = 'Medical-data'
  
        # 8. Pour Atlas, remplacez par votre URI : "mongodb+srv://user:pass@cluster.mongodb.net/"
          URI = "mongodb://localhost:27017/"

          migrate_csv_to_mongo(CSV_FILE, DATABASE, COLLECTION, URI)


Conteneurisation avec Docker

Nom : docker-compose.yml

    version: '3.8'
      services:
        mongodb:
          image: mongo:7
          container_name: medical_mongodb
          restart: always
          ports:
            - "27017:27017"
          volumes:
            - ./data/db:/data/db
          environment:
            MONGO_INITDB_ROOT_USERNAME: root
            MONGO_INITDB_ROOT_PASSWORD: example
      


## 6- Pourquoi MongoDB

-	Base NoSQL adaptée aux données semi structurées orientée documents (JSON/BSON)
-	Adaptée aux données médicales évolutives
-	Scalabilité horizontale via sharding
-	Haute performance en lecture/écriture
-	Docker pour la portabilité


## 7- Schéma de base 

## 8- Scalabilité 

-	MongoDB supporte le sharding
-	Docker facilite la réplication et le déploiement

## 9- Sécurité et Authentification

-	Utilisateur admin
-	Rôles data_reader et data_writer
-	Authentification via MONGO_URI

## 10- Commande de lancement

- Python migration.py (migration est le nom du script)

## 11- Projet AWS

  ##### Amazon S3 pour le stockage des backups
-	Sauvegarde des dumps Mongo (mongodump)
-	Stockage peu couteux
-	versionning
  
  ##### Amazon ECS pour exécuter les conteneurs Docker
-	Lance les conteneurs docker
-	Scalabilité horizontale
-	Orchestration simple
  
##### Amazon DocumentDB compatible MongoDB
-	Service managé compatible MongoDB
-	Pas de gestion de serveur
-	Haute dispo native
  
##### RDS non adapté car orienté SQL





