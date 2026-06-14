from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from app.config import GENERATED_DIR
import os

router = APIRouter()


class FileInfo(BaseModel):
    filename: str
    size: int


def _safe_path(filename: str):
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid file name")
    path = GENERATED_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return path


def _list_files():
    """List generated files from GENERATED_DIR, newest first."""
    if not GENERATED_DIR.exists():
        return []
    files = [
        f for f in GENERATED_DIR.iterdir()
        if f.is_file() and not f.name.startswith('.')
    ]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return [FileInfo(filename=f.name, size=f.stat().st_size) for f in files]


@router.get("", response_model=list[FileInfo])
@router.get("/", response_model=list[FileInfo], include_in_schema=False)
def list_files():
    return _list_files()


@router.get("/{filename}")
def download_file(filename: str):
    path = _safe_path(filename)
    media_types = {
        "pdf": "application/pdf",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "md": "text/markdown",
        "txt": "text/plain",
    }
    ext = path.suffix.lstrip('.')
    media_type = media_types.get(ext, 'application/octet-stream')
    return FileResponse(path=str(path), filename=filename, media_type=media_type)


@router.delete("/{filename}", status_code=204)
def delete_file(filename: str):
    path = _safe_path(filename)
    path.unlink()
