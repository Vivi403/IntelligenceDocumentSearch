from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

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


def save_vectors(client, document_id, chunk_ids, embeddings):

    if len(chunk_ids) != len(embeddings):
        raise ValueError("Чанков и векторов должно быть одинаковое количество")

    points = []

    for chunk, embed in zip(chunk_ids, embeddings):
        point = PointStruct(
            id=chunk,
            vector=embed,
            payload={"document_id": document_id, "chunk_id": chunk},
        )

        points.append(point)

    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search_vectors(client, query_vector, limit):

    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )
