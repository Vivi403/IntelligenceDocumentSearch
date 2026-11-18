from sentence_transformers import SentenceTransformer
from src.settings import EMBEDDING_MODEL


def load_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def create_embeddings(texts, model) -> list[list[float]]:

    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    return embeddings.tolist()
