from src.extractor import extract_file
from src.cleaner import clean_text
from src.chunker import split_into_chunks
from src.embedder import create_embeddings
from src.db.repositories import save_document, save_chunks
from pathlib import Path


def process_file(file_path, model) -> dict:

    document = extract_file(file_path)
    clean_doc = clean_text(document.text)
    chunks = split_into_chunks(clean_doc)
    embeddings = create_embeddings(chunks, model)

    doc_id = save_document(Path(file_path).name, document.file_type, document.source)
    save_chunks(doc_id, chunks, embeddings)

    return {
        "document_id": doc_id,
        "document": document,
        "chunks": chunks,
        "embeddings": embeddings,
    }


# model = load_model()
# result = process_file("oop-ru.pdf", model)
# print(result)
