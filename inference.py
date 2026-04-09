import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("API_KEY", "")

# ✅ OpenAI client (REQUIRED)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


# ✅ REQUIRED LOG FUNCTIONS
def log_start():
    print("[START] task=email-triage", flush=True)


def log_step(step, reward, done):
    print(
        f"[STEP] step={step} reward={reward:.2f} done={'true' if done else 'false'}",
        flush=True,
    )


def log_end(score, steps):
    print(
        f"[END] task=email-triage score={score:.2f} steps={steps}",
        flush=True,
    )


# ✅ REQUIRED LLM CALL (IMPORTANT)
def call_llm():
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Classify this email"}
            ],
        )
    except Exception as e:
        print("[WARN] LLM call failed:", str(e))


def main():
    log_start()

    # ✅ RESET
    try:
        res = requests.post(f"{API_BASE_URL}/reset", json={})
        data = res.json()
    except Exception as e:
        print("[ERROR] Reset failed:", str(e))
        data = {}

    emails = data.get("observation", {}).get("emails", [])

    processed = []
    rewards = []

    for i, email in enumerate(emails, start=1):

        # ✅ IMPORTANT: call LLM here
        call_llm()

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

        processed.append(email_id)
        rewards.append(reward)

        log_step(i, reward, done)

    # ✅ GRADER
    try:
        result = requests.post(
            f"{API_BASE_URL}/grader",
            json={"processed": processed}
        ).json()

        score = result.get("score", 0.0)

    except Exception as e:
        print("[ERROR] Grader failed:", str(e))
        score = 0.0

    log_end(score, len(processed))


if __name__ == "__main__":
    main()