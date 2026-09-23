# 📄 ResumeAI — AI-Powered Resume Analyzer

ResumeAI is a Streamlit-based NLP application that analyzes a resume against a target job description.

The application extracts text from a resume PDF, preprocesses the text, calculates resume–job-description similarity using TF-IDF and cosine similarity, identifies matching and missing technical skills, and provides basic resume-tailoring recommendations.

## 🚀 Live Demo

**Live App:** [Add your Streamlit deployment URL here after deployment.](https://ai-resume-analyzer18.streamlit.app/)

**GitHub:** [Add your GitHub repository URL here.](https://github.com/amanchoudhary1812/ResumeAI)

---

## ✨ Features

- Upload a resume in PDF format
- Extract text from the resume using PyPDF2
- Paste a target job description
- Clean and preprocess resume and job-description text
- Convert text into numerical representations using TF-IDF
- Calculate textual similarity using cosine similarity
- Display a resume–job match percentage
- Detect matching technical skills
- Detect skills from the job description that were not detected in the resume
- Generate basic resume-tailoring recommendations
- Display technical details of the NLP pipeline
- Handle invalid or unreadable PDF input

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **PyPDF2**
- **scikit-learn**
- **TF-IDF**
- **Cosine Similarity**
- **Regular Expressions**

---

## 🧠 How It Works

The application follows this pipeline:

```text
Resume PDF
    │
    ▼
PDF Text Extraction
    │
    ▼
Text Preprocessing
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Resume Vector
    │
    ├───────────────┐
    │               │
    ▼               ▼
Cosine Similarity   Skill Extraction
    │               │
    ▼               ▼
Match Score     Matching / Missing Skills
                    │
                    ▼
              Recommendations
```

---

## 📐 Architecture

```text
┌───────────────────────┐
│       User            │
└───────────┬───────────┘
            │
            │ Upload PDF
            │ Paste Job Description
            ▼
┌───────────────────────┐
│     Streamlit UI      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   PDF Text Extraction │
│        PyPDF2         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    Text Cleaning      │
│   Regex + Normalize   │
└───────────┬───────────┘
            │
            ├─────────────────────┐
            │                     │
            ▼                     ▼
┌───────────────────────┐ ┌───────────────────────┐
│     TF-IDF            │ │    Skill Extraction   │
│     Vectorizer        │ │  Predefined Skills    │
└───────────┬───────────┘ └───────────┬───────────┘
            │                         │
            ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐
│ Cosine Similarity     │ │ Matching / Missing    │
└───────────┬───────────┘ │ Skills                │
            │             └───────────┬───────────┘
            ▼                         │
┌───────────────────────┐             │
│ Resume Match Score    │             │
└───────────┬───────────┘             │
            │                         │
            └────────────┬────────────┘
                         ▼
              ┌───────────────────────┐
              │ Recommendations       │
              └───────────────────────┘
```

---

## 📊 Example Output

The application produces results such as:

```text
Resume Match
67.4%

Matching Skills
✓ Python
✓ Java
✓ Spring Boot
✓ REST APIs
✓ Docker

Missing Skills
⚠ AWS
⚠ Kubernetes
⚠ Redis

Recommendations
• Review the skills missing from the target job description.
• Highlight relevant backend experience more prominently.
• Only add skills that you genuinely possess.
```

The actual results depend on the uploaded resume and target job description.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ResumeAI.git
cd ResumeAI
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
ResumeAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
```

---

## 🔬 Machine Learning Approach

### TF-IDF

TF-IDF converts text into numerical vectors based on word importance within the provided documents.

It allows the application to represent both the resume and job description mathematically.

### Cosine Similarity

Cosine similarity compares the resulting vectors.

The resulting value is converted into a percentage for the application's textual match score.

Important:

> The match percentage represents textual similarity between the supplied documents. It is not a probability of getting hired and does not represent a candidate's actual qualification.

---

## 🔎 Skill Extraction

The application currently uses a predefined skill vocabulary containing technologies and concepts such as:

- Python
- Java
- SQL
- Spring Boot
- REST APIs
- React
- Docker
- AWS
- Kubernetes
- MySQL
- Machine Learning
- Deep Learning
- NLP
- PyTorch
- Git

Skills detected in both documents are displayed as matching skills.

Skills detected in the job description but not in the resume are displayed as potential missing skills.

---

## ⚠️ Limitations

- PDF text extraction may be imperfect for highly designed or image-based resumes.
- Skill extraction currently depends on a predefined vocabulary.
- The similarity score measures textual similarity rather than actual hiring suitability.
- The system does not understand context as deeply as modern language models.
- Synonyms and related concepts may not always be recognized as equivalent.
- Recommendations are rule-based rather than generated by a large language model.

---

## 🔮 Future Improvements

Possible future improvements include:

- OCR support for scanned resumes
- Named Entity Recognition for dynamic skill extraction
- Sentence embeddings for semantic similarity
- LLM-powered resume recommendations
- Job-specific resume bullet suggestions
- Experience and education section analysis
- Resume section classification
- Support for DOCX resumes
- Resume version comparison
- Exportable analysis reports
- More comprehensive skill taxonomy

---

## 🎯 Learning Outcomes

This project demonstrates practical understanding of:

- Python
- NLP preprocessing
- Regular expressions
- TF-IDF
- Cosine similarity
- Basic information retrieval
- Streamlit application development
- PDF text extraction
- Rule-based skill extraction
- Git/GitHub
- Application deployment

---

## 👨‍💻 Author

**Aman Choudhary**

MCA — Artificial Intelligence & Machine Learning

---

## 📄 Disclaimer

ResumeAI is an educational/portfolio project.

Its similarity score should not be interpreted as a prediction of hiring outcomes or as an objective assessment of candidate suitability.