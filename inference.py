# # trigger rebuild

# import os
# import requests

# API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
# MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
# HF_TOKEN = os.getenv("HF_TOKEN", "")

# TASK_NAME = "email-triage"
# BENCHMARK = "email_triage_env"


# def log_start():
#     print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)


# def log_step(step, action, reward, done):
#     print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)


# def log_end(success, steps, score, rewards):
#     rewards_str = ",".join(f"{r:.2f}" for r in rewards)
#     print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


# def main():
#     log_start()

#     res = requests.post(f"{API_BASE_URL}/reset", json={})
#     data = res.json()

#     emails = data["observation"]["emails"]

#     rewards = []
#     processed = []
#     steps = 0

#     for i, email in enumerate(emails, start=1):
#         email_id = email["id"]
#         subject = email["subject"].lower()

#         if "free" in subject or "win" in subject:
#             label = "spam"
#             priority = "low"
#         else:
#             label = "important"
#             priority = "high"

#         action = {
#             "action": {
#                 "email_id": email_id,
#                 "label": label,
#                 "priority": priority
#             },
#             "timeout_s": 30
#         }

#         r = requests.post(f"{API_BASE_URL}/step", json=action).json()

#         reward = r.get("reward", 0.0)
#         done = r.get("done", False)

#         rewards.append(reward)
#         processed.append(email_id)

#         log_step(i, f"{label}-{priority}", reward, done)

#         steps = i

#     result = requests.post(f"{API_BASE_URL}/grader", json={"processed": processed}).json()

#     score = result.get("score", 0.0)
#     success = score >= 0.5

#     log_end(success, steps, score, rewards)


# if __name__ == "__main__":
#     main()


import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def main():
    try:
        res = requests.post(f"{API_BASE_URL}/reset", json={})
        data = res.json()
    except Exception as e:
        print("[ERROR] Reset failed:", str(e))
        data = {}

    # ✅ SAFE extraction (THIS FIXES YOUR ERROR)
    emails = data.get("observation", {}).get("emails", [])

    if not emails:
        print("[WARN] No emails found, response:", data)

    processed = []
    rewards = []

    for i, email in enumerate(emails, start=1):
        try:
            email_id = email.get("id")
            subject = email.get("subject", "").lower()

            if "free" in subject or "win" in subject:
                label = "spam"
                priority = "low"
            else:
                label = "important"
                priority = "high"

            action = {
                "action": {
                    "email_id": email_id,
                    "label": label,
                    "priority": priority
                },
                "timeout_s": 30
            }

            r = requests.post(f"{API_BASE_URL}/step", json=action)
            step_data = r.json()

            reward = step_data.get("reward", 0.0)
            done = step_data.get("done", False)

        except Exception as e:
            print("[ERROR] Step failed:", str(e))
            reward = 0.0
            done = True

        rewards.append(reward)
        processed.append(email_id)

        print(f"[STEP] step={i} reward={reward} done={done}")

    # ✅ SAFE grader
    try:
        result = requests.post(
            f"{API_BASE_URL}/grader",
            json={"processed": processed}
        ).json()

        score = result.get("score", 0.0)

    except Exception as e:
        print("[ERROR] Grader failed:", str(e))
        score = 0.0

    print(f"[END] score={score}")


if __name__ == "__main__":
    main()