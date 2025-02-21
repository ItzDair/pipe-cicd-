import os
import openai
import glob
import logging
import time

logging.basicConfig(level=logging.INFO)

# Ensure API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

client = openai.OpenAI()

def get_all_files():
    """Fetch all Python files in the project, avoiding large and unnecessary files."""
    ignore_dirs = {".git", ".venv", "__pycache__"}
    files = []
    for root, _, filenames in os.walk("."):
        if any(ignored in root for ignored in ignore_dirs):
            continue
        for filename in filenames:
            if filename.endswith(".py") and os.path.getsize(os.path.join(root, filename)) < 500_000:
                files.append(os.path.join(root, filename))
    
    content = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content[file] = f.read()

    return content

def full_project_review(files):
    """Send all project files to OpenAI for analysis, splitting into chunks."""
    reviews = []
    for file, content in files.items():
        prompt = f"Review this Python file and provide detailed feedback:\n{file}\n\n{content}"
        retries = 3
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior software architect."},
                        {"role": "user", "content": prompt}
                    ]
                )
                reviews.append(f"### {file} ###\n{response.choices[0].message.content}")
                break
            except openai.APIError as e:
                logging.error(f"OpenAI API error: {e}, attempt {attempt + 1} of {retries}")
                time.sleep(2 ** attempt)
    
    return "\n".join(reviews) if reviews else "Review failed due to API error."

if __name__ == "__main__":
    files = get_all_files()
    if not files:
        print("No files found.")
    else:
        review = full_project_review(files)
        print("Full Project Review:\n", review)

