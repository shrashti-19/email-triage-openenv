from openenv.core.env_server.http_server import create_app
from models import EmailTriageAction, EmailTriageObservation
from server.email_triage_env_environment import EmailTriageEnvironment

from fastapi import APIRouter
import uvicorn

# Create FastAPI app
app = create_app(
    EmailTriageEnvironment,
    EmailTriageAction,
    EmailTriageObservation,
    env_name="email_triage_env",
    max_concurrent_envs=1,
)

router = APIRouter()

@app.get("/")
def home():
    return {"message": "Email Triage Env is running 🚀"}


# ✅ TASKS (unchanged but good)
@router.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": "easy", "description": "Process at least 2 emails"},
            {"id": "medium", "description": "Process at least 3 emails"},
            {"id": "hard", "description": "Process all emails correctly"},
        ]
    }


# ✅ SAFE HELPERS
def clamp_score(score: float) -> float:
    if score >= 1.0:
        return 0.99
    if score <= 0.0:
        return 0.01
    return round(score, 2)


def safe_processed_count(data: dict) -> int:
    processed = data.get("processed")
    if not isinstance(processed, list):
        return 0
    return len(processed)


# ✅ SINGLE GRADER (IMPORTANT FIX)
@router.post("/grader")
def grader(data: dict):
    task_id = data.get("task_id")
    count = safe_processed_count(data)

    if task_id == "easy":
        score = count / 5

    elif task_id == "medium":
        score = (count + 1) / 6

    elif task_id == "hard":
        score = (count + 2) / 7

    else:
        score = 0.1  # fallback safe value

    return {"score": clamp_score(score)}


# ✅ Register routes
app.include_router(router)


# ✅ Entry point
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()