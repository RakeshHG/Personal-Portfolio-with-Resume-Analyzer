# backend/resume_analyzer.py
import google.generativeai as genai
from backend.utils import clean_text

def initialize_gemini(api_key):
    """Initializes the Gemini Pro model."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def analyze_resume(model, resume_text):
    """Analyzes the resume text using the Gemini Pro model."""
    prompt = f"""
    Analyze the following resume and extract the following information in a structured JSON format:

    - Technical Skills: A list of technical skills mentioned in the resume.
    - Soft Skills: A list of soft skills or personal qualities highlighted.
    - Work Experience: A list of job titles, company names, employment periods, and key responsibilities/achievements for each role.
    - Education: A list of degrees, institutions, graduation dates (if mentioned), and relevant coursework or honors.
    - Projects: A list of projects, their descriptions, and technologies used.

    Also, provide a brief summary of the candidate's profile and suggest 3 key areas for improvement in their resume based on common best practices.

    Resume:
    ```
    {resume_text}
    ```

    Format the output as a JSON object with the keys: "technical_skills", "soft_skills", "work_experience", "education", "projects", "profile_summary", "improvement_suggestions".
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during resume analysis: {e}"

if __name__ == '__main__':
    # Example usage (replace with your actual API key and resume file)
    from backend.config import GEMINI_API_KEY
    from backend.utils import extract_text_from_pdf

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in config.py or .env file.")
    else:
        model = initialize_gemini(GEMINI_API_KEY)
        resume_path = '../example_resume.pdf'  # Replace with a sample PDF
        resume_content = extract_text_from_pdf(resume_path)

        if resume_content:
            analysis_result = analyze_resume(model, resume_content)
            print(analysis_result)
        else:
            print("Could not extract text from the example resume.")