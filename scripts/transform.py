"""Stage 2 (transform): add a ``date`` column (YYYY-MM-DD)."""

import csv
import os
import sys


def main(src: str, dst: str) -> None:
    with open(src, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = [*(reader.fieldnames or []), "date"]
        rows = [{**row, "date": row["timestamp"][:10]} for row in reader]
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    with open(dst, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"transform: wrote {len(rows)} rows")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
