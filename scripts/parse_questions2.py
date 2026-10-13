import re
import json

with open("extracted_text2.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Pattern to match questions in this format: Question #:1 - [Category]
# Split by question markers
question_blocks = re.split(r'Question #:(\d+)', text)[1:]  # Skip header

questions = []
i = 0
while i < len(question_blocks) - 1:
    q_num = int(question_blocks[i])
    q_content = question_blocks[i + 1]

    # Find the answer line - only capture letters right after "Answer:"
    answer_match = re.search(r'\nAnswer:\s*([A-F](?:\s*[A-F])*)\s*\n', q_content)
    if not answer_match:
        i += 2
        continue

    # Parse correct answers - split by whitespace
    answer_text = answer_match.group(1).strip()
    correct_answers = answer_text.split()

    # Get question text (everything before Answer:)
    q_text_part = q_content[:answer_match.start()]

    # Extract category if present
    category_match = re.search(r'\[([^\]]+)\]', q_text_part)
    category = category_match.group(1) if category_match else ""

    # Remove category from question text
    if category_match:
        q_text_part = q_text_part[category_match.end():]

    # Parse question and options
    lines = q_text_part.strip().split('\n')

    question_text = []
    options = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip page markers
        if 'Pass Your Certification' in line or 'Practice Test CompTIA' in line:
            continue
        # Check for options A-F
        opt_match = re.match(r'^([A-F])\.\s*(.+)$', line)
        if opt_match:
            opt_letter = opt_match.group(1)
            opt_text = opt_match.group(2).strip()
            if opt_text:  # Only add if there's actual text
                options[opt_letter] = opt_text
        else:
            # If we haven't started options yet, it's question text
            if not options:
                question_text.append(line)

    full_question = ' '.join(question_text).strip()

    # Clean up question text
    full_question = re.sub(r'\s+', ' ', full_question)

    # Only add valid questions with at least 2 options
    if len(options) >= 2 and full_question:
        questions.append({
            "id": q_num,
            "question": full_question,
            "options": options,
            "correct": correct_answers,  # Can be multiple for "Select two" questions
            "category": category
        })

    i += 2

print(f"Parsed {len(questions)} questions")

# Save to JSON
with open("questions2.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("Saved to questions2.json")

# Print first 5 questions as sample
print("\n--- Sample Questions ---")
for q in questions[:5]:
    print(f"\nQ{q['id']} [{q['category']}]: {q['question'][:80]}...")
    print(f"Options: {list(q['options'].keys())}")
    print(f"Correct: {q['correct']}")

# Count questions with multiple correct answers
multi = sum(1 for q in questions if len(q['correct']) > 1)
print(f"\nQuestions with multiple correct answers: {multi}")
