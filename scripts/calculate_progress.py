import json
import sys

def calculate_progress(completed_tasks, total_tasks):
    """
    Calculates the progress percentage.

    Args:
        completed_tasks: The number of completed tasks.
        total_tasks: The total number of tasks.

    Returns:
        A dictionary with the progress percentage.
    """
    if total_tasks == 0:
        percentage = 0
    else:
        percentage = (completed_tasks / total_tasks) * 100

    return {"percentage": percentage}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python calculate_progress.py <completed_tasks> <total_tasks>"}))
        sys.exit(1)

    try:
        completed = int(sys.argv[1])
        total = int(sys.argv[2])
        result = calculate_progress(completed, total)
        print(json.dumps(result))
    except ValueError:
        print(json.dumps({"error": "Invalid input. Please provide integers for tasks."}))
        sys.exit(1)
