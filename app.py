import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    """Generates AI response using Gemini API with structured JSON output."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response.text.strip()  

def extract_text_from_pdf(uploaded_file):
    """Extracts text content from an uploaded PDF file."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text() or ""  
    return text.strip()  

def format_prompt(resume_text, jd_text):
    """Formats the prompt to ensure AI returns structured JSON output."""
    return f"""
    Act as an advanced ATS (Application Tracking System) with expertise in 
    software engineering, data science, data analytics, and big data engineering.

    Your task:
    - Analyze the given resume against the job description.
    - Assign a **percentage match**.
    - Identify **missing keywords**.
    - Provide a **brief profile summary**.

    **Return the response in strict JSON format**:
    {{
        "JD Match": "xx%",
        "Missing Keywords": ["keyword1", "keyword2"],
        "Profile Summary": "A brief summary..."
    }}

    **Resume:** {resume_text}
    **Job Description:** {jd_text}
    """

# Streamlit UI
st.title("🚀 Smart ATS - Resume Evaluator")
st.text("Improve Your Resume ATS Score & Get Job-Ready!")

jd = st.text_area("📄 Paste the Job Description here", height=150)

uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF only)", type="pdf", help="Upload a PDF resume for analysis.")

if st.button("🔍 Analyze Resume"):
    if uploaded_file is not None and jd.strip():
        with st.spinner("⏳ Processing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            prompt = format_prompt(resume_text, jd)
            retry_attempts = 2
            for attempt in range(retry_attempts):
                response_text = get_gemini_response(prompt)

                try:
                   
                    response_text = response_text.strip("`").strip()
                    result = json.loads(response_text)
                    break  
                except json.JSONDecodeError:
                    if attempt == retry_attempts - 1:
                        st.error("❌ AI response was not structured correctly after retries.")
                        st.write("🔍 Raw AI Response:", response_text)  
                        result = None  

        
            if result:
                st.subheader("✅ ATS Analysis Results")
                st.write(f"**📊 JD Match:** {result.get('JD Match', 'N/A')}")
                
                missing_keywords = result.get("Missing Keywords", [])
                st.write(f"**📌 Missing Keywords:** {', '.join(missing_keywords) if missing_keywords else 'None'}")
                
                st.write(f"**📄 Profile Summary:** {result.get('Profile Summary', 'No summary available.')}")

    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")
