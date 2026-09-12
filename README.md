# MaayaBreaker / The DeepBusters

An evidence-first digital-media forensics platform. The current implementation provides a polished React analysis experience, secure media intake, forensic metadata extraction, persistent analysis records, and a human-review feedback queue.

## What is implemented

- Responsive React landing page, analysis workspace, result state, feedback controls, and verification guidance.
- Flask JSON API with image, video, and audio upload validation.
- Magic-byte validation, filename sanitisation, upload-size limits, image decode verification, SHA-256 hashes, and no permanent media-file storage.
- SQLite persistence for analyses and unverified feedback.
- Image evidence: decoded format, dimensions, and EXIF-presence indicator.
- Honest model state: no prediction or confidence is emitted until a validated detector is configured.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Service and model readiness |
| POST | `/api/analyze/image` | Validate and inspect an image upload |
| POST | `/api/analyze/video` | Validate a video upload container |
| POST | `/api/analyze/audio` | Validate an audio upload container |
| GET | `/api/analysis/:id` | Retrieve an analysis record |
| POST | `/api/analysis/:id/feedback` | Submit unverified review feedback |

Analysis endpoints accept `multipart/form-data` with a `file` field. Feedback accepts a claim of `authentic`, `manipulated`, `unsure`, or `result_incorrect`.

## Run locally

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Flask Flask-Cors Pillow
python app.py
```

For the production-shaped asynchronous flow, start the API and worker separately:

```powershell
cd backend
python app.py
# separate terminal
python worker.py
```

In another terminal:

```powershell
cd frontend
npm install
npm start
```

Copy `.env.example` to `.env` and adjust paths, origins, and limits. `REACT_APP_API_URL` is available when the API is hosted separately.

## Model integration roadmap

The legacy model scripts remain outside the production request path because their model identifiers are placeholders and cannot yield trustworthy results. A production adapter should expose a registered version/checksum, calibrated probabilities, uncertainty/OOD handling, evidence artifacts, benchmark metrics, and background processing for video/audio. Training data and user feedback must remain separated until feedback has undergone verification.

## Research programs

The `ml/` package is intentionally separate from the API.

```powershell
# Validate an identity/source-safe dataset manifest and create a reproducible run record
python -m ml.training.train --config ml/configs/example.json

# Score an exported prediction JSONL file (one {"label": 0|1, "score": 0..1} per line)
python -m ml.evaluation.evaluate --predictions predictions.jsonl --output evaluation.json
```

Dataset manifests require a media path, binary label, split, and should include `source_id` or `identity_id`. The loader rejects split leakage when a source/identity appears across multiple splits. Evaluation reports accuracy, precision, recall, F1, balanced accuracy, error rates, a confusion matrix, and expected calibration error.

## Limitations

This repository does **not** yet contain validated weights, a background queue, authentication/admin review, model registry, benchmark runner, or training pipeline. It must not be represented as a deepfake detector until those capabilities are implemented and evaluated.
