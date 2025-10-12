import os
from PIL import Image
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from docx import Document
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_file(file_path):
    text = ""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                print("✅ Extracted text using pdfplumber.")
                return text.strip()
        except Exception as e:
            print(f"⚠️ PDF extraction failed: {e}")
        print("⚙️ Trying OCR for scanned PDF...")
        images = convert_from_path(file_path)
        for img in images:
            gray = img.convert("L")
            text += pytesseract.image_to_string(gray)
        print("✅ Extracted text using OCR.")

    elif ext == ".docx":
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        print("✅ Extracted text from Word file.")

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(file_path)
        gray = img.convert("L")
        text = pytesseract.image_to_string(gray)
        print("✅ Extracted text from image using OCR.")

    else:
        print("❌ Unsupported file type.")

    return text.strip()

# 🔍 Test with your file (edit file name)
file_path = "Resume.jpg"  # or Resume.pdf / Resume.docx
text = extract_text_from_file(file_path)
print("\n📝 Extracted Text:\n", "-" * 60)
print(text[:1500] if text else "❌ No text found.")
