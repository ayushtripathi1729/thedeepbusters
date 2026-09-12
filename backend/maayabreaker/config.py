from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[1] / "data"))
    database_path: Path = Path(os.getenv("DATABASE_PATH", Path(__file__).resolve().parents[1] / "data" / "maayabreaker.db"))
    storage_dir: Path = Path(os.getenv("STORAGE_DIR", Path(__file__).resolve().parents[1] / "data" / "media"))
    max_image_bytes: int = int(os.getenv("MAX_IMAGE_BYTES", 25 * 1024 * 1024))
    max_media_bytes: int = int(os.getenv("MAX_MEDIA_BYTES", 250 * 1024 * 1024))
    retention_hours: int = int(os.getenv("RETENTION_HOURS", "24"))
    eager_jobs: bool = os.getenv("EAGER_JOBS", "0") == "1"
    production_model: str = os.getenv("PRODUCTION_MODEL", "")
settings = Settings()
