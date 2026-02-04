# 📄 SkillMatch – Resume Matcher & Skill Recommender

SkillMatch is an AI-powered tool designed to analyze resumes and job descriptions using Natural Language Processing (NLP). It identifies skill gaps, extracts technical keywords, and provides insights to help users tailor their resumes for specific job roles.

---

## 🚀 Features

*   **Resume Parsing**: Supports PDF and DOCX formats. Extracts text content while preserving structure.
*   **Job Description Analysis**: Processes raw job description text provided by the user.
*   **Intelligent Text Cleaning**:
    *   Removes stopwords, special characters, and noise.
    *   Standardizes text case for accurate matching.
*   **Skill Extraction**:
    *   Uses a curated database of technical skills (`data/skills_db.csv`).
    *   Identifies and extracts skills from both the Resume and Job Description.
*   **Interactive UI**: Built with Streamlit for a seamless, user-friendly experience.

---

## 📂 Project Structure

```
SkillMatch/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── WORKFLOW.md                 # Detailed information about the data flow
├── data/
│   ├── resumes/                # Directory for storing uploaded resumes
│   ├── job_descriptions/       # Directory for job description texts
│   └── skills_db.csv           # CSV database of technical skills
├── modules/
│   ├── resume_parser.py        # Logic for parsing PDF/DOCX resumes
│   ├── jd_parser.py            # Logic for processing job descriptions
│   ├── text_cleaner.py         # NLP preprocessing (cleaning, stopword removal)
│   └── skill_extractor.py      # Core logic for skill identification
└── utils/
    └── helpers.py              # Utility helper functions
```

---

## 🛠️ Setup & Installation

### 1. Clone or Download the repository
Ensure you have the project files locally.

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using `pip`.

```bash
pip install -r requirements.txt
```
*Note: This project relies on `nltk`, `streamlit`, `pandas`, `pdfplumber`, and `python-docx`.*

---

## ▶️ Usage

1.  **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

2.  **Interact with the UI**:
    *   **Upload Resume**: Select your Resume file (PDF or DOCX).
    *   **Paste Job Description**: Copy and paste requirements from the job posting.
    *   **Click "Analyze Resume"**: The system will process the texts.

3.  **View Results**:
    *   Extracted Text Preview.
    *   Cleaned Text Preview.
    *   **Skills Found in Resume**: Validated skills found in your document.
    *   **Skills Required in Job Description**: Skills identified in the JD.

---

## ✅ Development Progress (Milestone 1)

**Phase 1: Project Setup** - Folder structure & initial files.  
**Phase 2: UI Development** - Basic Streamlit interface.  
**Phase 3: Resume Extraction** - PDF/DOCX text parsing.  
**Phase 4: JD Processing** - Input handling & validation.  
**Phase 5: Text Cleaning** - NLP preprocessing & stopword removal.  
**Phase 6: Skill Database** - Creation & loading of skill dataset.  
**Phase 7: Skill Extraction** - Logic to identify specific skills.  

---

## 🔮 Future Roadmap (Milestone 2)

*   **Skill Gap Analysis**: Highlight missing skills.
*   **Match Score**: Calculate a percentage match between Resume and JD.
*   **Keyword Visualization**: Word clouds or charts.
*   **Resume Tips**: Suggestions for improvement based on the JD.
