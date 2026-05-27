import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def parse_timestamp(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            # Attempt ISO 8601 parsing
            return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            return None
    return None


def is_task_overdue(task: Dict[str, Any], now: Optional[datetime] = None) -> bool:
    now = now or datetime.now(timezone.utc)
    due_date = parse_timestamp(task.get("due_date"))
    status = (task.get("status") or "").strip().lower()
    if due_date is None:
        return False
    return due_date < now and status != "concluida"


def overdue_subject_ids(tasks: List[Dict[str, Any]], now: Optional[datetime] = None) -> List[int]:
    now = now or datetime.now(timezone.utc)
    subject_ids: List[int] = []
    for task in tasks:
        if is_task_overdue(task, now=now):
            subject_id = task.get("subject_id")
            if isinstance(subject_id, int) and subject_id not in subject_ids:
                subject_ids.append(subject_id)
    return subject_ids


def filter_subjects(
    subjects: List[Dict[str, Any]],
    query: Optional[str] = None,
    overdue_subject_ids_list: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    filtered = list(subjects)
    if query:
        query_lower = query.strip().lower()
        filtered = [
            subject for subject in filtered
            if isinstance(subject.get("name"), str) and query_lower in subject["name"].lower()
        ]
    if overdue_subject_ids_list:
        overdue_set = set(overdue_subject_ids_list)
        filtered = [
            subject for subject in filtered
            if isinstance(subject.get("id"), int) and subject["id"] in overdue_set
        ]
    return filtered


if __name__ == "__main__":
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"error": "Expected JSON payload on stdin."}))
        raise SystemExit(1)

    subjects = payload.get("subjects", [])
    tasks = payload.get("tasks", [])
    query = payload.get("query")
    overdue = payload.get("overdue")
    overdue_ids = overdue_subject_ids(tasks)
    result = {
        "overdue_subject_ids": overdue_ids,
        "filtered_subjects": filter_subjects(subjects, query=query, overdue_subject_ids_list=overdue_ids if overdue else None),
    }
    print(json.dumps(result, default=str))
