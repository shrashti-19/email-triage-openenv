import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


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


def main():
    log_start()

    # ✅ RESET
    try:
        res = requests.post(f"{API_BASE_URL}/reset", json={})
        data = res.json()
    except Exception as e:
        print("[ERROR] Reset failed:", str(e))
        data = {}

    # ✅ SAFE extraction (fixes KeyError)
    emails = data.get("observation", {}).get("emails", [])

    if not emails:
        print("[WARN] No emails found, response:", data)

    processed = []
    rewards = []

    # ✅ LOOP
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

        # ✅ REQUIRED STEP LOG
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

    # ✅ REQUIRED END LOG
    log_end(score, len(processed))


if __name__ == "__main__":
    main()