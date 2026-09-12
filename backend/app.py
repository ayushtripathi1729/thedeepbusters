from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import your detection blueprints
from detect_image import detect_image_bp
from detect_video import detect_video_bp
from detect_audio import detect_audio_bp
from detect_text import detect_text_bp

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests for all routes

# Register all detection blueprints with consistent /api prefix
app.register_blueprint(detect_image_bp, url_prefix='/api')
app.register_blueprint(detect_video_bp, url_prefix='/api')
app.register_blueprint(detect_audio_bp, url_prefix='/api')
app.register_blueprint(detect_text_bp, url_prefix='/api')

# Ensure essential static folders exist
for folder in ["static/uploads", "static/heatmaps", "static/results", "models"]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def index():
    return jsonify({
        "message": "Deepfake Detection API running",
        "endpoints": {
            # Updated endpoints to include /api prefix and consistent naming with blueprints
            "image_detection": "/api/detect-image [POST with file or url]",
            "video_detection": "/api/detect-video [POST with file or url]",
            "audio_detection": "/api/detect-audio [POST with file or url]",
            "text_detection": "/api/detect-text [POST with file or url or raw text]"
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
