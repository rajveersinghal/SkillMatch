# 🧩 SkillMatch - AI Resume Matcher

SkillMatch is an intelligent, AI-powered internal tool designed to match resumes with job descriptions accurately. It leverages Natural Language Processing (NLP) techniques to analyze text, extract skills, and calculate compatibility scores, helping recruiters and hiring managers streamline the screening process.

## 🚀 Key Features

*   **Intelligent Matching:** Uses TF-IDF vectorization and cosine similarity to match resumes against job descriptions.
*   **Skill Extraction:** Automatically identifies key technical and soft skills from documents.
*   **Detailed Analysis:** Provides a breakdown of matching skills, missing skills, and an overall compatibility score.
*   **User Management:** Secure authentication system for recruiters to manage their sessions.
*   **History Tracking:** Saves all analysis results for future reference.
*   **Modern UI:** Built with Streamlit for a responsive and interactive user experience.

## 🛠️ Tech Stack

*   **Frontend:** Streamlit, Custom CSS
*   **Backend:** FastAPI, Python 3.10+
*   **Database:** MongoDB Atlas
*   **NLP:** scikit-learn (TF-IDF), NLTK, spaCy
*   **Authentication:** JWT (JSON Web Tokens)
*   **Deployment:** Docker ready (optional)

## 📂 Project Structure

```
SkillMatch/
├── backend/            # FastAPI backend application
│   ├── routers/        # API routes (auth, documents)
│   └── main.py         # Entry point for the backend
├── core/               # Core business logic
│   └── ingestion.py    # Text extraction logic
├── frontend/           # Streamlit frontend application
│   ├── app.py          # Main Streamlit app
│   └── style.css       # Custom styling
├── nlp/                # NLP processing modules
│   ├── preprocessing.py # Text cleaning and normalization
│   └── skill_extractor.py # Skill extraction logic
├── data/               # Data storage (if local)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## ⚙️ Setup & Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/skillmatch.git
cd skillmatch
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your configuration:
```env
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application

**Start the Backend Server:**
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

**Start the Frontend Interface:**
Open a new terminal, activate the environment, and run:
```bash
streamlit run frontend/app.py
```
The application will open in your browser at `http://localhost:8501`.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
