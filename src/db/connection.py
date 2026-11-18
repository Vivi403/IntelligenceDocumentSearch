import psycopg
from src.settings import DATABASE_URL


def get_connection():
    conn = psycopg.connect(DATABASE_URL)

    return conn
