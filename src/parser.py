def validate_course_data(data: dict) -> bool:
    """
    Returns True if the scraped data looks valid.
    Catches edge cases like missing fields or malformed enrollment numbers.
    """
    if not data:
        return False

    required_keys = ["code", "enrolled", "status"]
    for key in required_keys:
        if key not in data or not data[key]:
            print(f"[WARN] Missing field: {key}")
            return False

    valid_statuses = {"OPEN", "WAITLISTED", "FULL", "Waitl", "NewOnly"}
    if not any(s in data["status"] for s in valid_statuses):
        print(f"[WARN] Unexpected status value: {data['status']}")
        return False

    return True


def is_open(data: dict) -> bool:
    """Returns True if the course has open spots."""
    return "OPEN" in data.get("status", "")
