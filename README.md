# Dxora — Automated Multi-Platform Posting API

## Overview

Dxora is a Python-based social media automation project that allows users to publish content across multiple social media platforms through a centralized REST API.

Built using FastAPI, the application supports asynchronous publishing, platform-specific integrations, input validation, and independent error handling.

## Features

- Centralized REST API for social media publishing.
- Integration with five social media platforms.
- Asynchronous publishing using Python's `asyncio`.
- Independent execution of platform publishing tasks.
- Error isolation so one platform's failure does not stop other publishing attempts.
- Environment-based credential management.
- Request validation using Pydantic.
- Automated testing using Pytest.

## Supported Platforms

| Platform | Integration |
|---|---|
| Bluesky | Integrated |
| Telegram | Integrated |
| Mastodon | Integrated |
| Facebook Pages | Integrated |
| Threads | Integrated |

## Tech Stack

- **Language:** Python
- **Backend Framework:** FastAPI
- **Server:** Uvicorn
- **Data Validation:** Pydantic
- **HTTP Client:** HTTPX / Requests
- **Environment Management:** Python-dotenv
- **Testing:** Pytest

## Project Structure

```text
automated-posting/
│
├── app/
│   ├── platforms/
│   │   ├── base.py
│   │   ├── bluesky.py
│   │   ├── telegram.py
│   │   ├── mastodon.py
│   │   ├── facebook.py
│   │   └── threads.py
│   │
│   ├── services/
│   │   └── posting_service.py
│   │
│   ├── config.py
│   ├── main.py
│   └── schemas.py
│
├── tests/
│   ├── test_posting.py
│   ├── test_facebook.py
│   └── test_threads.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd automated-posting
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Use `.env.example` as a reference and add your own platform credentials locally.

Required environment variables:

```env
BLUESKY_HANDLE=your_handle
BLUESKY_APP_PASSWORD=your_app_password

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

MASTODON_BASE_URL=https://mastodon.social
MASTODON_ACCESS_TOKEN=your_access_token

FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token

THREADS_USER_ID=your_threads_user_id
THREADS_ACCESS_TOKEN=your_threads_access_token
```

**Security:** Never upload your `.env` file or actual API credentials to GitHub.

## Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Usage

### POST /posting

Publishes the supplied message to the configured and integrated platforms.

**Example request:**

```json
{
  "message": "Hello! This is an automated post from Dxora.",
  "cta_url": "https://example.com"
}
```

The API returns an individual result for each platform, including its success status and any error information.

**Example response structure:**

```json
{
  "results": [
    {
      "platform": "bluesky",
      "success": true,
      "post_id": "post_identifier",
      "published_url": null,
      "error": null
    }
  ]
}
```

Actual response fields depend on the platform implementation and publishing result.

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Check Python syntax:

```bash
python -m compileall -q app tests
```

## Security Practices

- API credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- `.env.example` contains placeholder values only.
- Access tokens and passwords should never be committed to version control.

## Future Improvements

- Scheduled publishing.
- Publishing history and analytics.
- Media and image publishing support.
- Improved automated test coverage.
- Additional social media integrations.


## Author

**Rahul Passi**

B.Tech – Mathematics and Computing  
Delhi Technological University (DTU)


