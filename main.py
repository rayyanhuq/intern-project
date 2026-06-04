from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/generate-summary")
def generate_summary():

    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not found"
        )

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            "Summarize: FastAPI is a modern Python framework."
        )

        return {
            "summary": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(e)}"
        )