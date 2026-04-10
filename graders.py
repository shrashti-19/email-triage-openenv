# from __future__ import annotations

# from typing import Any


# def grade_task(payload: dict[str, Any] | None = None) -> dict[str, Any]:
#     payload = payload or {}
#     task_id = payload.get("task_id")

#     processed = payload.get("processed", [])
#     if not isinstance(processed, list):
#         processed = []

#     count = len(processed)

#     if task_id == "easy":
#         score = 0.2 + (count * 0.05)
#     elif task_id == "medium":
#         score = 0.3 + (count * 0.05)
#     elif task_id == "hard":
#         score = 0.4 + (count * 0.05)
#     else:
#         score = 0.25

#     score = max(0.01, min(0.99, score))

#     return {
#         "score": round(score, 2),
#         "reason": f"Processed {count} emails for {task_id or 'default'}",
#     }

from __future__ import annotations
from typing import Any


def _score(task_id: str, payload: dict) -> dict:
    processed = payload.get("processed", [])
    if not isinstance(processed, list):
        processed = []
    count = len(processed)

    base = {"easy": 0.2, "medium": 0.3, "hard": 0.4}.get(task_id, 0.25)
    score = max(0.01, min(0.99, round(base + count * 0.05, 2)))

    return {
        "score": score,
        "reason": f"Processed {count} emails for {task_id}",
    }


def grade_task(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    task_id = payload.get("task_id", "easy")
    return _score(task_id, payload)


def grade_easy(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return _score("easy", payload or {})


def grade_medium(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return _score("medium", payload or {})


def grade_hard(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return _score("hard", payload or {})