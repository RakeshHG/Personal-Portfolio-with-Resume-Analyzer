# Intelligent Personal Portfolio with Resume Analyzer

This project is a cloud-based personal portfolio website that dynamically showcases achievements, skills, and projects. It also integrates intelligent features for resume analysis using the Gemini API and provides job recommendations by matching the user's resume with job descriptions scraped from online portals.

## Features

- **Dynamic Portfolio Showcase:** Automatically aggregates data from LeetCode, GitHub, LinkedIn, and YouTube to keep the portfolio current. (Implementation details for this will depend on the specific APIs of these platforms and are left as an exercise for the user.)
- **Resume Upload and Analysis:** Allows users to upload their resume (PDF). The backend extracts key information (skills, experience, education, projects) using the Gemini API and presents it visually.
- **Job Description Scraping and Matching:** Periodically fetches job listings from popular job portals, compares them against the analyzed resume, calculates relevance scores, and recommends suitable job openings.
- **Resume Improvement Suggestions:** The Gemini API analysis can also provide suggestions for improving the resume based on common best practices and the content of relevant job descriptions.

## File Structure