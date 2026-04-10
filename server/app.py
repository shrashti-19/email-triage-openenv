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

    # safe handling
    if not isinstance(processed, list):
        count = 0
    else:
        count = len(processed)

    # scoring
    if task_id == "easy":
        score = count / 5
        reason = f"Processed {count} emails for easy task"

    elif task_id == "medium":
        score = (count + 1) / 6
        reason = f"Processed {count} emails for medium task"

    elif task_id == "hard":
        score = (count + 2) / 7
        reason = f"Processed {count} emails for hard task"

    else:
        score = 0.1
        reason = "Unknown task"

    # clamp strictly between (0,1)
    if score >= 1.0:
        score = 0.99
    if score <= 0.0:
        score = 0.01

    return {
        "score": round(score, 2),
        "reason": reason
    }

# ✅ Entry point
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()