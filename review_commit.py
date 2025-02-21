import os
import openai
import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO)

# Load API Key with proper error handling
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

client = openai.OpenAI()

def get_git_diff():
    """Fetch the latest commit diff with error handling."""
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing git diff: {e}")
        return ""

def review_commit(diff_text):
    """Send the git diff to OpenAI for analysis."""
    if not diff_text:
        return "No changes detected."

    prompt = f"Review the following code changes and provide comments:\n{diff_text}"
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior code reviewer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}, attempt {attempt + 1} of {retries}")
            time.sleep(2 ** attempt)

    return "Review failed due to API error."

if __name__ == "__main__":
    diff = get_git_diff()
    review = review_commit(diff)
    print("Review Comments:\n", review)

