"""HTTP API. Expensive analysis is persisted then handled by worker.py."""
import json, os, uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from maayabreaker.config import settings
from maayabreaker.database import connect, init, now, audit
from maayabreaker.storage import save_upload, path_for, expiration
from maayabreaker.validation import detect_type, validate_image
from maayabreaker.jobs import enqueue, process_one

app=Flask(__name__); app.config["MAX_CONTENT_LENGTH"]=settings.max_media_bytes
CORS(app,resources={r"/api/*":{"origins":os.getenv("CORS_ORIGINS","http://localhost:3000").split(",")}})
def error(message,code=400): return jsonify({"error":{"message":message,"code":code}}),code
def serialise(analysis_id):
    with connect() as db: row=db.execute("SELECT a.*,m.sha256,m.byte_size,m.original_name FROM analyses a JOIN media_assets m ON m.id=a.asset_id WHERE a.id=?",(analysis_id,)).fetchone()
    if not row:return None
    data=dict(row); data["report"]=json.loads(data["report"]) if data["report"] else None; return data
def create_analysis(expected):
    upload=request.files.get("file")
    if not upload or not upload.filename:return error("Choose a media file to analyze.")
    try: key,name,digest,size=save_upload(upload.stream,upload.filename)
    except ValueError:return error("This file exceeds the configured upload limit.",413)
    actual=detect_type(path_for(key),name)
    if actual!=expected: path_for(key).unlink(missing_ok=True); return error(f"The upload is not a supported {expected} file.",415)
    try:
        if expected=="image": validate_image(path_for(key),settings.max_image_bytes)
    except ValueError as exc: path_for(key).unlink(missing_ok=True); return error(str(exc).replace("_"," "),415)
    asset_id,analysis_id=str(uuid.uuid4()),str(uuid.uuid4())
    with connect() as db:
        db.execute("INSERT INTO media_assets VALUES(?,?,?,?,?,?,?,?)",(asset_id,expected,name,key,digest,size,now(),expiration()))
        db.execute("INSERT INTO analyses VALUES(?,?,?,?,?,?,?,?,?,?)",(analysis_id,asset_id,expected,"queued",None,None,None,None,now(),None))
        audit(db,"analysis",analysis_id,"created",{"media_type":expected})
    job_id=enqueue(analysis_id)
    if settings.eager_jobs: process_one()
    return jsonify({"analysis_id":analysis_id,"job_id":job_id,"status":"queued","status_url":f"/api/analysis/{analysis_id}"}),202
@app.get("/api/health")
def health(): return jsonify({"status":"ok","service":"maayabreaker-api","worker_required":not settings.eager_jobs,"production_model":settings.production_model or None})
@app.get("/api/models")
def models():
    with connect() as db: rows=[dict(r) for r in db.execute("SELECT id,version,modality,status,metrics,created_at FROM model_versions ORDER BY created_at DESC")]
    for row in rows:row["metrics"]=json.loads(row["metrics"])
    return jsonify({"models":rows})
@app.post("/api/analyze/<media_type>")
def analyze(media_type):
    if media_type not in {"image","video","audio"}:return error("Unsupported media type.",404)
    return create_analysis(media_type)
@app.get("/api/analysis/<analysis_id>")
def analysis(analysis_id):
    value=serialise(analysis_id); return jsonify(value) if value else error("Analysis not found.",404)
@app.post("/api/analysis/<analysis_id>/feedback")
def feedback(analysis_id):
    if not serialise(analysis_id):return error("Analysis not found.",404)
    payload=request.get_json(silent=True) or {}; claim=payload.get("claim")
    if claim not in {"authentic","manipulated","unsure","result_incorrect"}:return error("Choose a valid feedback claim.")
    feedback_id=str(uuid.uuid4())
    with connect() as db:
        db.execute("INSERT INTO feedback VALUES(?,?,?,?,?,?,?,?)",(feedback_id,analysis_id,claim,str(payload.get("explanation", ""))[:2000],str(payload.get("source_url", ""))[:500],payload.get("user_confidence"),"submitted",now()))
        audit(db,"feedback",feedback_id,"submitted",{"analysis_id":analysis_id})
    return jsonify({"id":feedback_id,"status":"submitted","message":"Feedback is unverified and requires review before it can inform a dataset."}),201
@app.errorhandler(RequestEntityTooLarge)
def oversized(_):return error("This file exceeds the configured upload limit.",413)
@app.errorhandler(500)
def unexpected(_):return error("The analysis service encountered an unexpected error.",500)
init()
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=os.getenv("FLASK_DEBUG")=="1")
