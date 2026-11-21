"""合成 Skill を HERMES_HOME/skills/lab-synth/ に N 個作る。一覧（索引）の伸び方を測るため。"""
import sys, pathlib
home, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
for i in range(n):
    d = home / "skills" / "lab-synth" / f"monthly-report-variant-{i:04d}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"""---
name: monthly-report-variant-{i:04d}
description: Build the monthly sales report for region {i:04d} from the CSV export, validate totals, and write the summary in the house format.
version: 1.0.0
---
# Monthly report variant {i:04d}

1. Read `sales_{i:04d}.csv`.
2. Sum `amount` by `category`.
3. Write `report_{i:04d}.md` with a table and three bullet findings.
""")
