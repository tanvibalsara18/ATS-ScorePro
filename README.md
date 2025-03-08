# 🚀 Smart ATS – AI Resume Analyzer  

🔗 **Live Demo:** [ATS ScorePro](https://ats-scorepro.streamlit.app/)  

Smart ATS evaluates resumes against job descriptions using **Google Gemini AI**, providing a **match percentage, missing keywords, and a profile summary** to optimize resumes.  

## 🔹 Features  
✅ Resume parsing (PDF)  
✅ AI-powered JD match analysis  
✅ Missing keyword suggestions  
✅ Profile summary generation  

## ⚙️ Tech Stack  
- **Python** (Backend)  
- **Streamlit** (UI)  
- **Google Gemini AI** (Analysis)  
- **PyPDF2** (PDF Parsing)  

## 🚀 Setup  
```bash
git clone https://github.com/tanvibalsara18/ATS-ScorePro  
cd ATS-ScorePro  
pip install -r requirements.txt  
echo "GOOGLE_API_KEY=your_api_key_here" > .env  
streamlit run app.py  
