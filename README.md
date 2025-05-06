# Job Research Pro - AI-Powered Job Matching System

## Overview

Job Research Pro is a comprehensive job matching system that combines web scraping with AI-powered analysis to help job seekers find the best opportunities. The system consists of two main components:

1. **Scraper (app.py)**: Collects job listings from CoolStartupJobs.com
2. **Streamlit Web App (stream.py)**: Provides an interactive interface for job searching and CV analysis

## Features

### Scraper Module (`app.py`)
- Scrapes job listings from CoolStartupJobs.com with pagination support
- Extracts key job information including:
  - Company name
  - Job title
  - Location
  - Job URL
  - Posting date
- Implements polite scraping with:
  - Random delays between requests
  - Error handling
  - User-agent rotation
- Saves results to timestamped CSV files

### Streamlit Web App (`stream.py`)
- Interactive job search interface with:
  - Natural language query processing
  - AI-powered job matching
  - CV analysis (supports PDF, DOCX, PNG, TXT)
- Key functionalities:
  - **Job Matching**: Finds relevant jobs based on skills/role queries
  - **CV Analysis**: Evaluates experience level and suggests improvements
  - **AI Recommendations**: Provides tailored job suggestions with match reasons
- Integration with DeepInfra's LLM API for advanced analysis

## System Requirements

- Python 3.8+
- Required Python packages (see `requirements.txt`)
- Tesseract OCR installed (for image CV processing)
- DeepInfra API key (set in `.env` file)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd job-research-pro
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - Windows: Download from [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

4. Create a `.env` file with your DeepInfra API key:
   ```
   DEEPINFRA_API_KEY=your_api_key_here
   ```

## Usage

### Running the Scraper
```bash
python app.py
```
This will:
1. Scrape job listings from CoolStartupJobs.com
2. Save results to a timestamped CSV file (e.g., `coolstartupjobs_20240506_143022.csv`)

### Running the Web App
```bash
streamlit run stream.py
```
This will launch the interactive web interface in your default browser.

## Web App Features

### Job Search
- Enter natural language queries (e.g., "Python jobs at startups")
- View AI-curated job matches with relevance explanations

### CV Analysis
- Upload your CV in multiple formats (PDF, DOCX, PNG, TXT)
- Get:
  - Experience level assessment (Junior/Mid/Senior)
  - Top job matches with fit scores
  - Specific CV improvement suggestions

## Configuration

Key configuration options in `stream.py`:
- `CSV_PATH`: Path to the jobs CSV file
- `DEEPINFRA_API_URL`: LLM endpoint URL
- `SYSTEM_PROMPTS`: Customize AI behavior for job matching and CV analysis

## Output Examples

### Scraper Output
```
Starting CoolStartupJobs.com scraper...

Scraping page 1: https://www.coolstartupjobs.com/startups?p=1
Found 12 companies on page 1

Processing company: https://www.coolstartupjobs.com/startups/acme-corp
Found 5 job cards at Acme Corp
Completed 5 cards at Acme Corp

Scraping complete. Processed 12 companies and 42 jobs total.
Saved 42 jobs to coolstartupjobs_20240506_143022.csv
```

### Web App Output
```
--- EXPERIENCE LEVEL ---
Mid-level (Pleno) - 3 years of Python development with Django experience, but no large-scale system design experience.

--- TOP 3 MATCHES ---
1. Python Developer at TechStart
   - Match Strength: 9/10
   - Why Fit: Perfect stack alignment, growing startup with mentorship

--- CV IMPROVEMENTS ---
- Add metrics to project descriptions
- Include any open-source contributions
- Highlight specific technical challenges overcome
```

## Limitations
- Scraper is dependent on CoolStartupJobs.com's HTML structure
- CV analysis accuracy depends on input quality
- API usage may be rate-limited

## Future Enhancements
- Add more job sources
- Implement user accounts for saved searches
- Add email alerts for new matching jobs
- Enhanced CV parsing with more file formats
