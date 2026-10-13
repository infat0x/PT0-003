import re
import json

with open("extracted_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Pattern to match questions
pattern = r'Question (\d+)\n(.*?)(?=Correct Answer: ([A-D]))'

questions = []
matches = re.findall(pattern, text, re.DOTALL)

for match in matches:
    q_num = int(match[0])
    q_text = match[1].strip()
    correct = match[2].strip()

    # Skip HOTSPOT and SIMULATION questions
    if 'HOTSPOT' in q_text or 'SIMULATION' in q_text:
        continue

    # Parse question text and options
    lines = q_text.split('\n')

    # Find where options start
    question_text = []
    options = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Check if line starts with A., B., C., D.
        if re.match(r'^[A-D]\.', line):
            opt_letter = line[0]
            opt_text = line[2:].strip()
            options[opt_letter] = opt_text
        else:
            if not options:  # Still in question text
                question_text.append(line)

    full_question = ' '.join(question_text)

    # Only add if we have all 4 options
    if len(options) >= 4:
        questions.append({
            "id": q_num,
            "question": full_question,
            "options": options,
            "correct": correct
        })

print(f"Parsed {len(questions)} questions")

# Save to JSON
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("Saved to questions.json")

# Print first 3 questions as sample
print("\n--- Sample Questions ---")
for q in questions[:3]:
    print(f"\nQ{q['id']}: {q['question'][:100]}...")
    print(f"Options: {list(q['options'].keys())}")
    print(f"Correct: {q['correct']}")
