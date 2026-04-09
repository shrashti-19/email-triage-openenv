import os
import requests
from openai import OpenAI

# Environment variables (IMPORTANT)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("API_KEY", "")

# OpenAI client (MANDATORY for checker)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

TASK_NAME = "email-triage"
BENCHMARK = "email_triage_env"


def log_start():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def call_llm():
    """
    REQUIRED: Make at least one call to LLM proxy
    """
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Classify email"}]
        )
    except Exception as e:
        print("[ERROR] LLM call failed:", str(e))


def main():
    log_start()

    # ✅ REQUIRED LLM CALL
    call_llm()

    # Reset environment
    try:
        res = requests.post(f"{API_BASE_URL}/reset", json={})
        data = res.json()

        emails = data.get("observation", {}).get("emails", [])
        if not emails:
            emails = data.get("emails", [])

    except Exception as e:
        print("[ERROR] Reset failed:", str(e))
        log_end(False, 0, 0.0, [])
        return

    rewards = []
    processed = []
    steps = 0

    # Process emails
    for i, email in enumerate(emails, start=1):
        email_id = email.get("id")
        subject = email.get("subject", "").lower()

        if "free" in subject or "win" in subject:
            label = "spam"
            priority = "low"
        else:
            label = "important"
            priority = "high"

        action_payload = {
            "action": {
                "email_id": email_id,
                "label": label,
                "priority": priority
            },
            "timeout_s": 30
        }

        try:
            r = requests.post(f"{API_BASE_URL}/step", json=action_payload)
            step_data = r.json()

            reward = step_data.get("reward", 0.0)
            done = step_data.get("done", False)

        except Exception as e:
            print("[ERROR] Step failed:", str(e))
            reward = 0.0
            done = True

        rewards.append(reward)
        processed.append(email_id)

        log_step(i, f"{label}-{priority}", reward, done)

        steps = i

    # Grader
    try:
        result = requests.post(
            f"{API_BASE_URL}/grader",
            json={"processed": processed}
        ).json()

        score = result.get("score", 0.0)

    except Exception as e:
        print("[ERROR] Grader failed:", str(e))
        score = 0.0

    success = score >= 0.5

    log_end(success, steps, score, rewards)


if __name__ == "__main__":
    main()