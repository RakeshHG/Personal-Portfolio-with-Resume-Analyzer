// frontend/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const resumeInput = document.getElementById('resume-input');
    const analyzeButton = document.getElementById('analyze-button');
    const resumeAnalysisDiv = document.getElementById('resume-analysis');
    const jobListDiv = document.getElementById('job-list');

    analyzeButton.addEventListener('click', async () => {
        const file = resumeInput.files[0];
        if (!file) {
            alert('Please select a resume file.');
            return;
        }

        const formData = new FormData();
        formData.append('resume', file);

        try {
            const response = await fetch('/analyze_resume', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to analyze resume');
            }

            const data = await response.json();
            console.log("Resume analysis data:", data);

            // Display the analysis - adjust based on the structure of your data
            if (data.raw_analysis) {
                resumeAnalysisDiv.textContent = data.raw_analysis;
            } else {
                let analysisHTML = '<h3>Resume Analysis:</h3>';
                analysisHTML += '<pre>' + JSON.stringify(data, null, 2) + '</pre>'; // Pretty print JSON
                resumeAnalysisDiv.innerHTML = analysisHTML;
            }

        } catch (error) {
            console.error('Error analyzing resume:', error);
            resumeAnalysisDiv.textContent = 'Error: ' + error.message;
        }
    });

    async function fetchAndDisplayJobs() {
        try {
            const response = await fetch('/scrape_and_match');
            if (!response.ok) {
                throw new Error('Failed to fetch job matches');
            }
            const jobs = await response.json();
            console.log("Job matches:", jobs);

            let jobListHTML = '<h3>Job Matches:</h3>';
            jobs.forEach(match => {
                jobListHTML += `
                    <div class="job-item">
                        <h4><a href="${match.job.url}" target="_blank">${match.job.title}</a> (${match.job.company})</h4>
                        <p>Location: ${match.job.location}</p>
                        <p>Relevance: ${(match.relevance_score * 100).toFixed(2)}%</p>
                    </div>
                `;
            });
            jobListDiv.innerHTML = jobListHTML;

        } catch (error) {
            console.error('Error fetching job matches:', error);
            jobListDiv.textContent = 'Error: ' + error.message;
        }
    }

    // Fetch and display jobs when the page loads
    fetchAndDisplayJobs();
});