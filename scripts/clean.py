"""Stage 1 (clean): drop bad rows and normalise timestamps to ISO 8601."""

import csv
import os
import sys
from datetime import datetime

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)


def parse_timestamp(text: str) -> datetime | None:
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def parse_duration(text: str) -> int | None:
    try:
        return int(float(text))
    except ValueError:
        return None


def clean_row(row: dict[str, str]) -> dict[str, str] | None:
    if any(value is None or value.strip() == "" for value in row.values()):
        return None
    event_type = row["event_type"].strip()
    if event_type not in VALID_EVENT_TYPES:
        return None
    duration = parse_duration(row["duration_seconds"].strip())
    if duration is None or duration <= 0:
        return None
    timestamp = parse_timestamp(row["timestamp"].strip())
    if timestamp is None:
        return None
    return {
        "user_id": row["user_id"].strip(),
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
        "event_type": event_type,
        "duration_seconds": str(duration),
    }


def main(src: str, dst: str) -> None:
    with open(src, newline="") as f:
        rows = list(csv.DictReader(f))
    cleaned = [r for r in map(clean_row, rows) if r is not None]
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    with open(dst, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["user_id", "timestamp", "event_type", "duration_seconds"]
        )
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"clean: kept {len(cleaned)} of {len(rows)} rows")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
