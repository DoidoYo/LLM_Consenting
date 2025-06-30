import openai
import time
import os
from dotenv import load_dotenv

# Set your OpenAI API key
# Load environment variables from .env file
load_dotenv()

MY_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_mcq(consent_text, topic_name, topic_description, model="gpt-4"):
    prompt = f"""
You are a urologist writing a multiple-choice question (MCQ) to test patient understanding of a medical procedure. Use only the information contained in the consent text below.

CONSENT:
\"\"\"
{consent_text}
\"\"\"

Please generate ONE multiple-choice question.

Instructions:
- Provide exactly four answer choices (A–D).
- There should be only one correct answer.
- Use only information from the consent text — do not add new facts or assumptions.
- The question should be clear, concise, and patient-friendly (8th-grade reading level).
- End with the correct answer letter and a brief rationale explaining why.

Output Format:
**Question**: ...
A) ...
B) ...
C) ...
D) ...
**Answer**: [Letter]
**Rationale**: ...
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
            max_tokens=300
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

def generate_mcqs_by_topic(consent_text, questions_per_topic=1):
    results = []
    for topic_name, topic_description in TOPICS:
        for i in range(questions_per_topic):
            print(f"Generating '{topic_name}' question {i + 1}/{questions_per_topic}...")
            mcq = generate_mcq(consent_text, topic_name, topic_description)
            results.append(f"--- {topic_name} (Q{i+1}) ---\n{mcq}\n")
            time.sleep(1.5)  # rate limit protection
    return results

if __name__ == "__main__":
 
    with open("consents/cysto_consent.txt", "r", encoding="utf-8") as file:
        CONSENT_TEXT = file.read()

    TOPICS = load_topics_from_file("topics.txt")
    QUESTIONS_PER_TOPIC = 1

    mcqs = generate_mcqs_by_topic(CONSENT_TEXT, QUESTIONS_PER_TOPIC)

    output_file = "mcqs_by_topic_output.txt"
    with open(output_file, "w") as f:
        for mcq in mcqs:
            f.write(mcq + "\n")

    print(f"\nDone! Saved {len(mcqs)} MCQs to '{output_file}'")  
