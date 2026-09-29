"""
LangGraph-style analyst graph (teaching simulation).
Nodes: retrieve -> validate_freshness -> answer
NO live LLM API keys — deterministic retriever + templates.
Optional real LLM stub in llm_stub.py (disabled by default).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "finance_transactions.csv"
META = ROOT / "data" / "dataset_freshness.json"


@dataclass
class AnalystState:
    question: str
    rows: list[dict] = field(default_factory=list)
    freshness_ok: bool = False
    answer: str = ""


def node_retrieve(state: AnalystState) -> AnalystState:
    df = pd.read_csv(DATA)
    q = state.question.lower()
    if "payroll" in q:
        filt = df[df["account"] == "PAYROLL"]
    elif "operating" in q:
        filt = df[df["account"] == "OPERATING"]
    elif "fee" in q:
        filt = df[df["category"] == "FEE"]
    else:
        filt = df.nlargest(5, "amount_usd")
    state.rows = filt.head(10).to_dict(orient="records")
    return state


def node_validate_freshness(state: AnalystState) -> AnalystState:
    meta = json.loads(META.read_text(encoding="utf-8"))
    refreshed = datetime.fromisoformat(meta["last_refreshed_utc"])
    age_days = (datetime.now(timezone.utc) - refreshed).days
    state.freshness_ok = age_days <= 7
    return state


def node_answer(state: AnalystState) -> AnalystState:
    if not state.freshness_ok:
        state.answer = "Template: dataset freshness check FAILED — refresh finance_transactions.csv."
        return state
    total = sum(r.get("amount_usd", 0) for r in state.rows)
    state.answer = (
        f"Template analyst answer for '{state.question}': retrieved {len(state.rows)} rows; "
        f"sum(amount_usd)={total:,.2f}. (Simulation — no LLM API call.)"
    )
    return state


GraphStep = Callable[[AnalystState], AnalystState]


class TeachingGraph:
    def __init__(self, steps: list[GraphStep]) -> None:
        self.steps = steps

    def invoke(self, state: AnalystState) -> AnalystState:
        for step in self.steps:
            state = step(state)
        return state


def build_graph() -> TeachingGraph:
    return TeachingGraph([node_retrieve, node_validate_freshness, node_answer])


def main() -> None:
    graph = build_graph()
    for q in ["Summarize payroll activity", "What are the largest operating amounts?"]:
        out = graph.invoke(AnalystState(question=q))
        print(f"Q: {q}\nA: {out.answer}\n")


if __name__ == "__main__":
    main()
