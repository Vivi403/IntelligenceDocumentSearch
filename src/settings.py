# Загружает настройки и переменные окружения
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("URL базы данных не может быть пустым")


EMBEDDING_MODEL = os.environ.get(
    "EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2"
)

SEARCH_LIMIT = int(os.environ.get("SEARCH_LIMIT", 10))

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ

CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 150))

if CHUNK_SIZE <= 0:
    raise ValueError("Размер чанка не может быть меньше нуля")

if CHUNK_OVERLAP < 0:
    raise ValueError("Размер перекрытия не может быть меньше нуля")

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("Размер перекрытия не может быть больше размера чанка")
