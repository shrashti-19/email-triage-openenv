import requests

BASE_URL = "http://localhost:8000"

def run_baseline():
    # reset environment
    r = requests.post(f"{BASE_URL}/reset", json={})
    data = r.json()

    emails = data["observation"]["emails"]

    processed = []

    for email in emails:
        email_id = email["id"]

        # simple rule-based agent
        if "free" in email["subject"].lower() or "win" in email["subject"].lower():
            label = "spam"
            priority = "low"
        else:
            label = "important"
            priority = "high"

        step_payload = {
            "action": {
                "email_id": email_id,
                "label": label,
                "priority": priority
            }
        }

        requests.post(f"{BASE_URL}/step", json=step_payload)

        processed.append(email_id)

    scores = []
    for task_id in ["easy", "medium", "hard"]:
        grader = requests.post(
            f"{BASE_URL}/grader",
            json={"task_id": task_id, "processed": processed},
        )
        scores.append(grader.json().get("score", 0.0))

    print("Baseline Score:", sum(scores) / len(scores))


if __name__ == "__main__":
    run_baseline()
