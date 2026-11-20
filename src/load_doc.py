from src.pipeline import process_file
from pathlib import Path
from src.settings import RAW_DIR
from src.embedder import load_model
from src.db.qdrant_store import get_qdrant_client


dir_path = Path(RAW_DIR)
ext = {".txt", ".pdf", ".docx"}
files = [p for p in dir_path.iterdir() if p.suffix.lower() in ext]

model = load_model()
client = get_qdrant_client()

for file in files:

    try:
        process_file(file, model, client)

    except Exception as e:
        print(f"Ошибка при обработке {file.name}: {e}")
        continue
