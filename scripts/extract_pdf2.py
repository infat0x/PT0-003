import pdfplumber

pdf_path = r"c:\Users\infat\Documents\codes\question\CompTIA-PT0-003.pdf"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Save raw text for inspection
with open("extracted_text2.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"PDF extracted successfully!")
print(f"Total characters: {len(full_text)}")
print(f"Saved to extracted_text2.txt")
print("\n--- First 3000 characters preview ---\n")
print(full_text[:3000])
