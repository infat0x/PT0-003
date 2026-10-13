import pdfplumber
import json
import re

pdf_path = r"c:\Users\infat\Documents\codes\question\PT0-003_Premium File 307 Questions & Answers. Last Update Oct 16, 2025.pdf"

questions = []
current_question = None

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Save raw text for inspection
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"PDF extracted successfully!")
print(f"Total characters: {len(full_text)}")
print(f"Saved to extracted_text.txt")
print("\n--- First 3000 characters preview ---\n")
print(full_text[:3000])
