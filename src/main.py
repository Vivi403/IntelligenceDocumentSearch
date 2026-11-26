from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.embedder import load_model
from src.db.qdrant_store import get_qdrant_client
from src.api.routes import router

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.model = load_model()
    app.state.client = get_qdrant_client()

    yield

    app.state.client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/style.css")
def frontend_styles():
    return FileResponse(FRONTEND_DIR / "style.css", media_type="text/css")


@app.get("/app.js")
def frontend_script():
    return FileResponse(FRONTEND_DIR / "app.js", media_type="text/javascript")
