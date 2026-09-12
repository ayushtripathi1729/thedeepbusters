import json, sqlite3
from datetime import datetime, timezone
from .config import settings

def now(): return datetime.now(timezone.utc).isoformat()
def connect():
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.database_path); conn.row_factory = sqlite3.Row; conn.execute("PRAGMA foreign_keys = ON"); return conn
def init():
    with connect() as db:
        # Early versions used an incompatible analyses schema. Preserve it instead
        # of silently discarding records, then initialise the versioned schema.
        columns = {row[1] for row in db.execute("PRAGMA table_info(analyses)")}
        if columns and "asset_id" not in columns:
            suffix = now().replace(":", "").replace("+", "_").replace("-", "").replace(".", "")
            for table in ("analyses", "feedback"):
                if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone():
                    db.execute(f"ALTER TABLE {table} RENAME TO {table}_legacy_{suffix}")
        job_sql = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='jobs'").fetchone()
        if job_sql and "legacy_" in (job_sql[0] or ""):
            db.execute(f"ALTER TABLE jobs RENAME TO jobs_legacy_{now().replace(':','').replace('+','_').replace('-','').replace('.','')}")
        db.executescript("""
    CREATE TABLE IF NOT EXISTS media_assets(id TEXT PRIMARY KEY, media_type TEXT NOT NULL, original_name TEXT NOT NULL, storage_key TEXT NOT NULL UNIQUE, sha256 TEXT NOT NULL, byte_size INTEGER NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS analyses(id TEXT PRIMARY KEY, asset_id TEXT NOT NULL REFERENCES media_assets(id), media_type TEXT NOT NULL, status TEXT NOT NULL, assessment TEXT, model_version TEXT, report TEXT, error_code TEXT, created_at TEXT NOT NULL, completed_at TEXT);
    CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, analysis_id TEXT NOT NULL REFERENCES analyses(id), kind TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, locked_at TEXT, error TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS feedback(id TEXT PRIMARY KEY, analysis_id TEXT NOT NULL REFERENCES analyses(id), claim TEXT NOT NULL, explanation TEXT, source_url TEXT, user_confidence TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS audit_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL, created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS model_versions(id TEXT PRIMARY KEY, version TEXT NOT NULL UNIQUE, modality TEXT NOT NULL, status TEXT NOT NULL, artifact_path TEXT NOT NULL, sha256 TEXT NOT NULL, metrics TEXT NOT NULL, created_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS jobs_pending ON jobs(status, created_at);
    CREATE INDEX IF NOT EXISTS analyses_asset ON analyses(asset_id);
    """)
def audit(db, entity_type, entity_id, action, details=None): db.execute("INSERT INTO audit_logs(entity_type,entity_id,action,details,created_at) VALUES(?,?,?,?,?)",(entity_type,entity_id,action,json.dumps(details or {}),now()))
