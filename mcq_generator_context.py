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
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def generate_mcq_context(context_messages=[], model="gpt-4o"):
    """
    Generate a single topic and MCQ, passing prior messages as context.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=context_messages,
            temperature=0,
            top_p=0,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {e}"

if __name__ == "__main__":
    # Load consent text
    with open("consents/cysto_consent.txt", "r", encoding="utf-8") as file:
        consent_text = file.read()

    # Load prompt template
    prompt_template_init = load_prompt_template("prompts/mcq_prompt_context.txt")
    prompt_template_init = prompt_template_init.format(consent_text=consent_text)

    prompt_template_followup = load_prompt_template("prompts/mcq_prompt_context_followup.txt")

    output_path = "output_context/MCQs_output_context_3.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    context_messages = []
    context_messages = [{"role": "system", "content": "You are a helpful assistant that writes patient education questions."}]
    
    total_questions = 10
    full_output = ""

    # Initial prompt
    context_messages.append({"role": "user", "content": prompt_template_init})
    mcq = generate_mcq_context(context_messages=context_messages)
    full_output += f"{mcq}"
    # Store this as part of context for the next round
    context_messages.append({"role": "assistant", "content": mcq})
    
    for i in range(total_questions):
        context_messages.append({"role": "user", "content": prompt_template_followup})
        mcq = generate_mcq_context(context_messages=context_messages)
        full_output += f"\n\n=== MCQ {i+1} ===\n{mcq}"

        # Store this as part of context for the next round
        context_messages.append({"role": "assistant", "content": mcq})

    # Save final result
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_output)

    print(f"\nDone! Saved {total_questions} contextual MCQs to '{output_path}'.")
