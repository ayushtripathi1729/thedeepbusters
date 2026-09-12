# Deepfake Detection Website

A full-stack deepfake and misinformation detection platform featuring multi-modal analysis of images, videos, audio, text, and files with AI-powered detection models and an intuitive React frontend.

## Table of Contents
- [About The Project](#about-the-project)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## About The Project
This project aims to provide a comprehensive web platform to detect deepfakes using state-of-the-art AI models. Users can upload various media types for real-time authenticity checks, supported by a modern React UI and a robust Flask backend.

## Features
- Image, video, audio, text, and generic file upload and analysis
- Heatmap visualizations for detection results
- Secure file handling and upload processing
- Modular architecture for extensibility
- Responsive and user-friendly interface

## Technology Stack
- Backend: Python, Flask, PyTorch/TensorFlow (for models)
- Frontend: React, Tailwind CSS
- Other: REST APIs, Axios for HTTP requests

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Installation

1. Clone the repository:
git clone https://github.com/ayushtripathi1729/deepfake-detection-website.git
cd deepfake-detection-website


2. Set up backend environment:
cd backend
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
pip install -r requirements.txt


3. Set up frontend environment:
cd ../frontend
npm install

## Usage

### Backend
Start the Flask backend server:
cd backend
source venv/bin/activate # Activate your virtual environment
python app.py

### Frontend
Start the React frontend:
cd frontend
npm start
Open `http://localhost:3000` in the browser to access the app.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests for features, bug fixes, or improvements.

## Contact
Ayush Tripathi - [GitHub](https://github.com/ayushtripathi1729) - ayushtripathi2822@gmail.com

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
