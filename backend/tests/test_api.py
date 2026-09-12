import os, tempfile
from io import BytesIO
from pathlib import Path
from PIL import Image

def test_queue_and_worker(monkeypatch):
    root=tempfile.mkdtemp(); monkeypatch.setenv("DATA_DIR",root); monkeypatch.setenv("DATABASE_PATH",str(Path(root)/"db.sqlite")); monkeypatch.setenv("STORAGE_DIR",str(Path(root)/"media")); monkeypatch.setenv("EAGER_JOBS","1")
    import importlib, maayabreaker.config, maayabreaker.database, app
    importlib.reload(maayabreaker.config); importlib.reload(maayabreaker.database); importlib.reload(app)
    raw=BytesIO();Image.new("RGB",(4,4)).save(raw,format="PNG")
    response=app.app.test_client().post("/api/analyze/image",data={"file":(BytesIO(raw.getvalue()),"x.png")})
    assert response.status_code==202
    analysis=app.app.test_client().get(response.get_json()["status_url"]);assert analysis.status_code==200;assert analysis.get_json()["assessment"]=="inconclusive"
