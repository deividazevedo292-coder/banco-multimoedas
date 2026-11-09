import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def conectar():
    # No servidor (Render), o endereço do banco (Neon) vem pronto numa variável só
    url = os.getenv("DATABASE_URL")
    if url:
        return psycopg2.connect(url, sslmode="require")

    # No seu computador, continua usando o .env de sempre
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )