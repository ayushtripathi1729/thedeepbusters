import json, uuid
from pathlib import Path
from .database import connect, now, audit
from .detectors import registry, DetectorUnavailable
from .forensics import inspect
from .config import settings

def enqueue(analysis_id):
    job_id = str(uuid.uuid4())
    with connect() as db: db.execute("INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?)",(job_id,analysis_id,"analysis","queued",0,None,None,now(),now())); audit(db,"analysis",analysis_id,"queued",{"job_id":job_id})
    return job_id
def claim():
    with connect() as db:
        row=db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY created_at LIMIT 1").fetchone()
        if not row:return None
        db.execute("UPDATE jobs SET status='processing',attempts=attempts+1,locked_at=?,updated_at=? WHERE id=? AND status='queued'",(now(),now(),row['id']))
        if db.total_changes != 1:return None
        return dict(row)
def process_one():
    job=claim()
    if not job:return False
    with connect() as db:
        row=db.execute("SELECT a.*,m.storage_key,m.sha256,m.byte_size,m.original_name FROM analyses a JOIN media_assets m ON m.id=a.asset_id WHERE a.id=?",(job['analysis_id'],)).fetchone()
        db.execute("UPDATE analyses SET status='processing' WHERE id=?",(job['analysis_id'],))
    try:
        signals=inspect(Path(settings.storage_dir)/row['storage_key'],row['media_type']); prediction=None; model_version=None
        try:
            output=registry.get(settings.production_model).predict(Path(settings.storage_dir)/row['storage_key'])
            prediction={"manipulated_probability":output.manipulated_probability,"uncertainty":output.uncertainty,"evidence":output.evidence}; model_version=output.model_version
            assessment="likely_manipulated" if output.uncertainty < .2 and output.manipulated_probability >= .75 else "likely_authentic" if output.uncertainty < .2 and output.manipulated_probability <= .25 else "inconclusive"
        except DetectorUnavailable: assessment="inconclusive"
        report={"stages":["validated","metadata extracted","forensic checks complete"],"forensic_signals":signals,"model_prediction":prediction,"limitations":["Forensic signals are contextual evidence, not proof."] if prediction else ["No validated detection model is configured on this server."],"recommendation":"Verify consequential content using the original source and independent reporting."}
        with connect() as db: db.execute("UPDATE analyses SET status='completed',assessment=?,model_version=?,report=?,completed_at=? WHERE id=?",(assessment,model_version,json.dumps(report),now(),job['analysis_id'])); db.execute("UPDATE jobs SET status='completed',updated_at=? WHERE id=?",(now(),job['id'])); audit(db,"analysis",job['analysis_id'],"completed",{"model_version":model_version})
    except Exception as exc:
        with connect() as db: db.execute("UPDATE analyses SET status='failed',error_code='analysis_failed',completed_at=? WHERE id=?",(now(),job['analysis_id'])); db.execute("UPDATE jobs SET status='failed',error=?,updated_at=? WHERE id=?",(str(exc)[:500],now(),job['id'])); audit(db,"analysis",job['analysis_id'],"failed",{})
    return True
