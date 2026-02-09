# SkillMatch 🚀

SkillMatch is a powerful AI-driven application designed to streamline the recruitment process by automatically extracting and analyzing skills from resumes and job descriptions. It leverages FastAPI for a high-performance backend and React for a modern, responsive frontend.

## ✨ Features

- **User Authentication**: Secure signup and login system using JWT tokens.
- **Resume Ingestion**: Upload PDF, DOCX, or TXT resumes or paste text directly.
- **Job Description (JD) Ingestion**: Upload or paste job descriptions to compare against resumes.
- **Automated Text Extraction**: Integrated extraction logic to pull content from various file formats.
- **Interactive Dashboard**: A sleek, modern dashboard built with React and Framer Motion for a premium user experience.

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [MongoDB](https://www.mongodb.com/) (using Motor driver)
- **Security**: JWT Authentication, CORS Middleware
- **Libraries**: `python-multipart`, `python-jose`, `passlib`, `pdfplumber`, `python-docx`

### Frontend
- **Framework**: [React](https://reactjs.org/) (Vite)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm
- MongoDB instance (local or Atlas)

### Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
4. Configure `.env` with your MongoDB URI and secret keys.
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the `react-frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 📂 Project Structure

- `backend/`: FastAPI application code, routes, models, and database logic.
- `react-frontend/`: React components, pages, and API clients.
- `data/`: Storage for processed or sample data.
- `tests/`: Backend unit tests.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
Built with ❤️ by [Rajveer Singhal](https://github.com/rajveersinghal)
