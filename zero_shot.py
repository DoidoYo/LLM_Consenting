import openai
import time

# Set your OpenAI API key
openai.api_key = "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"

def generate_mcq(consent_text, topic, tag, model="gpt-4"):
    prompt = f"""
You are a urologist writing a multiple-choice question (MCQ) to test patient understanding of a medical procedure. Use only the information contained in the consent text below.

CONSENT:
\"\"\"
{consent_text}
\"\"\"

Please generate ONE multiple-choice question about the following topic: **{topic}**.

Instructions:
- Provide exactly four answer choices (A–D).
- There should be only one correct answer.
- Use only information from the consent text — do not add new facts or assumptions.
- The question should be clear, concise, and patient-friendly (8th-grade reading level).
- End with the correct answer letter and a brief rationale explaining why.

Output Format:
**Topic**: {tag}
**Question**: ...
A) ...
B) ...
C) ...
D) ...
**Answer**: [Letter]
**Rationale**: ...
"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes patient education questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"[ERROR] {e}"

def generate_multiple_mcqs(consent_text, topic, tag, num_questions=10):
    results = []
    for i in range(num_questions):
        print(f"Generating question {i + 1}/{num_questions}...")
        mcq = generate_mcq(consent_text, topic, tag)
        results.append(mcq)
        time.sleep(1.5)  # rate limiting buffer
    return results

if __name__ == "__main__":
    # === Replace with your own values ===
    consent_text = "The risks of cystoscopy include bleeding, infection, and discomfort during urination."
    topic = "Risks of cystoscopy"
    tag = "RSK"
    num_questions = 10

    mcqs = generate_multiple_mcqs(consent_text, topic, tag, num_questions)
    
    output_file = "mcqs_output.txt"
    with open(output_file, "w") as f:
        for i, mcq in enumerate(mcqs):
            f.write(f"--- Question {i+1} ---\n{mcq}\n\n")

    print(f"\n✅ Done! Saved {num_questions} MCQs to '{output_file}'")
