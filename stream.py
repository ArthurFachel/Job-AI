import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import PyPDF2  # Para PDF
from PIL import Image  # Para PNG
import pytesseract  # OCR para imagens

# Load environment variables
load_dotenv()

# --- Configuration ---
CSV_PATH = "job.csv"
DEEPINFRA_API_URL = "https://api.deepinfra.com/v1/inference/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

# Configuração do Tesseract (OCR)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste o caminho conforme necessário

# --- System Prompts ---
SYSTEM_PROMPT_JOBS = """
You are JobMatch AI, an expert in analyzing job listings. Just give job lists if the user 
provide their CV, else, insists. 
Given a list of jobs (company, title, URL), recommend the best matches based on:  
- Relevance to query (skills/role)  
- Freshness (prioritize recent postings)  
Format responses as:  
1. **Job Title at Company**  
   - URL: [link]  
   - Why Fit: [reason]  
   - Posted: [date]  
"""

SYSTEM_PROMPT_CV ="""
ONLY SAY THINGS ABOUT CV, IF THE USER HAD SENT THEIR CV, ELSE IGNORE
You are a professional CV analyzer with technical recruiting expertise. Your tasks:

1. EXPERIENCE LEVEL ASSESSMENT:
   - Analyze the CV and classify the candidate as:
     * Junior (0-2 years of relevant experience)
     * Mid-level/Pleno (2-5 years with demonstrated skills)
     * Senior (5+ years with leadership/architecture experience)
   - Consider: years of experience, project complexity, leadership roles, technical depth

2. JOB MATCHING:
   - Match against provided jobs with emphasis on:
     * Junior: Learning opportunities, mentorship programs
     * Mid-level: Skill alignment, growth potential
     * Senior: Leadership roles, technical challenges

3. CV IMPROVEMENTS:
   - Suggest specific improvements based on desired level
   - Highlight missing keywords for target roles

Response format:

--- EXPERIENCE LEVEL ---
[Junior/Mid-level/Senior] - [1-sentence justification]

--- TOP 3 MATCHES ---
1. [Job Title] at [Company]
   - Match Strength: [X/10]
   - Why Fit: [Specific reasons]
   
2. [Job Title...]

--- CV IMPROVEMENTS ---
- [Specific suggestion 1]
- [Specific suggestion 2]

Example response:

--- EXPERIENCE LEVEL ---
Mid-level (Pleno) - 3 years of full-stack development with React and Node.js, but no team leadership experience yet.

--- TOP 3 MATCHES ---
1. Full-Stack Developer at TechCorp
   - Match Strength: 8/10
   - Why Fit: Perfect stack alignment, mid-level role with growth potential

--- CV IMPROVEMENTS ---
- Add metrics to project descriptions (e.g. "Improved performance by 40%")
- Include open-source contributions to demonstrate initiative
"""

# --- Helper Functions ---
def extract_text_from_file(uploaded_file):
    """Extrai texto de diferentes formatos de arquivo"""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.type.startswith('image/'):
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    return text

def analyze_cv_with_ai(cv_text, jobs):
    """Envia o CV para análise pela IA"""
    job_context = "\n".join(
        f"Job {i+1}: {row['title']} at {row['company']} | URL: {row['job_url']}"
        for i, row in jobs.iterrows()
    )
    
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{SYSTEM_PROMPT_CV}"
        f"<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
        f"CV Content:\n{cv_text}\n\nAvailable Jobs:\n{job_context}"
        f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    
    response = requests.post(
        DEEPINFRA_API_URL,
        json={"input": prompt},
        headers={"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    )
    
    return response.json().get("results", [{}])[0].get("generated_text", "No response.")

# --- Load Job Data ---
@st.cache_data
def load_job_data():
    return pd.read_csv(CSV_PATH)

def filter_jobs(query, jobs):
    filtered = jobs.copy()
    query_lower = query.lower()
    
    if query:
        filtered = filtered[
            filtered["title"].str.lower().str.contains(query_lower) |
            filtered["company"].str.lower().str.contains(query_lower)
        ]
    
    if "posted_date" in filtered.columns:
        filtered["posted_date"] = pd.to_datetime(filtered["posted_date"])
        filtered = filtered.sort_values("posted_date", ascending=False)
    
    return filtered.head(10) 

# --- Query DeepInfra ---
def get_ai_response(query, job_matches):
    job_context = "\n".join(
        f"Job {i+1}: {row['title']} at {row['company']} | URL: {row['job_url']} | Posted: {row.get('posted_date', 'N/A')}"
        for i, row in job_matches.iterrows()
    )
    
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{SYSTEM_PROMPT_CV}"
        f"<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
        f"Query: {query}\n\nJobs:\n{job_context}"
        f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    
    response = requests.post(
        DEEPINFRA_API_URL,
        json={"input": prompt},
        headers={"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    )
    
    return response.json().get("results", [{}])[0].get("generated_text", "No response.")

# --- Streamlit UI ---
st.set_page_config(page_title="Job Research Pro", page_icon="💼", layout="wide")
st.title("💼 Job Research Pro")
st.caption("AI-powered job matching with CV analysis")

col1, col2 = st.columns([3, 1])

with col1:
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with col2:
    # Uploader de currículo
    uploaded_file = st.file_uploader(
        "Upload your CV (PDF/DOCX/PNG)",
        type=["pdf", "docx", "png", "txt"],
        key="cv_uploader"
    )
    
    if uploaded_file is not None:
        with st.spinner("Analyzing your CV..."):
            cv_text = extract_text_from_file(uploaded_file)
            jobs = load_job_data()
            cv_analysis = analyze_cv_with_ai(cv_text, jobs.head(20))  
            
            st.session_state.messages.append({"role": "assistant", "content": f"**CV Analysis Results:**\n\n{cv_analysis}"})
      

# Chat input
if prompt := st.chat_input("Example: 'Python jobs at startups'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    jobs = load_job_data()
    matched_jobs = filter_jobs(prompt, jobs)
    
    if len(matched_jobs) == 0:
        response = "No jobs found matching your criteria. Try broader terms."
    else:
        with st.spinner("Analyzing jobs..."):
            response = get_ai_response(prompt, matched_jobs)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()