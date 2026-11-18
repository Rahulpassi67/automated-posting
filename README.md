# Dxora – Automated Multi-Platform Posting API

**A Python-based social media automation system built using FastAPI.**

Dxora is a multi-platform social media posting API that allows users to publish content across multiple social media platforms through a centralized REST API.

The project uses asynchronous programming, platform-specific integrations, environment-based configuration, and independent error handling to simplify social media publishing.

---

## 1. Project Overview

Managing social media accounts across multiple platforms can be time-consuming. Dxora aims to simplify this process by providing a centralized API through which users can publish content to multiple platforms.

The application integrates individual platform adapters with a common posting service. It supports asynchronous publishing and isolates platform failures so that an error on one platform does not necessarily interrupt publishing on others.

## 2. Features

- Centralized REST API for social media publishing.
- Integration with five social media platforms.
- Asynchronous publishing using Python's `asyncio`.
- Platform-specific publishing adapters.
- Independent error handling and failure isolation.
- Environment-based configuration using environment variables.
- Request validation using Pydantic.
- Automated testing using Pytest.
- FastAPI interactive API documentation.
- Secure separation of environment credentials from source code.

## 3. Supported Platforms

Dxora currently supports the following integrations:

| Platform | Integration |
|---|---|
| Bluesky | Integrated |
| Mastodon | Integrated |
| Telegram | Integrated |
| Facebook Pages | Integrated |
| Threads | Integrated |

Each platform has its own adapter that handles platform-specific authentication and publishing requests.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API framework |
| HTTPX | Asynchronous HTTP requests |
| Pydantic | Request validation and data schemas |
| asyncio | Asynchronous task execution |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |
| Git & GitHub | Version control and project hosting |

## 5. Project Structure

```text
automated-posting/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   │
│   ├── platforms/
│   │   ├── base.py
│   │   ├── bluesky.py
│   │   ├── mastodon.py
│   │   ├── telegram.py
│   │   ├── facebook.py
│   │   └── threads.py
│   │
│   └── services/
│       └── posting_service.py
│
├── tests/
│   ├── test_posting.py
│   ├── test_facebook.py
│   └── test_threads.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** The `.env` file contains private credentials and must never be committed to GitHub.

## 6. Prerequisites

Before running the project, ensure that you have:

- Python 3.10 or later.
- pip (Python package installer).
- Git.
- A code editor such as Visual Studio Code.
- Developer credentials or API access for the social media platforms you want to use.

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/Rahulpassi67/automated-posting.git
```

### Step 2: Navigate to the project directory

```bash
cd automated-posting
```

### Step 3: Create a virtual environment

```bash
python3 -m venv venv
```

### Step 4: Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## 8. Environment Configuration

The application uses environment variables to manage application settings and API credentials.

Create a `.env` file in the project root directory.

Use `.env.example` as a reference for the configuration structure.

The example configuration includes:

```env
API_HOST=127.0.0.1
API_PORT=8000

APP_ENV=development
APP_NAME=Dxora
DEBUG=False

BLUESKY_HANDLE=your_bluesky_handle
BLUESKY_APP_PASSWORD=your_bluesky_app_password

MASTODON_BASE_URL=https://mastodon.social
MASTODON_ACCESS_TOKEN=your_mastodon_access_token

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

FACEBOOK_PAGE_ID=your_facebook_page_id
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token

THREADS_USER_ID=your_threads_user_id
THREADS_ACCESS_TOKEN=your_threads_access_token
```

Replace the placeholder values with your own credentials where applicable.

**Important security practices:**

- Never upload your actual `.env` file to GitHub.
- Never expose access tokens, API keys, or passwords.
- Keep `.env` included in `.gitignore`.
- Use `.env.example` to document the required configuration without exposing secrets.

Additional platform credentials should be configured according to the corresponding adapter and application configuration.

## 9. Running the Application

Ensure that your virtual environment is activated and dependencies are installed.

Start the FastAPI development server using:

```bash
uvicorn app.main:app --reload
```

By default, the application runs at:

```text
http://127.0.0.1:8000
```

### Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Open the following URL in your browser

