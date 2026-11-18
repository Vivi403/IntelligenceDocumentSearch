from src.db.qdrant_store import get_qdrant_client, create_collection

cl = get_qdrant_client()

# create_collection(cl)

# print(cl.get_collections())

print(cl.get_collection("document_chunks").points_count)
