# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.utils import extract_text_from_pdf
from backend.resume_analyzer import initialize_gemini, analyze_resume
from backend.job_scraper import scrape_jobs
from backend.job_matcher import match_resume_to_jobs
from backend.config import GEMINI_API_KEY, JOB_PORTAL_URLS
import os
import json

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for local development

# Initialize Gemini model
gemini_model = None
if GEMINI_API_KEY:
    gemini_model = initialize_gemini(GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found. Resume analysis will not function.")

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('../frontend/css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('../frontend/js', path)

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume_endpoint():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        pdf_path = f"temp_{file.filename}"
        file.save(pdf_path)
        resume_text = extract_text_from_pdf(pdf_path)
        os.remove(pdf_path)
        if resume_text:
            if gemini_model:
                analysis_result_str = analyze_resume(gemini_model, resume_text)
                try:
                    analysis_result = json.loads(analysis_result_str)
                    return jsonify(analysis_result)
                except json.JSONDecodeError:
                    return jsonify({'raw_analysis': analysis_result_str, 'error': 'Could not parse JSON analysis'}), 500
            else:
                return jsonify({'error': 'Gemini API key not configured'}), 500
        else:
            return jsonify({'error': 'Could not extract text from PDF'}), 500
    return jsonify({'error': 'Invalid file format. Only PDF files are allowed'}), 400

@app.route('/scrape_and_match')
def scrape_and_match_endpoint():
    scraped_jobs = scrape_jobs(JOB_PORTAL_URLS)
    # For demonstration, let's load a dummy resume analysis result
    # In a real application, you would likely store this per user
    try:
        with open('sample_resume_analysis.json', 'r') as f:
            sample_resume_analysis = f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Sample resume analysis file not found. Please run resume analysis first.'}), 500

    ranked_jobs = match_resume_to_jobs(sample_resume_analysis, scraped_jobs)
    return jsonify(ranked_jobs)

if __name__ == '__main__':
    # Create a dummy sample_resume_analysis.json for demonstration
    sample_analysis_data = {
        "technical_skills": ["Python", "JavaScript", "SQL", "AWS", "Docker"],
        "soft_skills": ["Communication", "Teamwork", "Problem-solving"],
        "work_experience": [],
        "education": [],
        "projects": [],
        "profile_summary": "A motivated individual...",
        "improvement_suggestions": []
    }
    with open('sample_resume_analysis.json', 'w') as f:
        json.dump(sample_analysis_data, f, indent=4)

    app.run(debug=True)