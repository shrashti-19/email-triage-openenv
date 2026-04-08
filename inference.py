import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")


def main():
    # Reset environment
    res = requests.post(f"{API_BASE_URL}/reset", json={})
    data = res.json()

    emails = data["observation"]["emails"]
    processed = []

    for email in emails:
        email_id = email["id"]
        subject = email["subject"].lower()

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

        requests.post(f"{API_BASE_URL}/step", json=action)
        processed.append(email_id)

    result = requests.post(
        f"{API_BASE_URL}/grader",
        json={"processed": processed}
    )

    print(result.json())


if __name__ == "__main__":
    main()