<<<<<<< HEAD
Code Review Automation

Этот проект автоматизирует процесс ревью кода в GitHub и GitLab с использованием OpenAI API. Он включает в себя автоматический анализ коммитов и полного кода проекта при каждом запросе на слияние.

📌 Функциональность

Автоматический анализ коммитов – выполняется при каждом pull/merge request.

Полный обзор проекта – анализ всех файлов Python в репозитории.

Интеграция с GitHub Actions (review.yml).

Интеграция с GitLab CI/CD (.gitlab-ci.yml).

📦 Установка

Клонируйте репозиторий:

git clone https://github.com/your-repo/code-review-automation.git
cd code-review-automation

Установите зависимости:

pip install -r requirements.txt

Убедитесь, что у вас установлен API-ключ OpenAI:

export OPENAI_API_KEY="your_api_key_here"

🚀 Использование

Локальный запуск

Анализ последнего коммита:

python scripts/review_commit.py

Полный анализ проекта:

python scripts/full_review.py

CI/CD Автоматизация

GitHub Actions:

Запускает ревью кода на каждый pull request.

Определяется файлом .github/workflows/review.yml.

GitLab CI/CD:

Запускает ревью кода на merge requests и в ветках.

Определяется файлом .gitlab-ci.yml.

🔧 Структура проекта

```plaintext
├── scripts/
│   ├── review_commit.py   # Анализ последнего коммита
│   ├── full_review.py     # Полный анализ проекта
│
├── .github/
│   ├── workflows/
│   │   ├── review.yml    # Конфигурация GitHub Actions
│
├── .gitlab-ci.yml        # Конфигурация GitLab CI/CD
├── requirements.txt      # Зависимости проекта
├── README.md
```


⚠️ Важные замечания

Безопасность: Никогда не коммитьте API-ключ OpenAI в репозиторий.

Ограничения OpenAI API: Обратите внимание на лимиты запросов в зависимости от вашего тарифного плана.







**On English**



Code Review Automation

This project automates the code review process in GitHub and GitLab using the OpenAI API. It includes automatic commit analysis and a full project code review for every merge request.

📌 Features

Automatic commit analysis – executed on every pull/merge request.

Full project review – analyzes all Python files in the repository.

Integration with GitHub Actions (review.yml).

Integration with GitLab CI/CD (.gitlab-ci.yml).

📦 Installation

Clone the repository:

git clone https://github.com/your-repo/code-review-automation.git
cd code-review-automation

Install dependencies:

pip install -r requirements.txt

Ensure your OpenAI API key is set:

export OPENAI_API_KEY="your_api_key_here"

🚀 Usage

Local Execution

Analyze the latest commit:

python scripts/review_commit.py

Perform a full project review:

python scripts/full_review.py

CI/CD Automation

GitHub Actions:

Runs a code review for every pull request.

Defined in .github/workflows/review.yml.

GitLab CI/CD:

Runs code review on merge requests and branches.

Defined in .gitlab-ci.yml.

🔧 Project Structure
```plaintext
├── scripts/
│   ├── review_commit.py   # Анализ последнего коммита
│   ├── full_review.py     # Полный анализ проекта
│
├── .github/
│   ├── workflows/
│   │   ├── review.yml    # Конфигурация GitHub Actions
│
├── .gitlab-ci.yml        # Конфигурация GitLab CI/CD
├── requirements.txt      # Зависимости проекта
├── README.md
```

⚠️ Important Notes

Security: Never commit your OpenAI API key to the repository.

OpenAI API Limitations: Be aware of request limits depending on your subscription plan.
=======
# pipe-ci-cd
>>>>>>> 0cfb4423ad53269ae1e1c5d25fae9a68462db83c
