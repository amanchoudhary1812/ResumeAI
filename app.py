import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = {
    # Programming Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "ruby",
    "php",
    "kotlin",
    "swift",

    # Web / Frontend
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "next.js",
    "bootstrap",
    "tailwind",

    # Backend
    "spring",
    "spring boot",
    "node.js",
    "express",
    "django",
    "flask",
    "fastapi",
    "rest api",
    "rest apis",
    "graphql",
    "microservices",
    "multithreading",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "redis",
    "oracle",
    "sqlite",
    "database",
    "databases",

    # Cloud / DevOps
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "jenkins",
    "terraform",
    "ci/cd",
    "linux",

    # Data / AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "ml",
    "nlp",
    "computer vision",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "bert",
    "resnet",

    # Analytics
    "power bi",
    "tableau",
    "excel",
    "mixpanel",
    "product analytics",
    "a/b testing",
    "ab testing",
    "cohort analysis",
    "funnel analysis",

    # Software Engineering
    "data structures",
    "algorithms",
    "object oriented programming",
    "oops",
    "dbms",
    "operating systems",
    "computer networks",
    "git",
    "github",
    "jira",
    "agile",
    "junit",
    "postman"
}


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_file):
    """
    Extract text from all pages of a PDF.
    """

    try:
        reader = PdfReader(pdf_file)

        if len(reader.pages) == 0:
            return ""

        text_parts = []

        for page in reader.pages:
            try:
                page_text = page.extract_text()

                if page_text:
                    text_parts.append(page_text)

            except Exception:
                continue

        return "\n".join(text_parts)

    except Exception:
        return ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Clean text for NLP processing.
    """

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Remove email addresses
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # Replace common separators with spaces
    text = text.replace("|", " ")
    text = text.replace("/", " ")
    text = text.replace("-", " ")

    # Keep letters, numbers and spaces
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):
    """
    Detect known skills from text.
    """

    text_lower = text.lower()

    detected_skills = set()

    # Sort longest skills first so multi-word skills
    # are checked before shorter words.
    sorted_skills = sorted(
        SKILLS,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):
            detected_skills.add(skill)

    return detected_skills


# ============================================================
# BASIC KEYWORD EXTRACTION
# ============================================================

def get_keywords(text):

    stop_words = {
        "the", "and", "a", "an", "to", "of",
        "in", "for", "on", "with", "is", "are",
        "that", "this", "as", "by", "from",
        "at", "be", "or", "it", "their", "they",
        "we", "our", "will", "can", "has", "have",
        "into", "using", "used", "work", "working",
        "role", "job", "candidate", "experience",
        "looking", "including", "required"
    }

    words = text.split()

    keywords = {
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
        and not word.isdigit()
    }

    return keywords


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    matching_skills,
    missing_skills,
    match_percentage
):

    recommendations = []

    if missing_skills:
        top_missing = sorted(missing_skills)[:8]

        recommendations.append(
            "Review the job description for these skills "
            "that were not detected in your resume: "
            + ", ".join(top_missing)
            + "."
        )

    if match_percentage < 50:
        recommendations.append(
            "The textual similarity is relatively low for "
            "this job description. Consider tailoring your "
            "resume summary and relevant project descriptions "
            "to the target role."
        )

    elif match_percentage < 75:
        recommendations.append(
            "There is moderate textual alignment. Consider "
            "highlighting the most relevant experience and "
            "technical skills for this particular role."
        )

    else:
        recommendations.append(
            "The resume has strong textual alignment with "
            "the supplied job description. Make sure the "
            "most relevant skills and achievements are easy "
            "to find."
        )

    if matching_skills:
        recommendations.append(
            "Your resume already contains relevant skills such as "
            + ", ".join(sorted(matching_skills)[:6])
            + "."
        )

    recommendations.append(
        "Only add a skill to your resume if you genuinely "
        "have experience or knowledge of it."
    )

    return recommendations


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 10px 0 20px 0;
    ">
        <h1>📄 ResumeAI</h1>
        <p style="font-size: 18px;">
            AI-powered resume and job description analyzer
        </p>
        <p style="color: #777;">
            Analyze resume-job similarity, identify relevant skills,
            and discover potential gaps.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

left_col, right_col = st.columns(2)

with left_col:

    st.subheader("📄 Resume")

    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload a text-based PDF resume."
    )

with right_col:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the target job description",
        height=220,
        placeholder=(
            "Example:\n"
            "We are looking for a backend engineer "
            "with experience in Java, Spring Boot, "
            "REST APIs, SQL and Docker..."
        )
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not resume_file:

        st.warning(
            "Please upload your resume PDF."
        )
        st.stop()

    if not job_description.strip():

        st.warning(
            "Please paste a job description."
        )
        st.stop()

    # --------------------------------------------------------
    # EXTRACT RESUME TEXT
    # --------------------------------------------------------

    with st.spinner("Reading your resume..."):

        resume_text = extract_text_from_pdf(
            resume_file
        )

    if not resume_text.strip():

        st.error(
            "No readable text could be extracted from "
            "this PDF. Please upload a text-based PDF."
        )
        st.stop()

    # --------------------------------------------------------
    # CLEAN TEXT
    # --------------------------------------------------------

    cleaned_resume_text = clean_text(
        resume_text
    )

    cleaned_job_description = clean_text(
        job_description
    )

    if not cleaned_resume_text:

        st.error(
            "The resume text could not be processed."
        )
        st.stop()

    if not cleaned_job_description:

        st.error(
            "The job description could not be processed."
        )
        st.stop()

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        [
            cleaned_resume_text,
            cleaned_job_description
        ]
    )

    # --------------------------------------------------------
    # COSINE SIMILARITY
    # --------------------------------------------------------

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    match_percentage = similarity[0][0] * 100

    # --------------------------------------------------------
    # SKILL EXTRACTION
    # --------------------------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matching_skills = (
        resume_skills & job_skills
    )

    missing_skills = (
        job_skills - resume_skills
    )

    # --------------------------------------------------------
    # BASIC KEYWORDS
    # --------------------------------------------------------

    resume_keywords = get_keywords(
        cleaned_resume_text
    )

    job_keywords = get_keywords(
        cleaned_job_description
    )

    matching_keywords = (
        resume_keywords & job_keywords
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        matching_skills,
        missing_skills,
        match_percentage
    )

    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.subheader("📊 Analysis Result")

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        st.metric(
            "Resume Match",
            f"{match_percentage:.1f}%"
        )

    with score_col2:

        st.metric(
            "Matching Skills",
            len(matching_skills)
        )

    with score_col3:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )

    # --------------------------------------------------------
    # SCORE PROGRESS BAR
    # --------------------------------------------------------

    st.markdown("### Match Score")

    st.progress(
        min(match_percentage / 100, 1.0)
    )

    if match_percentage < 40:

        st.caption(
            "Low textual similarity based on the supplied "
            "resume and job description."
        )

    elif match_percentage < 70:

        st.caption(
            "Moderate textual similarity based on the "
            "supplied resume and job description."
        )

    else:

        st.caption(
            "High textual similarity based on the supplied "
            "resume and job description."
        )

    # ========================================================
    # SKILLS
    # ========================================================

    st.divider()

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:

        st.subheader("✅ Matching Skills")

        if matching_skills:

            for skill in sorted(
                matching_skills
            ):
                st.markdown(
                    f"- **{skill}**"
                )

        else:

            st.info(
                "No skills from the predefined skill "
                "database were detected in both documents."
            )

    with skill_col2:

        st.subheader("⚠️ Missing Skills")

        if missing_skills:

            for skill in sorted(
                missing_skills
            ):
                st.markdown(
                    f"- **{skill}**"
                )

        else:

            st.success(
                "No missing skills were detected from "
                "the predefined skill database."
            )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader("💡 Resume Recommendations")

    for recommendation in recommendations:

        st.markdown(
            f"- {recommendation}"
        )

    # ========================================================
    # BASIC KEYWORDS
    # ========================================================

    st.divider()

    st.subheader("🔎 Keyword Analysis")

    keyword_col1, keyword_col2 = st.columns(2)

    with keyword_col1:

        st.write(
            f"**Matching words:** "
            f"{len(matching_keywords)}"
        )

        if matching_keywords:

            st.write(
                ", ".join(
                    sorted(matching_keywords)
                )
            )

    with keyword_col2:

        st.write(
            f"**Job-specific words not found in resume:** "
            f"{len(job_keywords - resume_keywords)}"
        )

        missing_keywords = (
            job_keywords - resume_keywords
        )

        if missing_keywords:

            st.write(
                ", ".join(
                    sorted(missing_keywords)
                )
            )

    # ========================================================
    # TECHNICAL DETAILS
    # ========================================================

    st.divider()

    with st.expander("🧠 How the analysis works"):

        st.markdown(
            """
            **1. PDF text extraction**

            PyPDF2 extracts readable text from the uploaded PDF.

            **2. Text preprocessing**

            URLs, email addresses, punctuation and unnecessary
            whitespace are removed and text is normalized.

            **3. TF-IDF**

            The resume and job description are converted into
            numerical vectors using TF-IDF.

            **4. Cosine similarity**

            The two vectors are compared using cosine similarity
            to produce the textual match percentage.

            **5. Skill extraction**

            The application checks both documents against a
            predefined technical skill vocabulary.

            **6. Recommendations**

            The application identifies detected skill gaps and
            provides basic resume-tailoring suggestions.
            """
        )

        st.write(
            f"TF-IDF vocabulary size: "
            f"{len(vectorizer.get_feature_names_out())}"
        )

    # ========================================================
    # RAW RESUME
    # ========================================================

    with st.expander("📄 View extracted resume text"):

        st.text(resume_text)

    with st.expander("🧹 View cleaned resume text"):

        st.text(cleaned_resume_text)

    with st.expander("💼 View cleaned job description"):

        st.text(cleaned_job_description)