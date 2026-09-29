from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
(DATA / "questions.json").write_text(json.dumps([
    {"qid": "Q1", "text": "What was yesterday's gross margin?"},
    {"qid": "Q2", "text": "What will margin be next quarter?"}
], indent=2), encoding="utf-8")
print("questions ready")
