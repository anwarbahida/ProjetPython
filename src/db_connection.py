import psycopg2
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_connection():
    """Retourne une connexion à la base de données PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except psycopg2.DatabaseError as error:
        print(f"Erreur lors de la connexion à la base de données : {error}")
        return None
