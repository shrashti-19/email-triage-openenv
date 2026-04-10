from openenv.core.env_server.http_server import create_app
from graders import grade_task, grade_easy, grade_medium, grade_hard
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
    return {"message": "Email Triage Env is running"}

@app.get("/tasks")
def get_tasks():
    return [
        {"id": "easy", "name": "Easy Email Triage", "difficulty": "easy"},
        {"id": "medium", "name": "Medium Email Triage", "difficulty": "medium"},
        {"id": "hard", "name": "Hard Email Triage", "difficulty": "hard"},
    ]

@app.post("/grader")
def grader(data: dict):
    task_id = data.get("task_id", "easy")
    if task_id == "easy":
        return grade_easy(data)
    elif task_id == "medium":
        return grade_medium(data)
    elif task_id == "hard":
        return grade_hard(data)
    return grade_task(data)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
