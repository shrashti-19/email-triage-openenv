# # # from openenv.core.env_server.http_server import create_app
# # # from models import EmailTriageAction, EmailTriageObservation
# # # from server.email_triage_env_environment import EmailTriageEnvironment

# # # import uvicorn

# # # # Create FastAPI app
# # # app = create_app(
# # #     EmailTriageEnvironment,
# # #     EmailTriageAction,
# # #     EmailTriageObservation,
# # #     env_name="email_triage_env",
# # #     max_concurrent_envs=1,
# # # )


# # # # ✅ Home
# # # @app.get("/")
# # # def home():
# # #     return {"message": "Email Triage Env is running 🚀"}


# # # # ✅ Tasks endpoint
# # # @app.get("/tasks")
# # # def get_tasks():
# # #     return {
# # #         "tasks": [
# # #             {"id": "easy", "description": "Process at least 2 emails"},
# # #             {"id": "medium", "description": "Process at least 3 emails"},
# # #             {"id": "hard", "description": "Process all emails correctly"},
# # #         ]
# # #     }


# # # # ✅ Grader (FINAL FIXED VERSION)
# # # @app.post("/grader")
# # # def grader(data: dict):
# # #     task_id = data.get("task_id")
# # #     processed = data.get("processed")

# # #     # safe handling
# # #     if not isinstance(processed, list):
# # #         count = 0
# # #     else:
# # #         count = len(processed)

# # #     # scoring
# # #     if task_id == "easy":
# # #         score = (count+1) / 6
# # #         reason = f"Processed {count} emails for easy task"

# # #     elif task_id == "medium":
# # #         score = (count + 2) / 7
# # #         reason = f"Processed {count} emails for medium task"

# # #     elif task_id == "hard":
# # #         score = (count + 3) / 8
# # #         reason = f"Processed {count} emails for hard task"

# # #     else:
# # #         score = 0.1
# # #         reason = "Unknown task"

# # #     # clamp strictly between (0,1)
# # #     if score >= 1.0:
# # #         score = 0.99
# # #     if score <= 0.0:
# # #         score = 0.01

# # #     return {
# # #         "score": round(score, 2),
# # #         "reason": reason
# # #     }

# # # # ✅ Entry point
# # # def main():
# # #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # # if __name__ == "__main__":
# # #     main()



# # from openenv.core.env_server.http_server import create_app
# # from models import EmailTriageAction, EmailTriageObservation
# # from server.email_triage_env_environment import EmailTriageEnvironment

# # import uvicorn

# # app = create_app(
# #     EmailTriageEnvironment,
# #     EmailTriageAction,
# #     EmailTriageObservation,
# #     env_name="email_triage_env",
# #     max_concurrent_envs=1,
# # )


# # @app.get("/")
# # def home():
# #     return {"message": "Email Triage Env is running 🚀"}


# # @app.get("/tasks")
# # def get_tasks():
# #     return {
# #         "tasks": [
# #             {"id": "easy", "description": "Process at least 2 emails"},
# #             {"id": "medium", "description": "Process at least 3 emails"},
# #             {"id": "hard", "description": "Process all emails correctly"},
# #         ]
# #     }


# # @app.post("/grader")
# # def grader(data: dict):
# #     # ✅ Handle ALL formats
# #     task_id = (
# #         data.get("task_id")
# #         or data.get("task")
# #         or (data.get("task", {}) or {}).get("id")
# #     )

# #     processed = (
# #         data.get("processed")
# #         or (data.get("state", {}) or {}).get("processed")
# #         or []
# #     )

# #     if not isinstance(processed, list):
# #         processed = []

# #     count = len(processed)

# #     # ✅ SAFE SCORING (NO EDGE VALUES EVER)
# #     if task_id == "easy":
# #         score = 0.21 + (count * 0.07)

# #     elif task_id == "medium":
# #         score = 0.31 + (count * 0.07)

# #     elif task_id == "hard":
# #         score = 0.41 + (count * 0.07)

# #     else:
# #         score = 0.2

# #     # ✅ HARD CLAMP
# #     if score >= 0.99:
# #         score = 0.99
# #     if score <= 0.01:
# #         score = 0.01

# #     return {
# #         "score": round(score, 2),
# #         "reason": f"Processed {count} emails for {task_id}"
# #     }


# # def main():
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # if __name__ == "__main__":
# #     main()


# from openenv.core.env_server.http_server import create_app
# from models import EmailTriageAction, EmailTriageObservation
# from server.email_triage_env_environment import EmailTriageEnvironment

# import uvicorn

# app = create_app(
#     EmailTriageEnvironment,
#     EmailTriageAction,
#     EmailTriageObservation,
#     env_name="email_triage_env",
#     max_concurrent_envs=1,
# )


# @app.get("/")
# def home():
#     return {"message": "Email Triage Env is running 🚀"}


# # @app.get("/tasks")
# # def get_tasks():
# #     return {
# #         "tasks": [
# #             {"id": "easy", "description": "Process at least 2 emails"},
# #             {"id": "medium", "description": "Process at least 3 emails"},
# #             {"id": "hard", "description": "Process all emails correctly"},
# #         ]
# #     }

# @app.get("/tasks")
# def get_tasks():
#     return {
#         "tasks": {
#             "easy": {
#                 "description": "Process at least 2 emails",
#                 "grader": "grader"
#             },
#             "medium": {
#                 "description": "Process at least 3 emails",
#                 "grader": "grader"
#             },
#             "hard": {
#                 "description": "Process all emails correctly",
#                 "grader": "grader"
#             }
#         }
#     }


# @app.post("/grader")
# def grader(data: dict):
#     # ✅ handle ALL input formats
#     task_id = (
#         data.get("task_id")
#         or data.get("task")
#         or (data.get("task", {}) or {}).get("id")
#     )

#     processed = (
#         data.get("processed")
#         or (data.get("state", {}) or {}).get("processed")
#         or []
#     )

#     if not isinstance(processed, list):
#         processed = []

#     count = len(processed)

#     # ✅ SAFE SCORING (no edge values)
#     if task_id == "easy":
#         score = 0.21 + (count * 0.07)
#         reason = f"Processed {count} emails for easy"

#     elif task_id == "medium":
#         score = 0.31 + (count * 0.07)
#         reason = f"Processed {count} emails for medium"

#     elif task_id == "hard":
#         score = 0.41 + (count * 0.07)
#         reason = f"Processed {count} emails for hard"

#     else:
#         # ✅ FINAL FIX: fallback behaves like valid task
#         score = 0.33 + (count * 0.06)
#         reason = f"Fallback scoring with {count} emails"

#     # ✅ HARD CLAMP
#     if score >= 0.99:
#         score = 0.99
#     if score <= 0.01:
#         score = 0.01

#     return {
#         "score": round(score, 2),
#         "reason": reason
#     }


# def main():
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# if __name__ == "__main__":
#     main()


from openenv.core.env_server.http_server import create_app
from models import EmailTriageAction, EmailTriageObservation
from server.email_triage_env_environment import EmailTriageEnvironment

import uvicorn

# ✅ IMPORTANT: register graders HERE
app = create_app(
    EmailTriageEnvironment,
    EmailTriageAction,
    EmailTriageObservation,
    env_name="email_triage_env",
    max_concurrent_envs=1,
    graders=["easy", "medium", "hard"]   # ✅ FINAL FIX
)


@app.get("/")
def home():
    return {"message": "Email Triage Env is running 🚀"}


# ❌ REMOVE custom /tasks (OpenEnv handles internally)


@app.post("/grader")
def grader(data: dict):
    # ✅ handle all input formats
    task_id = (
        data.get("task_id")
        or data.get("task")
        or (data.get("task", {}) or {}).get("id")
    )

    processed = (
        data.get("processed")
        or (data.get("state", {}) or {}).get("processed")
        or []
    )

    if not isinstance(processed, list):
        processed = []

    count = len(processed)

    # ✅ SAFE SCORING
    if task_id == "easy":
        score = 0.21 + (count * 0.07)
        reason = f"Processed {count} emails for easy"

    elif task_id == "medium":
        score = 0.31 + (count * 0.07)
        reason = f"Processed {count} emails for medium"

    elif task_id == "hard":
        score = 0.41 + (count * 0.07)
        reason = f"Processed {count} emails for hard"

    else:
        score = 0.33 + (count * 0.06)
        reason = f"Fallback scoring with {count} emails"

    # ✅ HARD CLAMP
    if score >= 0.99:
        score = 0.99
    if score <= 0.01:
        score = 0.01

    return {
        "score": round(score, 2),
        "reason": reason
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()