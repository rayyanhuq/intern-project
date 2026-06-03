# Intern Project

A simple FastAPI application created as part of the internship onboarding tasks.

## Getting Started

### Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Run the application

```bash
uvicorn main:app --reload
```

Once the server is running, open:

* API: http://127.0.0.1:8000
* API Docs: http://127.0.0.1:8000/docs

## Available Endpoints

* `GET /health`
* `POST /generate-summary`
* `POST /extract-tasks`
* `POST /generate-email`

## Environment Variables

Create a `.env` file based on `.env.example` and add any required environment variables there.
