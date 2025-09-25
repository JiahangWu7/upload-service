from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import os
from datetime import datetime

# ----------------------------
# Basic config (no processing)
# ----------------------------

# Allowlists: keep image endpoint "images only"; file endpoint "docs only".
ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_FILE_EXTS  = {".txt", ".pdf", ".docx", ".xlsx"}

# Size limit (MB) - adjustable via env var MAX_MB; default 20MB
MAX_MB = int(os.getenv("MAX_MB", "20"))
MAX_BYTES = MAX_MB * 1024 * 1024

# Storage directories
STORAGE = Path("storage")
IMAGE_DIR = STORAGE / "images"
FILE_DIR  = STORAGE / "files"
for d in (IMAGE_DIR, FILE_DIR):
    d.mkdir(parents=True, exist_ok=True)

def gen_id() -> str:
    """Generate a short random id for saved files."""
    return uuid.uuid4().hex[:12]

def save_file(content: bytes, target_dir: Path, uid: str, ext: str) -> Path:
    """Persist file bytes to storage and return the path."""
    target_dir.mkdir(parents=True, exist_ok=True)
    p = target_dir / f"{uid}{ext}"
    p.write_bytes(content)
    return p

# ----------------------------
# FastAPI app
# ----------------------------

app = FastAPI(
    title="File & Photo Upload Service",
    version="0.1.0",
    description="Minimal service that ONLY uploads files/images. No processing."
)

# CORS: open for dev; tighten origins in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    """Simple healthcheck to verify the service is alive."""
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
        "limits": {"max_mb": MAX_MB},
        "image_types": sorted(ALLOWED_IMAGE_EXTS),
        "file_types": sorted(ALLOWED_FILE_EXTS)
    }

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """
    Accept image files only. Save to storage/images.
    Returns metadata so the main backend can store and reference it.
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported image type: {ext}. Allowed: {sorted(ALLOWED_IMAGE_EXTS)}"
        )

    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large (> {MAX_MB} MB)"
        )

    uid = gen_id()
    stored_path = save_file(content, IMAGE_DIR, uid, ext)

    return {
        "id": uid,
        "kind": "image",
        "filename": file.filename,
        "stored_path": str(stored_path),   # internal path; do NOT expose directly to the public web
        "size_bytes": len(content),
        "mime_type": file.content_type,
        "message": "uploaded"
    }

@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept common document types (txt/pdf/docx/xlsx). Save to storage/files.
    No text extraction here (processing will be added later).
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_FILE_EXTS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {ext}. Allowed: {sorted(ALLOWED_FILE_EXTS)}"
        )

    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large (> {MAX_MB} MB)"
        )

    uid = gen_id()
    stored_path = save_file(content, FILE_DIR, uid, ext)

    return {
        "id": uid,
        "kind": "file",
        "filename": file.filename,
        "stored_path": str(stored_path),   # internal path; main backend should manage access
        "size_bytes": len(content),
        "mime_type": file.content_type,
        "message": "uploaded"
    }
