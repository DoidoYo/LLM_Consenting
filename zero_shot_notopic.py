import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_mcq(consent_text, topic_name="", topic_description="", model="gpt-4o"):
    prompt = f"""
You are a urologist writing a multiple-choice question (MCQ) to test patient understanding of a medical procedure. Use only the information contained in the consent text below.

CONSENT:
\"\"\"
{consent_text}
\"\"\"

Please generate topics which you think are relevant. For each topic, generate THREE multiple-choice question.

Instructions:
- Questions should be different from each other.
- Provide exactly four answer choices (A–D).
- There should be only one correct answer.
- Use only information from the consent text — do not add new facts or assumptions.
- The question should be clear, concise, and patient-friendly (8th-grade reading level).
- End with the correct answer letter and a brief rationale explaining why.

Output Format:
**Topics: **
1) ...
*Rationale* ...
2) ...
*Rationale* ...
so on...

** Topic **: ...
**Question**: ...
A) ...
B) ...
C) ...
D) ...
**Answer**: [Letter]
**Rationale**: ...

so on...
"""
    try:

        client = openai.OpenAI(api_key=MY_API_KEY)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes patient education questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            top_p=0,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {e}"



#load topics
def load_topics_from_file(filename="topics.txt"):
    topics = []
    with open(filename, "r") as file:
        for line in file:
            if "-" in line:
                tag, description = line.strip().split("-", 1)
                topics.append((tag.strip(), description.strip()))
    return topics

def generate_mcqs(consent_text, number_of_questions=1):
    results = []
    # for topic_name, topic_description in TOPICS:

    for i in range(number_of_questions):
        print(f"Generating question {i + 1}/{number_of_questions}...")
        mcq = generate_mcq(consent_text)
        results.append(f"--- (Q{i+1}) ---\n{mcq}\n")
        time.sleep(1.5)  # rate limit protection
    return results

if __name__ == "__main__":
 
    with open("consents/cysto_consent.txt", "r", encoding="utf-8") as file:
        CONSENT_TEXT = file.read()

    TOPICS = load_topics_from_file("topics.txt")
    number_of_questions = 1

    mcqs = generate_mcqs(CONSENT_TEXT, number_of_questions)

    output_file = "MCQs_output_notopic_three.txt"
    with open(output_file, "w") as f:
        for mcq in mcqs:
            f.write(mcq + "\n")

    print(f"\nDone! Saved {len(mcqs)} MCQs to '{output_file}'")  
