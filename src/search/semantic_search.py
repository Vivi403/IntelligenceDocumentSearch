from src.embedder import create_embeddings
from src.db.qdrant_store import get_qdrant_client, search_vectors
from src.db.repositories import get_chunks_by_ids
from src.embedder import load_model
from src.settings import SEARCH_LIMIT


def semantic_search(user_input, model, client):

    embed_input = create_embeddings([user_input], model)
    query_vector = embed_input[0]

    result_ids = search_vectors(client, query_vector, SEARCH_LIMIT)
    chunk_ids = [point.id for point in result_ids.points]
    scores = [point.score for point in result_ids.points]

    result_chunks = get_chunks_by_ids(chunk_ids)
    chunks_by_id = {row[0]: row for row in result_chunks}

    ordered_chunks = [
        chunks_by_id[chunk_id] for chunk_id in chunk_ids if chunk_id in chunks_by_id
    ]

    return [
        {
            "chunk_id": chunk[0],
            "document_id": chunk[1],
            "content": chunk[2],
            "score": score,
        }
        for chunk, score in zip(ordered_chunks, scores)
    ]
