import os
import openai
import git
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_commit_diff(repo_path, commit_hash):
    """ Get the diff of a specific commit. """
    repo = git.Repo(repo_path)
    commit = repo.commit(commit_hash)
    return commit.diff(commit.parents[0]).patch

def review_commit(repo_path, commit_hash):
    """ Reviews changes in a given commit. """
    diff = get_commit_diff(repo_path, commit_hash)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a code review assistant. Analyze commit changes."},
            {"role": "user", "content": f"Review this commit diff:\n```diff\n{diff}\n```"}
        ]
    )

    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    repo_path = "."  # Change if needed
    commit_hash = "HEAD"  # Replace with actual commit hash
    review = review_commit(repo_path, commit_hash)
    print("Review for commit:", commit_hash)
    print(review)
