from __future__ import annotations
from typing import Any


def _compute_score(task_id: str, processed: list) -> float:
    count = len(processed)
    base = {"easy": 0.2, "medium": 0.3, "hard": 0.4}.get(task_id, 0.25)
    return max(0.01, min(0.99, round(base + count * 0.05, 2)))


def grade_task(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    task_id = payload.get("task_id", "easy")
    processed = payload.get("processed", [])
    if not isinstance(processed, list):
        processed = []
    return {"score": _compute_score(task_id, processed), "reason": f"Processed {len(processed)} emails for {task_id}"}


def grade_easy(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    processed = payload.get("processed", [])
    if not isinstance(processed, list):
        processed = []
    return {"score": _compute_score("easy", processed), "reason": f"Processed {len(processed)} emails for easy"}


def grade_medium(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    processed = payload.get("processed", [])
    if not isinstance(processed, list):
        processed = []
    return {"score": _compute_score("medium", processed), "reason": f"Processed {len(processed)} emails for medium"}


def grade_hard(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    processed = payload.get("processed", [])
    if not isinstance(processed, list):
        processed = []
    return {"score": _compute_score("hard", processed), "reason": f"Processed {len(processed)} emails for hard"}
