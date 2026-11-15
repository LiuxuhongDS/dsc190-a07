"""Stage 3 (features): add ``duration_minutes`` and ``weekday`` columns."""

import csv
import sys
from datetime import date

WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def main(src: str, dst: str) -> None:
    with open(src, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = [*(reader.fieldnames or []), "duration_minutes", "weekday"]
        rows = []
        for row in reader:
            rows.append(
                {
                    **row,
                    "duration_minutes": int(row["duration_seconds"]) / 60,
                    "weekday": WEEKDAY_NAMES[date.fromisoformat(row["date"]).weekday()],
                }
            )
    with open(dst, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"features: wrote {len(rows)} rows")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
