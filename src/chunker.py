from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.settings import CHUNK_SIZE, CHUNK_OVERLAP


def split_into_chunks(text) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
    )

    chunks = splitter.split_text(text)
    return [chunk for chunk in chunks if chunk.strip()]
