import json
import sys


def calculate_progress(completed_tasks, total_tasks):
    """Calculate the progress percentage.

    Args:
        completed_tasks: The number of completed tasks.
        total_tasks: The total number of tasks.

    Returns:
        A dictionary containing the progress percentage.
    """
    if total_tasks == 0:
        percentage = 0.0
    else:
        percentage = (completed_tasks / total_tasks) * 100.0

    return {"percentage": round(percentage, 2)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python calculate_progress.py <completed_tasks> <total_tasks>"}))
        sys.exit(1)

    try:
        completed = int(sys.argv[1])
        total = int(sys.argv[2])
    except ValueError:
        print(json.dumps({"error": "Invalid input. Please provide integers for tasks."}))
        sys.exit(1)

    result = calculate_progress(completed, total)
    print(json.dumps(result))
