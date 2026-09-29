from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)
p = ROOT / "data" / "finance_transactions.csv"
if p.exists():
    df = pd.read_csv(p)
    agg = df.groupby("account")["amount_usd"].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    agg.plot(kind="bar", ax=ax, color="#10B981")
    ax.set_title("Finance dataset by account (synthetic)")
    fig.tight_layout()
    fig.savefig(OUT / "account_totals.png", dpi=120)
    plt.close(fig)
