# Graph That Must Cite a Metric Id or Abstain

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A LangGraph-style analyst graph answers KPI questions only when it can cite a
`metric_id` from the certified catalog. Otherwise it abstains.

## The graph

Nodes: `retrieve_metrics` → `draft` → `cite_or_abstain` → `emit`.

## The citation

Question "What was yesterday's gross margin?" cites `metric_id=M_GM_PCT` with
value **24.12%**.

## The abstain path

Question "What will margin be next quarter?" has no certified forecast metric →
`ABSTAIN: no metric_id`.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_graph.py
```
