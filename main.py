import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.seed import seed_database
from app.migrate import migrate_db, sync_ad_targeting, sync_sample_comments
from app.routers import auth, complaints, interactions, brands, search_ai, admin, social

logger = logging.getLogger(__name__)


def _init_app_data() -> None:
    settings = get_settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    migrate_db()
    seed_database()
    sync_ad_targeting()
    sync_sample_comments()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        _init_app_data()
    except Exception:
        logger.exception("Startup initialization failed")
    yield


app = FastAPI(
    title="Panchaayat",
    description="Consumer Voice & Resolution Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(interactions.router)
app.include_router(brands.router)
app.include_router(search_ai.router)
app.include_router(admin.router)
app.include_router(social.router)

settings = get_settings()
STATIC_DIR = settings.static_dir
UPLOAD_DIR = settings.upload_dir


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": "Panchaayat",
        "vercel": settings.is_vercel,
        "static": STATIC_DIR.exists(),
    }


if STATIC_DIR.exists():
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    if UPLOAD_DIR.exists():
        app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        index = STATIC_DIR / "index.html"
        if index.is_file():
            return FileResponse(index)
        return {"error": "Frontend not built. Run: cd frontend && npm run build"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
