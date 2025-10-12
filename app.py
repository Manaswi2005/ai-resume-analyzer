import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path
import pytesseract
import pdfplumber
from docx import Document

# -------------------------------------------
# Load API Key
# -------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------------------
# ✅ Function: Extract text from file (PDF, DOCX, Image)
# -------------------------------------------
def extract_text_from_file(file_path):
    text = ""
    ext = os.path.splitext(file_path)[-1].lower()

    # --- 1️⃣ PDF ---
    if ext == ".pdf":
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                print(" Extracted text from PDF using pdfplumber.")
                return text.strip()
        except Exception as e:
            print(f" Direct text extraction failed: {e}")

        # Fallback: OCR for scanned PDF
        print(" Using OCR for image-based PDF...")
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                gray = image.convert("L")
                page_text = pytesseract.image_to_string(gray)
                text += f"\n\n--- Page {i+1} ---\n{page_text}"
            print(" Extracted text using OCR.")
        except Exception as e:
            print(f" OCR extraction failed: {e}")

    # --- 2️⃣ Word Document (.docx) ---
    elif ext == ".docx":
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            print(" Extracted text from Word file.")
        except Exception as e:
            print(f" Word extraction failed: {e}")

    # --- 3️⃣ Image (JPG, JPEG, PNG) ---
    elif ext in [".jpg", ".jpeg", ".png"]:
        try:
            image = Image.open(file_path)
            gray = image.convert("L")
            text = pytesseract.image_to_string(gray)
            print(" Extracted text from image using OCR.")
        except Exception as e:
            print(f" Image OCR failed: {e}")

    else:
        print(" Unsupported file type. Please upload PDF, DOCX, or image files.")

    return text.strip()


# -------------------------------------------
# ✅ Function: Analyze Resume using Gemini AI
# -------------------------------------------
def analyze_resume(resume_text, job_description=None):
    if not resume_text:
        return " No text could be extracted from the file."

    model = genai.GenerativeModel("models/gemini-2.5-pro")

    base_prompt = f"""
    You are an experienced HR professional skilled in Data Science, DevOps, AI Engineering, and Software Development.

    Analyze the following resume text and provide:
    - Strengths and weaknesses
    - Key skills
    - Skills to improve
    - Recommended certifications or courses
    - Overall job readiness

    Resume:
    {resume_text}
    """

    if job_description:
        base_prompt += f"""
        Additionally, compare it with this job description:

        Job Description:
        {job_description}

        Describe how well it matches the role and what can be improved.
        """

    try:
        response = model.generate_content(base_prompt)
        return response.text.strip()
    except Exception as e:
        return f" Gemini AI analysis failed: {e}"


# -------------------------------------------
# ✅ Streamlit UI
# -------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title(" AI Resume Analyzer")
st.write("Upload your resume (PDF, Word, or Image) and let Google Gemini AI evaluate it!")

# Upload + Job Description
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "jpg", "jpeg", "png"]
    )
with col2:
    job_description = st.text_area(
        "Enter Job Description (optional):",
        placeholder="Paste the job description here..."
    )

# Process
if uploaded_file:
    # Save uploaded file
    ext = os.path.splitext(uploaded_file.name)[-1]
    save_path = f"uploaded_resume{ext}"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f" File '{uploaded_file.name}' uploaded successfully!")

    with st.spinner("Extracting text..."):
        resume_text = extract_text_from_file(save_path)

    if resume_text:
        st.text_area(" Extracted Resume Text (Preview):", resume_text[:1500], height=250)
    else:
        st.error(" Could not extract any text from the file.")

    if st.button(" Analyze Resume"):
        with st.spinner("Analyzing resume using Gemini AI..."):
            analysis = analyze_resume(resume_text, job_description)
            st.success(" Analysis Complete!")
            st.write(analysis)
else:
    st.warning("Please upload a resume in PDF, DOCX, or image format.")

# Footer
st.markdown("---")
st.markdown(
    """<p style='text-align: center;'>
    Powered by <b>Streamlit</b> + <b>Google Gemini AI</b> | Developed by <b>You 🚀</b>
    </p>""",
    unsafe_allow_html=True,
)
