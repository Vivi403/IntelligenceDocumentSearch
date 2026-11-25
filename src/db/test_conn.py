from src.generation.rag import rag_answer
from src.embedder import load_model
from src.db.qdrant_store import get_qdrant_client

model = load_model()
client = get_qdrant_client()

question = "Что такое Python?"

answer = rag_answer(question, model, client)

print(answer)
