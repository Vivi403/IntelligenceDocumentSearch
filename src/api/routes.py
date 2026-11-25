from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pathlib import Path
from uuid import uuid4

from src.settings import RAW_DIR
from src.pipeline import process_file
from src.db.repositories import get_all_documents

from qdrant_client.models import Filter, FieldCondition, MatchValue, FilterSelector
from src.db.repositories import get_document_by_id, delete_document

from src.db.qdrant_store import COLLECTION_NAME

from src.generation.rag import rag_answer
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024


@router.post("/ask")
def ask_question(user_question: QuestionRequest, request: Request):

    model = request.app.state.model
    client = request.app.state.client

    return {
        "question": user_question.question,
        "answer": rag_answer(user_question.question, model, client),
    }


@router.post("/documents")
async def load_document(request: Request, file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()

    if ext not in {".txt", ".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    filename = f"{uuid4().hex}{ext}"
    file_path = RAW_DIR / filename
    total_size = 0

    try:
        with file_path.open("wb") as buffer:
            while True:
                content = await file.read(CHUNK_SIZE)

                if not content:
                    break

                total_size += len(content)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413, detail="Размер файла превышает 10 МБ"
                    )

                buffer.write(content)

        model = request.app.state.model
        client = request.app.state.client

        result = process_file(file_path, model, client)

        return {
            "message": "Документ успешно обработан",
            "document_id": result["document_id"],
            "filename": filename,
            "chunks_count": len(result["chunks"]),
        }

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    finally:
        await file.close()


@router.get("/documents")
def get_documents():
    documents = get_all_documents()

    return {"count": len(documents), "documents": documents}


@router.delete("/documents/{document_id}")
def remove_document(document_id: int, request: Request):

    document = get_document_by_id(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")

    file_path = Path(document["storage_path"]).resolve()

    try:
        file_path.relative_to(RAW_DIR.resolve())

    except ValueError:
        raise HTTPException(
            status_code=500, detail="Некорректный путь к файлу документа"
        )

    client = request.app.state.client

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id", match=MatchValue(value=document_id)
                    )
                ]
            )
        ),
        wait=True,
    )

    delete_document(document_id)

    file_path.unlink(missing_ok=True)

    return {"message": "Документ успешно удалён", "document_id": document_id}
