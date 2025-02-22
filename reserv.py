# requests==2.31.0
# aiogram==2.25.1
# telethon==1.24.0
# telebot==0.0.5
# python-decouple==3.6
# openai==1.2.0
# httpx==0.24.1
# tiktoken>=0.5.1,<0.6.0


# name: Code Review

# on:
#   pull_request:
#   workflow_dispatch:

# permissions:
#   contents: read
#   pull-requests: write

# jobs:
#   review:
#     runs-on: ubuntu-latest
#     steps:
#       - name: Checkout Repository
#         uses: actions/checkout@v3

#       - name: Set up Python
#         uses: actions/setup-python@v3
#         with:
#           python-version: '3.9'

#       - name: Install dependencies
#         run: pip install -r requirements.txt

#       - name: Run commit review
#         run: python scripts/review_commit.py || echo "Review failed, skipping..."
#         continue-on-error: true  

#       - name: Show review output
#         run: cat review.txt || echo "No review output available."

#       - name: Upload review artifact
#         uses: actions/upload-artifact@v3
#         with:
#           name: commit-review
#           path: review.txt
#         if: success() || failure()

#   test:
#     runs-on: ubuntu-latest
#     steps:
#       - name: Checkout Repository
#         uses: actions/checkout@v3

#       - name: Set up Python
#         uses: actions/setup-python@v3
#         with:
#           python-version: '3.9'

#       - name: Install dependencies
#         run: pip install -r requirements.txt

#       - name: Run tests
#         run: pytest tests



# image: python:3.9

# before_script:
#   - pip install --upgrade pip
#   - pip install -r requirements.txt --cache-dir .cache/pip

# stages:
#   - review
#   - test

# review:
#   stage: review
#   script:
#     - python scripts/review_commit.py > review.txt
#   artifacts:
#     paths:
#       - review.txt
#   only:
#     - merge_requests
#     - branches

# test:
#   stage: test
#   script:
#     - pytest tests/
#   artifacts:
#     paths:
#       - test-results.xml
#   when: always



# import os
# import openai
# import logging
# import time

# logging.basicConfig(level=logging.INFO)

# if not os.getenv("OPENAI_API_KEY"):
#     raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

# client = openai.OpenAI()

# IGNORE_PATTERNS = ["*.log", "*.json", "*.md"]  # ✅ Added file filters
# MAX_FILE_SIZE = 500_000  # ✅ Excludes large files

# def get_all_files():
#     """Fetch all Python files in the project, avoiding unnecessary files."""
#     ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", ".cache", "dist", "build"}
#     files = []
#     for root, _, filenames in os.walk("."):
#         if any(ignored in root for ignored in ignore_dirs):
#             continue
#         for filename in filenames:
#             if filename.endswith(".py") and os.path.getsize(os.path.join(root, filename)) < MAX_FILE_SIZE:
#                 if not any(filename.endswith(pattern) for pattern in IGNORE_PATTERNS):
#                     files.append(os.path.join(root, filename))
    
#     content = {}
#     for file in files:
#         with open(file, "r", encoding="utf-8") as f:
#             content[file] = f.read()

#     return content

# def full_project_review(files):
#     """Send all project files to OpenAI for analysis, splitting into chunks."""
#     reviews = []
#     for file, content in files.items():
#         prompt = f"Review this Python file and provide detailed feedback:\n{file}\n\n{content}"
#         retries = 3
#         for attempt in range(retries):
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4",
#                     messages=[
#                         {"role": "system", "content": "You are a senior software architect."},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 reviews.append(f"### {file} ###\n{response.choices[0].message.content}")
#                 break
#             except openai.APIError as e:
#                 logging.error(f"OpenAI API error: {e}, attempt {attempt + 1} of {retries}")
#                 time.sleep(2 ** attempt)
    
#     return "\n".join(reviews) if reviews else "Review failed due to API error."

# if __name__ == "__main__":
#     files = get_all_files()
#     review = full_project_review(files)
#     with open("full_review.txt", "w") as file:
#         file.write(review)

#     print("Full Project Review:\n", review)




# import os
# import openai
# import subprocess
# import logging
# import time
# import tiktoken

# logging.basicConfig(level=logging.INFO)

# # Ensure OpenAI API key is set
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

# client = openai.OpenAI()

# MAX_TOKENS = 4096  # Ensure consistent token limits
# CHUNK_SIZE = 3000  # Adjusted for better chunking

# def truncate_content(content, max_tokens=MAX_TOKENS):
#     """Splits content into manageable chunks if too large for OpenAI."""
#     encoding = tiktoken.encoding_for_model("gpt-4")
#     tokens = encoding.encode(content)

#     if len(tokens) <= max_tokens:
#         return [encoding.decode(tokens)]

#     # Split into smaller chunks
#     chunks = []
#     for i in range(0, len(tokens), CHUNK_SIZE):
#         chunk = tokens[i : i + CHUNK_SIZE]
#         chunks.append(encoding.decode(chunk))

#     return chunks

# def get_git_diff():
#     """Fetch latest commit diff, including unstaged changes."""
#     try:
#         subprocess.run(["git", "add", "-A"], check=True)  # Stage all changes
#         result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=True)
#         diff_output = result.stdout.strip()

#         logging.info("Git Diff Output:")
#         logging.info(diff_output if diff_output else "No changes detected.")

#         return diff_output
#     except subprocess.CalledProcessError as e:
#         logging.error(f"Error executing git diff: {e}")
#         return ""

# def call_openai_with_retry(prompt):
#     """Send request to OpenAI with retry mechanism."""
#     retries = 0
#     while retries < 3:
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are an AI reviewing code changes for quality."},
#                     {"role": "user", "content": prompt}  
#                 ],
#                 max_tokens=1000
#             )

#             review_content = response.choices[0].message.content.strip()
#             logging.info("Received review from OpenAI:")
#             logging.info(review_content)

#             return review_content
#         except openai.APIError as e:
#             wait_time = (2 ** retries) * 10  
#             logging.error(f"OpenAI API error: {e}. Retrying in {wait_time} seconds...")
#             time.sleep(wait_time)
#             retries += 1

#     logging.error("OpenAI API rate limit exceeded after retries.")
#     return "Review failed due to API limits."

# def review_commit():
#     """Get Git diff and request code review."""
#     diff_text = get_git_diff()
#     if not diff_text:
#         return "No changes detected."

#     chunks = truncate_content(diff_text)

#     review_results = []
#     for chunk in chunks:
#         prompt = f"Review the following code changes and provide comments:\n{chunk}"
#         logging.info("Sending the following prompt to OpenAI:")
#         logging.info(prompt)
#         review_results.append(call_openai_with_retry(prompt))

#     return "\n\n".join(review_results)

# if __name__ == "__main__":
#     review = review_commit()

#     with open("review.txt", "w") as file:
#         file.write(review)

#     logging.info("Review saved to review.txt")
#     print("Review Comments:\n", review)


# import pytest
# import scripts.review_commit as rc

# def test_truncate_content():
#     content = "This is a test string " * 1000  # Simulate long text
#     chunks = rc.truncate_content(content, max_tokens=100)
#     assert len(chunks) > 1  # Should be split

# def test_get_git_diff(mocker):
#     mocker.patch("scripts.review_commit.subprocess.run", return_value=mocker.Mock(stdout="mock_diff"))
#     assert rc.get_git_diff() == "mock_diff"

# def test_review_commit(mocker):
#     mocker.patch("scripts.review_commit.get_git_diff", return_value="Some changes")
#     mocker.patch("scripts.review_commit.call_openai_with_retry", return_value="Mock review")
#     result = rc.review_commit()
#     assert "Mock review" in result






# /////////////



# image: python:3.9

# before_script:
#   - pip install --upgrade pip
#   - pip install -r requirements.txt --cache-dir .cache/pip

# stages:
#   - review
#   - test

# review:
#   stage: review
#   script:
#     - python scripts/review_commit.py > review.txt
#   artifacts:
#     paths:
#       - review.txt
#   only:
#     - merge_requests
#     - branches

# test:
#   stage: test
#   script:
#     - pytest tests/
#   artifacts:
#     paths:
#       - test-results.xml
#   when: always





# import os
# import openai
# import logging
# import time

# logging.basicConfig(level=logging.INFO)

# if not os.getenv("OPENAI_API_KEY"):
#     raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

# client = openai.OpenAI()

# IGNORE_PATTERNS = ["*.log", "*.json", "*.md"]  # ✅ Added file filters
# MAX_FILE_SIZE = 500_000  # ✅ Excludes large files

# def get_all_files():
#     """Fetch all Python files in the project, avoiding unnecessary files."""
#     ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", ".cache", "dist", "build"}
#     files = []
#     for root, _, filenames in os.walk("."):
#         if any(ignored in root for ignored in ignore_dirs):
#             continue
#         for filename in filenames:
#             if filename.endswith(".py") and os.path.getsize(os.path.join(root, filename)) < MAX_FILE_SIZE:
#                 if not any(filename.endswith(pattern) for pattern in IGNORE_PATTERNS):
#                     files.append(os.path.join(root, filename))
    
#     content = {}
#     for file in files:
#         with open(file, "r", encoding="utf-8") as f:
#             content[file] = f.read()

#     return content

# def full_project_review(files):
#     """Send all project files to OpenAI for analysis, splitting into chunks."""
#     reviews = []
#     for file, content in files.items():
#         prompt = f"Review this Python file and provide detailed feedback:\n{file}\n\n{content}"
#         retries = 3
#         for attempt in range(retries):
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4",
#                     messages=[
#                         {"role": "system", "content": "You are a senior software architect."},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 reviews.append(f"### {file} ###\n{response.choices[0].message.content}")
#                 break
#             except openai.APIError as e:
#                 logging.error(f"OpenAI API error: {e}, attempt {attempt + 1} of {retries}")
#                 time.sleep(2 ** attempt)
    
#     return "\n".join(reviews) if reviews else "Review failed due to API error."

# if __name__ == "__main__":
#     files = get_all_files()
#     review = full_project_review(files)
#     with open("full_review.txt", "w") as file:
#         file.write(review)

#     print("Full Project Review:\n", review)






# import os
# import openai
# import subprocess
# import logging
# import time
# import tiktoken

# logging.basicConfig(level=logging.INFO)

# # Ensure OpenAI API key is set
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise EnvironmentError("Missing OPENAI_API_KEY. Please set it in your environment variables.")

# client = openai.OpenAI()

# MAX_TOKENS = 4096  # Ensure consistent token limits
# CHUNK_SIZE = 3000  # Adjusted for better chunking

# def truncate_content(content, max_tokens=MAX_TOKENS):
#     """Splits content into manageable chunks if too large for OpenAI."""
#     encoding = tiktoken.encoding_for_model("gpt-4")
#     tokens = encoding.encode(content)

#     if len(tokens) <= max_tokens:
#         return [encoding.decode(tokens)]

#     # Split into smaller chunks
#     chunks = []
#     for i in range(0, len(tokens), CHUNK_SIZE):
#         chunk = tokens[i : i + CHUNK_SIZE]
#         chunks.append(encoding.decode(chunk))

#     return chunks

# def get_git_diff():
#     """Fetch latest commit diff, including unstaged changes."""
#     try:
#         subprocess.run(["git", "add", "-A"], check=True)  # Stage all changes
#         result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=True)
#         diff_output = result.stdout.strip()

#         logging.info("Git Diff Output:")
#         logging.info(diff_output if diff_output else "No changes detected.")

#         return diff_output
#     except subprocess.CalledProcessError as e:
#         logging.error(f"Error executing git diff: {e}")
#         return ""

# def call_openai_with_retry(prompt):
#     """Send request to OpenAI with retry mechanism."""
#     retries = 0
#     while retries < 3:
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are an AI reviewing code changes for quality."},
#                     {"role": "user", "content": prompt}  
#                 ],
#                 max_tokens=1000
#             )

#             review_content = response.choices[0].message.content.strip()
#             logging.info("Received review from OpenAI:")
#             logging.info(review_content)

#             return review_content
#         except openai.APIError as e:
#             wait_time = (2 ** retries) * 10  
#             logging.error(f"OpenAI API error: {e}. Retrying in {wait_time} seconds...")
#             time.sleep(wait_time)
#             retries += 1

#     logging.error("OpenAI API rate limit exceeded after retries.")
#     return "Review failed due to API limits."

# def review_commit():
#     """Get Git diff and request code review."""
#     diff_text = get_git_diff()
#     if not diff_text:
#         return "No changes detected."

#     chunks = truncate_content(diff_text)

#     review_results = []
#     for chunk in chunks:
#         prompt = f"Review the following code changes and provide comments:\n{chunk}"
#         logging.info("Sending the following prompt to OpenAI:")
#         logging.info(prompt)
#         review_results.append(call_openai_with_retry(prompt))

#     return "\n\n".join(review_results)

# if __name__ == "__main__":
#     review = review_commit()

#     with open("review.txt", "w") as file:
#         file.write(review)

#     logging.info("Review saved to review.txt")
#     print("Review Comments:\n", review)




# import pytest
# import scripts.review_commit as rc

# def test_truncate_content():
#     content = "This is a test string " * 1000  # Simulate long text
#     chunks = rc.truncate_content(content, max_tokens=100)
#     assert len(chunks) > 1  # Should be split

# def test_get_git_diff(mocker):
#     mocker.patch("scripts.review_commit.subprocess.run", return_value=mocker.Mock(stdout="mock_diff"))
#     assert rc.get_git_diff() == "mock_diff"

# def test_review_commit(mocker):
#     mocker.patch("scripts.review_commit.get_git_diff", return_value="Some changes")
#     mocker.patch("scripts.review_commit.call_openai_with_retry", return_value="Mock review")
#     result = rc.review_commit()
#     assert "Mock review" in result
