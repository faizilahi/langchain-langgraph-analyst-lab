from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(21)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/finance_transactions.csv"))
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    accounts = ["OPERATING", "PAYROLL", "CAPITAL"]
    rows = []
    now = datetime.now(timezone.utc)
    for i in range(800):
        rows.append(
            {
                "txn_id": f"T{i:05d}",
                "account": RNG.choice(accounts),
                "amount_usd": round(float(RNG.uniform(-50000, 120000)), 2),
                "category": RNG.choice(["AP", "AR", "TRANSFER", "FEE"]),
                "posted_at": (now - timedelta(days=int(RNG.integers(0, 45)))).isoformat(),
            }
        )
    pd.DataFrame(rows).to_csv(args.out, index=False)
    meta = args.out.with_name("dataset_freshness.json")
    meta.write_text('{"last_refreshed_utc": "' + now.isoformat() + '"}', encoding="utf-8")
    print(f"Wrote {args.out} and {meta}")


if __name__ == "__main__":
    main()
