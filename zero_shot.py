import openai
import time

# Set your OpenAI API key
MY_API_KEY = "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"

def generate_mcq(consent_text, topic_name, topic_description, model="gpt-4"):
    prompt = f"""
You are a urologist writing a multiple-choice question (MCQ) to test patient understanding of a medical procedure. Use only the information contained in the consent text below.

CONSENT:
\"\"\"
{consent_text}
\"\"\"

Please generate ONE multiple-choice question about the following topic: **{topic_name} - {topic_description}**.

Instructions:
- Provide exactly four answer choices (A–D).
- There should be only one correct answer.
- Use only information from the consent text — do not add new facts or assumptions.
- The question should be clear, concise, and patient-friendly (8th-grade reading level).
- End with the correct answer letter and a brief rationale explaining why.

Output Format:
**Topic**: {topic_name}
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
    # === Replace with your own values ===

    CONSENT_TEXT = ""
    TOPICS = load_topics_from_file("topics.txt")

    consent_text = "The risks of cystoscopy include bleeding, infection, and discomfort during urination."
    QUESTIONS_PER_TOPIC = 1

    mcqs = generate_mcqs_by_topic(consent_text, QUESTIONS_PER_TOPIC)

    output_file = "mcqs_by_topic_output.txt"
    with open(output_file, "w") as f:
        for mcq in mcqs:
            f.write(mcq + "\n")

    print(f"\n✅ Done! Saved {len(mcqs)} MCQs to '{output_file}'")  
