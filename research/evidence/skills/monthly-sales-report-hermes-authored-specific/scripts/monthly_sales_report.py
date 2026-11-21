#!/usr/bin/env python3
"""Generate and validate a monthly sales report in a salesops workspace."""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

VALID_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
STATUSES = {"completed", "cancelled", "refunded", "pending"}


def jpy_round(value):
    return int((value / Decimal(1000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 1000)


def generate(month, root=Path.cwd()):
    source = root / "data" / f"sales_{month}.csv"
    rate_file = root / "config" / "rates.json"
    if not source.is_file() or not rate_file.is_file():
        raise ValueError(f"Required input missing: {source} or {rate_file}")
    rates = json.loads(rate_file.read_text(encoding="utf-8"))
    rate = Decimal(str(rates["USD_JPY"]))
    totals = defaultdict(Decimal)
    counts = defaultdict(int)
    with source.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"date", "region", "category", "amount", "currency", "status"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV is missing required columns")
        for line, row in enumerate(reader, start=2):
            if not row["date"].startswith(month + "-"):
                raise ValueError(f"Line {line}: date does not belong to {month}")
            if row["status"] not in STATUSES:
                raise ValueError(f"Line {line}: unknown status {row['status']!r}")
            if row["currency"] not in {"JPY", "USD"}:
                raise ValueError(f"Line {line}: unsupported currency {row['currency']!r}")
            try:
                amount = Decimal(row["amount"])
            except Exception as e:
                raise ValueError(f"Line {line}: invalid amount") from e
            if amount < 0:
                raise ValueError(f"Line {line}: negative amount")
            if row["status"] == "completed":
                category = row["category"]
                if not category:
                    raise ValueError(f"Line {line}: empty category")
                totals[category] += amount * (rate if row["currency"] == "USD" else 1)
                counts[category] += 1
    rounded = {k: jpy_round(v) for k, v in totals.items()}
    ordered = sorted(rounded.items(), key=lambda kv: (-kv[1], kv[0]))
    grand = sum(v for _, v in ordered)
    findings = [
        f"Included {sum(counts.values())} completed transactions; excluded all non-completed rows.",
        f"Top category by rounded sales was {ordered[0][0]} ({ordered[0][1]} JPY)." if ordered else "No completed sales were recorded.",
        f"Sales covered {len(ordered)} categories; grand total is the sum of rounded category totals ({grand} JPY).",
    ]
    lines = [f"# Sales report {month}", ""]
    lines.extend(f"CATEGORY:{name}={value}" for name, value in ordered)
    lines.extend([f"GRAND_TOTAL_JPY={grand}", "", "## Findings"])
    lines.extend(f"- {item}" for item in findings)
    content = "\n".join(lines) + "\n"
    validate(content, month, ordered, grand)
    target = root / "out" / f"report_{month}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    validate(target.read_text(encoding="utf-8"), month, ordered, grand)
    return target


def validate(content, month, ordered, grand):
    lines = content.splitlines()
    if not lines or lines[0] != f"# Sales report {month}":
        raise ValueError("Invalid report title")
    if lines.count("## Findings") != 1 or lines[-1:] == [""]:
        raise ValueError("Invalid Findings section")
    idx = lines.index("## Findings")
    expected_categories = [f"CATEGORY:{k}={v}" for k, v in ordered]
    actual_categories = [line for line in lines if line.startswith("CATEGORY:")]
    if actual_categories != expected_categories:
        raise ValueError("Category lines or descending order do not validate")
    if lines.count(f"GRAND_TOTAL_JPY={grand}") != 1:
        raise ValueError("Grand total does not validate")
    bullets = [line for line in lines[idx + 1:] if line.startswith("- ")]
    if len(bullets) != 3 or len(lines[idx + 1:]) != 3:
        raise ValueError("Findings must contain exactly three bullets")
    for line in actual_categories + [f"GRAND_TOTAL_JPY={grand}"]:
        if not re.fullmatch(r"(?:CATEGORY:[^=]+|GRAND_TOTAL_JPY)=\d+", line):
            raise ValueError(f"Invalid numeric line: {line}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("month", help="Reporting month in YYYY-MM format")
    args = parser.parse_args()
    if not VALID_MONTH.fullmatch(args.month):
        parser.error("month must be a valid YYYY-MM")
    try:
        output = generate(args.month)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"Generated and validated {output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
