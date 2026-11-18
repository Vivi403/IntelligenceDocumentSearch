from src.search.hybrid_search import hybrid_search
from src.embedder import load_model
from src.db.qdrant_store import get_qdrant_client

model = load_model()
client = get_qdrant_client()

results = hybrid_search("Как работают классы в Python?", model, client)

for result in results:
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Score: {result['rrf_score']:.5f}")
    print(f"Text: {result['content']}")
    print("-" * 60)
