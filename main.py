import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.seed import seed_database
from app.migrate import migrate_db, sync_ad_targeting, sync_sample_comments
from app.routers import auth, complaints, interactions, brands, search_ai, admin

app = FastAPI(title="Panchaayat", description="Consumer Voice & Resolution Platform", version="1.0.0")

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

STATIC_DIR = Path(__file__).parent / "static" / "dist"
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    migrate_db()
    seed_database()
    sync_ad_targeting()
    sync_sample_comments()


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Panchaayat"}


if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
