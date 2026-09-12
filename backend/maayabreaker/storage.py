import hashlib, os, uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from werkzeug.utils import secure_filename
from .config import settings

def save_upload(stream, original_name):
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    name = secure_filename(original_name) or "upload"
    key = str(uuid.uuid4()); target = settings.storage_dir / key
    digest = hashlib.sha256(); size = 0
    with target.open("xb") as output:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > settings.max_media_bytes: output.close(); target.unlink(missing_ok=True); raise ValueError("upload_too_large")
            digest.update(chunk); output.write(chunk)
    return key, name, digest.hexdigest(), size
def path_for(key): return settings.storage_dir / key
def expiration(): return (datetime.now(timezone.utc) + timedelta(hours=settings.retention_hours)).isoformat()
