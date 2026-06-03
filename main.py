from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/generate-summary")
def generate_summary():
    return {
        "summary": "This is a dummy summary response."
    }


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