from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


class MeetingNotes(BaseModel):
    text: str


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

1. A concise summary
2. Key decisions made
3. Action items assigned
4. A professional follow-up email

Return ONLY valid JSON in this exact format:

{{
    "summary": "...",
    "key_decisions": ["..."],
    "action_items": ["..."],
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

        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Model returned invalid JSON"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(e)}"
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