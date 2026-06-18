from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
from datetime import datetime

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://intern-project-ten-mu.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


class MeetingNotes(BaseModel):
    text: str


def save_to_history(notes, result):

    history_file = "history.json"

    try:
        with open(history_file, "r") as file:
            history = json.load(file)
    except:
        history = []

    history.append({
        "notes": notes,
        "short_summary": result.get("short_summary"),
        "detailed_summary": result.get("detailed_summary"),
        "key_decisions": result.get("key_decisions"),
        "action_items": result.get("action_items"),
        "follow_up_email": result.get("follow_up_email"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/generate-summary")
def generate_summary(notes: MeetingNotes):

    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not found"
        )

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are helping process meeting notes.

Read the meeting notes and generate:

1. A short summary
2. A detailed summary
3. Key decisions made during the meeting
4. Action items assigned
5. A professional follow-up email

For action items:
- Extract the task
- Extract the owner
- Extract the deadline if mentioned
- Extract the priority if mentioned
- If deadline or priority is not mentioned, use "Not specified"

Return ONLY valid JSON in this exact format:

{{
  "short_summary": "...",
  "detailed_summary": "...",
  "key_decisions": [
    "..."
  ],
  "action_items": [
    {{
      "task": "...",
      "owner": "...",
      "deadline": "...",
      "priority": "..."
    }}
  ],
  "follow_up_email": "..."
}}

Meeting Notes:

{notes.text}
"""

        response = model.generate_content(prompt)

        cleaned_response = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(cleaned_response)

        save_to_history(
            notes.text,
            result
        )

        return result

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Model returned invalid JSON"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="AI service is temporarily unavailable. Please try again in a minute."
        )


@app.post("/extract-tasks")
def extract_tasks():
    return {
        "tasks": [
            "Dummy task 1",
            "Dummy task 2",
            "Dummy task 3"
        ]
    }


@app.post("/generate-email")
def generate_email():
    return {
        "email": "Hello, this is a dummy email response."
    }