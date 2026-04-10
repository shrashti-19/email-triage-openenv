from openenv.core.env_server.http_server import create_app
from models import EmailTriageAction, EmailTriageObservation
from server.email_triage_env_environment import EmailTriageEnvironment

import uvicorn

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

@app.get("/tasks")
def get_tasks():
    return [
        {"id": "easy"},
        {"id": "medium"},
        {"id": "hard"}
    ]


# ✅ ONLY ONE GRADER
@app.post("/grader")
def grader(data: dict):
    task_id = data.get("task_id")

    processed = data.get("processed", [])
    if not isinstance(processed, list):
        processed = []

    count = len(processed)

    # ✅ DIFFERENT SCORING PER TASK
    if task_id == "easy":
        score = 0.2 + (count * 0.05)

    elif task_id == "medium":
        score = 0.3 + (count * 0.05)

    elif task_id == "hard":
        score = 0.4 + (count * 0.05)

    else:
        score = 0.25  # fallback

    # clamp
    if score >= 0.99:
        score = 0.99
    if score <= 0.01:
        score = 0.01

    return {
        "score": round(score, 2),
        "reason": f"Processed {count} emails for {task_id}"
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()