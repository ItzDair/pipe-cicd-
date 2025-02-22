import os
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def review_project(directory):
    """ Reviews all Python files in a project directory. """
    reviews = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code_content = f.read()

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a code reviewer. Provide detailed analysis."},
                        {"role": "user", "content": f"Review this code:\n```python\n{code_content}\n```"}
                    ]
                )

                reviews[file] = response["choices"][0]["message"]["content"]

    return reviews

if __name__ == "__main__":
    project_path = "."  # Change as needed
    review_results = review_project(project_path)
    print("Project review completed.")
    print(review_results)
