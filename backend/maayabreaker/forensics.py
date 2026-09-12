from pathlib import Path
from .validation import validate_image
from .config import settings
def inspect(path: Path, media_type: str):
    if media_type == "image": return validate_image(path, settings.max_image_bytes)
    return {"container_validation": "passed", "byte_size": path.stat().st_size}
