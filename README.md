# Intern Project – AI Meeting Notes Processor

A full-stack AI-powered Meeting Notes Processor built using React, FastAPI, and Google Gemini AI.

The application processes meeting notes and automatically generates structured summaries, key decisions, action items, and professional follow-up emails.

## Features

* AI-generated meeting summaries
* Detailed meeting summaries
* Key decision extraction
* Action item extraction
* Follow-up email generation
* Gemini AI integration
* Meeting history storage using JSON
* Export results as TXT files
* Export results as JSON files
* Copy generated email
* Clear inputs and outputs
* Regenerate summaries
* Responsive frontend interface

## Tech Stack

### Frontend

* React
* Vite
* JavaScript

### Backend

* FastAPI
* Python
* Gemini AI API
* python-dotenv

## Deployment

### Frontend

https://intern-project-ten-mu.vercel.app

### Backend

https://meeting-notes-backend-y55p.onrender.com

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/rayyanhuq/intern-project.git
cd intern-project
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

### Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Available Endpoints

### GET /health

Checks backend status.

### POST /generate-summary

Generates:

* Short summary
* Detailed summary
* Key decisions
* Action items
* Follow-up email

### POST /extract-tasks

Dummy endpoint used during initial development.

### POST /generate-email

Dummy endpoint used during initial development.

## Testing

The application was tested using:

* Normal meeting notes
* Empty input validation
* Long meeting notes
* Invalid request body
* Missing API key
* AI API failure handling
* Frontend-backend integration
* Export functionality

## Project Structure

```text
intern_project/
?
??? main.py
??? history.json
??? requirements.txt
??? .env.example
??? README.md
?
??? frontend/
    ??? src/
    ??? public/
    ??? package.json
```

## Known Issues

* Gemini API may stop responding if the free quota limit is exceeded.
* Meeting history is currently stored in a JSON file.
* Export is currently available only in TXT and JSON formats.

## Future Improvements

* Add CSV export for action items.
* Add search functionality for meeting history.
* Store data in a database.
* Add user authentication.
* Improve the user interface.

## Author

Mohammed Rayyan Ul Huq K

B.Tech CSE (AIML)

SRM Institute of Science and Technology, Ramapuram
