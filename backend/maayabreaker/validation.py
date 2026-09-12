from pathlib import Path
from PIL import Image, UnidentifiedImageError

IMAGE_SIGNATURES = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a", b"BM", b"RIFF")
def detect_type(path: Path, name: str):
    head = path.read_bytes()[:32]; lower = name.lower()
    if head.startswith(IMAGE_SIGNATURES) and not (head.startswith(b"RIFF") and lower.endswith((".wav", ".avi"))): return "image"
    if head[4:8] == b"ftyp" or head.startswith(b"\x1aE\xdf\xa3"): return "video"
    if head.startswith((b"ID3", b"fLaC", b"OggS", b"RIFF")) or lower.endswith((".wav", ".mp3", ".flac", ".ogg", ".m4a")): return "audio"
    return None
def validate_image(path: Path, max_bytes: int):
    if path.stat().st_size > max_bytes: raise ValueError("image_too_large")
    try:
        with Image.open(path) as image: image.verify()
        with Image.open(path) as image: return {"format": image.format, "dimensions": {"width": image.width,"height": image.height}, "metadata_present": bool(image.getexif())}
    except (UnidentifiedImageError, OSError): raise ValueError("unsafe_or_invalid_image")
