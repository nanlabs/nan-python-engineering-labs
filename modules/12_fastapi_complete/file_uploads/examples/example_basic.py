"""
Basic example: File Uploads
=============================

FastAPI handles file uploads through UploadFile, which gives you
async access to the file content, metadata, and the underlying stream.

This example demonstrates:
1. Single file upload with type validation
2. Multiple file uploads
3. File size limit enforcement
4. Saving files to disk
5. Returning file metadata in the response

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

Test upload with curl:
    curl -X POST "http://localhost:8000/upload" \
         -F "file=@/path/to/yourfile.jpg"
"""

import hashlib
import mimetypes
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from pydantic import BaseModel

# =============================================================================
# CONFIG
# =============================================================================

UPLOAD_DIR = Path("/tmp/fastapi_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_DOCUMENT_TYPES = {"application/pdf", "text/plain", "text/csv"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


# =============================================================================
# MODELS
# =============================================================================


class FileMetadata(BaseModel):
    """Metadata returned after a successful upload."""

    filename: str
    original_name: str
    content_type: str
    size_bytes: int
    size_human: str
    sha256: str
    saved_path: str


class UploadSummary(BaseModel):
    """Summary for a multi-file upload."""

    uploaded: int
    failed: int
    files: list[FileMetadata]
    errors: list[str]


# =============================================================================
# HELPERS
# =============================================================================


def human_size(bytes_: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


async def read_and_validate(
    file: UploadFile,
    allowed_types: set[str],
    max_size: int = MAX_FILE_SIZE_BYTES,
) -> bytes:
    """Read file contents, validate MIME type and size."""
    content_type = file.content_type or mimetypes.guess_type(file.filename or "")[0] or ""
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {content_type}. Allowed: {sorted(allowed_types)}",
        )
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large: {human_size(len(contents))}. Max: {human_size(max_size)}",
        )
    return contents


def save_and_hash(contents: bytes, filename: str) -> tuple[str, str]:
    """Save file contents to disk and return (saved_path, sha256)."""
    sha = hashlib.sha256(contents).hexdigest()
    safe_name = f"{sha[:8]}_{Path(filename).name}"
    dest = UPLOAD_DIR / safe_name
    dest.write_bytes(contents)
    return str(dest), sha


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="File Uploads Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "File Uploads Demo", "docs": "/docs"}


@app.post("/upload/image", response_model=FileMetadata, status_code=201)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload a single image file (JPEG, PNG, GIF, WebP).

    - Validates MIME type against the allowed image types.
    - Rejects files larger than 5 MB.
    - Returns file metadata including SHA-256 hash.
    """
    contents = await read_and_validate(file, ALLOWED_IMAGE_TYPES)
    saved_path, sha = save_and_hash(contents, file.filename or "upload")
    return FileMetadata(
        filename=Path(saved_path).name,
        original_name=file.filename or "unknown",
        content_type=file.content_type or "",
        size_bytes=len(contents),
        size_human=human_size(len(contents)),
        sha256=sha,
        saved_path=saved_path,
    )


@app.post("/upload/document", response_model=FileMetadata, status_code=201)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, TXT, CSV).

    Same validation logic as image upload but with document MIME types.
    """
    contents = await read_and_validate(file, ALLOWED_DOCUMENT_TYPES)
    saved_path, sha = save_and_hash(contents, file.filename or "doc")
    return FileMetadata(
        filename=Path(saved_path).name,
        original_name=file.filename or "unknown",
        content_type=file.content_type or "",
        size_bytes=len(contents),
        size_human=human_size(len(contents)),
        sha256=sha,
        saved_path=saved_path,
    )


@app.post("/upload/multiple", response_model=UploadSummary, status_code=201)
async def upload_multiple(files: list[UploadFile] = File(...)):
    """
    Upload up to 10 files at once (images or documents).

    Files that fail validation are reported in `errors` without aborting
    the entire batch — successfully uploaded files are still saved.
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per request")

    allowed = ALLOWED_IMAGE_TYPES | ALLOWED_DOCUMENT_TYPES
    uploaded: list[FileMetadata] = []
    errors: list[str] = []

    for f in files:
        try:
            contents = await read_and_validate(f, allowed)
            saved_path, sha = save_and_hash(contents, f.filename or "file")
            uploaded.append(
                FileMetadata(
                    filename=Path(saved_path).name,
                    original_name=f.filename or "unknown",
                    content_type=f.content_type or "",
                    size_bytes=len(contents),
                    size_human=human_size(len(contents)),
                    sha256=sha,
                    saved_path=saved_path,
                )
            )
        except HTTPException as e:
            errors.append(f"{f.filename}: {e.detail}")

    return UploadSummary(
        uploaded=len(uploaded),
        failed=len(errors),
        files=uploaded,
        errors=errors,
    )


@app.get("/uploads")
async def list_uploads():
    """List files currently saved in the upload directory."""
    files = [
        {"name": f.name, "size": human_size(f.stat().st_size)}
        for f in UPLOAD_DIR.iterdir()
        if f.is_file()
    ]
    return {"upload_dir": str(UPLOAD_DIR), "count": len(files), "files": files}


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 60)
    print("FILE UPLOADS — DEMO")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST /upload/image    — single image (JPEG/PNG/GIF/WebP)")
    print("  POST /upload/document — single doc (PDF/TXT/CSV)")
    print("  POST /upload/multiple — up to 10 files (mixed types)")
    print("  GET  /uploads         — list saved files")
    print()
    print("Test with curl:")
    print('  curl -X POST "http://localhost:8000/upload/image"')
    print('       -F "file=@/path/to/image.jpg"')
    print()
    print("Upload dir:", UPLOAD_DIR)
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    demo()
