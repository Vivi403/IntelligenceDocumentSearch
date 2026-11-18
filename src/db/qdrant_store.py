from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384


def get_qdrant_client():

    client = QdrantClient(url="http://localhost:6333")
    return client


def create_collection(client):
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
