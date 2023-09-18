# Resume Tracker

## Motivation

I wanted to have a way to have one static link for my resume that I could share with anyone. And whenever I update my resume, I want to be able to update it in one place and have it update everywhere. I also wanted to be able to track how many times my resume was viewed, when, and which website it was viewed from.

## How it works

It uses Python FastAPI with 2 endpoints:

- `/resume` - redirects to my resume
- `/metrics` - gets metrics for my resume

## Configuration

It is configured using environment variables:

- `RESUME_URL` - URL to my resume

## How to install locally?

1. Clone the repo

```bash
git clone https://github.com/mathewhany/resume-tracker.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
RESUME_URL=<resume-url> uvicorn app.main:app --reload
```

## How to test?

```bash
pytest
```