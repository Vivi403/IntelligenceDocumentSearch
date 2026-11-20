from src.search.semantic_search import semantic_search
from src.db.repositories import fulltext_search
from src.settings import SEARCH_LIMIT
from src.db.repositories import get_chunks_by_ids

HYBRID_LIMIT = 6
RRF_K = 60


def hybrid_search(user_input, model, client):

    if not user_input or not user_input.strip():
        return []

    semantic = semantic_search(user_input, model, client)
    fulltext = fulltext_search(user_input, SEARCH_LIMIT)

    rrf_scores = {}

    for rank, res in enumerate(semantic, start=1):
        chunk_id = res["chunk_id"]

        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (RRF_K + rank)

    for rank, res in enumerate(fulltext, start=1):
        chunk_id = res[0]

        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (RRF_K + rank)

    sort_scores = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[
        :HYBRID_LIMIT
    ]

    chunk_ids = [item[0] for item in sort_scores]

    content = get_chunks_by_ids(chunk_ids)

    chunks_by_id = {row[0]: row for row in content}
    return [
        {
            "chunk_id": chunk_id,
            "document_id": chunks_by_id[chunk_id][1],
            "content": chunks_by_id[chunk_id][2],
            "rrf_score": score,
        }
        for chunk_id, score in sort_scores
        if chunk_id in chunks_by_id
    ]
