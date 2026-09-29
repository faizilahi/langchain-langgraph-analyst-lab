import json
from pathlib import Path

def load_metrics(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8"))["metrics"]

def answer(question: str, metrics: list) -> dict:
    q = question.lower()
    if "next quarter" in q or "will margin" in q:
        return {"status": "ABSTAIN", "reason": "ABSTAIN: no metric_id", "metric_id": None, "value": None}
    if "gross margin" in q or "margin" in q:
        m = next(x for x in metrics if x["metric_id"] == "M_GM_PCT")
        return {"status": "OK", "metric_id": m["metric_id"], "value": m["value"], "citation": m["metric_id"]}
    return {"status": "ABSTAIN", "reason": "ABSTAIN: no metric_id", "metric_id": None, "value": None}
