from openenv.core.env_server.http_server import create_app
from models import EmailTriageAction, EmailTriageObservation
from server.email_triage_env_environment import EmailTriageEnvironment

import uvicorn

# Create FastAPI app
app = create_app(
    EmailTriageEnvironment,
    EmailTriageAction,
    EmailTriageObservation,
    env_name="email_triage_env",
    max_concurrent_envs=1,
)


# ✅ Home
@app.get("/")
def home():
    return {"message": "Email Triage Env is running 🚀"}


# ✅ Tasks endpoint
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": "easy", "description": "Process at least 2 emails"},
            {"id": "medium", "description": "Process at least 3 emails"},
            {"id": "hard", "description": "Process all emails correctly"},
        ]
    }


# ✅ Grader (FINAL FIXED VERSION)
@app.post("/grader")
def grader(data: dict):
    task_id = data.get("task_id")
    processed = data.get("processed")

    # Safe handling
    if not isinstance(processed, list):
        count = 0
    else:
        count = len(processed)

    # ✅ Ensure score NEVER becomes 0 or 1
    if task_id == "easy":
        score = (count + 1) / 6

    elif task_id == "medium":
        score = (count + 1) / 7

    elif task_id == "hard":
        score = (count + 1) / 8

    else:
        score = 0.2  # safe fallback

    # ✅ Final clamp (strictly between 0 and 1)
    if score >= 1.0:
        score = 0.99
    if score <= 0.0:
        score = 0.01

    return {"score": round(score, 2)}


# ✅ Entry point
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()