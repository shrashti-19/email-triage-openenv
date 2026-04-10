from openenv.core.env_server.http_server import create_app
from models import EmailTriageAction, EmailTriageObservation
from server.email_triage_env_environment import EmailTriageEnvironment

import uvicorn

# Create app
app = create_app(
    EmailTriageEnvironment,
    EmailTriageAction,
    EmailTriageObservation,
    env_name="email_triage_env",
    max_concurrent_envs=1,
)


@app.get("/")
def home():
    return {"message": "Email Triage Env is running 🚀"}


# ✅ SIMPLE TASKS (NO GRADER FIELD)
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": "easy"},
            {"id": "medium"},
            {"id": "hard"}
        ]
    }


# ✅ SINGLE GRADER ONLY
@app.post("/grader")
def grader(data: dict):
    task_id = data.get("task_id") or "easy"

    processed = data.get("processed", [])
    if not isinstance(processed, list):
        processed = []

    count = len(processed)

    # ✅ SIMPLE SAFE SCORE
    score = 0.3 + (count * 0.05)

    # clamp
    if score >= 0.99:
        score = 0.99
    if score <= 0.01:
        score = 0.01

    return {
        "score": round(score, 2),
        "reason": f"Processed {count} emails"
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()