
from docx import Document

doc = Document('testTask/AI Internship Test Assignment 2026.docx')
for para in doc.paragraphs:
    if para.text.strip():
        print(para.text)
