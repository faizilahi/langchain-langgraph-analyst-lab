import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from graph import GRAPH_NODES
from cite import load_metrics, answer
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    metrics = load_metrics(ROOT / "catalog" / "metrics.json")
    questions = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    rows = []
    for q in questions:
        r = answer(q["text"], metrics)
        rows.append({"qid": q["qid"], "question": q["text"], **r, "nodes": "->".join(GRAPH_NODES)})
    pd.DataFrame(rows).to_csv(OUT / "graph_answers.csv", index=False)
    print(json.dumps(rows, indent=2))
if __name__ == "__main__":
    main()
