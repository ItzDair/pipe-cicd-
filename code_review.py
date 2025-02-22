import os
import json
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Ensure it's set in the .env file.")

# Create an OpenAI client without passing `api_key` directly
client = openai.Client(api_key=api_key)

def review_code(file_path):
    """Reads a code file and sends it for review to OpenAI API."""
    with open(file_path, "r") as file:
        code_content = file.read()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if needed
        messages=[
            {"role": "system", "content": "You are an expert code reviewer. Provide a detailed analysis of the following code."},
            {"role": "user", "content": f"Review this code:\n```python\n{code_content}\n```"}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

def save_review_results(file_path, review):
    """Saves the review results in a JSON file."""
    results = {file_path: review}
    with open("code_reviews.json", "w") as json_file:
        json.dump(results, json_file, indent=4)

if __name__ == "__main__":
    code_file = "some_code.py"  # Ensure this file exists!
    review = review_code(code_file)
    save_review_results(code_file, review)
    print(f"Review saved for {code_file}")
