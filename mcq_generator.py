import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MY_API_KEY = os.getenv("OPENAI_API_KEY")

if not MY_API_KEY:
    raise EnvironmentError("Missing OPENAI_API_KEY in environment.")

client = openai.OpenAI(api_key=MY_API_KEY)

def load_prompt_template(filename):
    """
    Load the MCQ generation prompt template from a file.
    The file should contain a '{consent_text}' placeholder.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def generate_mcq(prompt_template, consent_text, model="gpt-4o"):
    """
    Generate multiple-choice questions from a given consent text using a prompt template.
    """
    prompt = prompt_template.format(consent_text=consent_text)

    try:
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

def load_topics_from_file(filename):
    """
    Load topics from a file in the format: Tag - Description
    """
    topics = []
    with open(filename, "r") as file:
        for line in file:
            if "-" in line:
                tag, description = line.strip().split("-", 1)
                topics.append((tag.strip(), description.strip()))
    return topics

if __name__ == "__main__":
    # Load consent text
    with open("consents/cysto_consent.txt", "r", encoding="utf-8") as file:
        consent_text = file.read()

    # Load prompt template
    prompt_template = load_prompt_template("prompts/mcq_prompt.txt")

    # load topic
    # topics = load_topics_from_file("topics.txt")

    # Generate MCQs
    mcqs = generate_mcq(prompt_template, consent_text)

    # Save output
    output_path = "output/MCQs_output_notopic_3.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mcqs)

    print(f"\nDone! Saved MCQ output to '{output_path}'.")
