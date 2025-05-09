# backend/job_matcher.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def match_resume_to_jobs(resume_analysis_json, job_listings):
    """Matches the skills and experience from the resume analysis to job descriptions."""
    try:
        resume_data = json.loads(resume_analysis_json)
        resume_text = " ".join(resume_data.get("technical_skills", []) + resume_data.get("soft_skills", []) + [item.get("description", "") for item in resume_data.get("work_experience", [])] + [item.get("description", "") for item in resume_data.get("projects", [])])
    except json.JSONDecodeError as e:
        print(f"Error decoding resume analysis JSON: {e}")
        return []

    job_texts = [job.get("title", "") + " " + job.get("company", "") for job in job_listings]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text] + job_texts)
    resume_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    job_matches = []
    for i, job in enumerate(job_listings):
        similarity_score = cosine_similarity(resume_vector, job_vectors[i])[0][0]
        job_matches.append({"job": job, "relevance_score": similarity_score})

    # Sort jobs by relevance score in descending order
    ranked_jobs = sorted(job_matches, key=lambda x: x["relevance_score"], reverse=True)
    return ranked_jobs

if __name__ == '__main__':
    # Example usage (replace with your actual resume analysis output and scraped jobs)
    sample_resume_analysis = """
    {
        "technical_skills": ["Python", "JavaScript", "SQL", "AWS", "Docker"],
        "soft_skills": ["Communication", "Teamwork", "Problem-solving"],
        "work_experience": [
            {"title": "Software Engineer", "company": "Tech Inc.", "description": "Developed web applications using Python and Flask."}
        ],
        "education": [],
        "projects": [],
        "profile_summary": "A highly motivated software engineer...",
        "improvement_suggestions": []
    }
    """
    sample_jobs = [
        {"title": "Software Engineer", "company": "Another Tech", "location": "Remote", "url": "...", "description": "Looking for a Python and AWS expert."},
        {"title": "Data Analyst", "company": "Data Corp", "location": "Bengaluru", "url": "...", "description": "Experience with SQL and data visualization required."},
        {"title": "Frontend Developer", "company": "Web Solutions", "location": "Mumbai", "url": "...", "description": "Proficiency in JavaScript and React needed."}
    ]

    ranked_jobs = match_resume_to_jobs(sample_resume_analysis, sample_jobs)
    for match in ranked_jobs:
        print(f"Job: {match['job']['title']} ({match['job']['company']}) - Relevance: {match['relevance_score']:.2f}")