

# evals_intro

**A from-scratch introduction to AI evaluation harnesses — built by doing, not by reading frameworks.**

This repo contains a practical essay and working Python code for understanding how to evaluate AI systems in production. Built around a support ticket triage use case.

------

## What's in here

| File                   | What it does                                                 |
| ---------------------- | ------------------------------------------------------------ |
| `Evals Intro Essay.md` | Conceptual walkthrough — ground truth, confusion matrix, metrics, use-case mapping |
| `eval_core.py`         | Batch eval harness — runs a dataset through AI, computes precision/recall/consistency |
| `prod_eval_hitl.py`    | Live HITL eval runner — one ticket at a time, human labels in real time |
| `run_interactive.py`   | Entry point for interactive mode                             |
| `run_preloaded.py`     | Entry point for batch/preloaded dataset mode                 |
| `*.json`               | Example eval run outputs — timestamped sessions with metrics and results |

------

## Core concepts covered

**Ground Truth** — Human-labelled benchmarks. Without these, you're just comparing AI to itself.

**Confusion Matrix**

|                 | AI: Flag            | AI: OK              |
| --------------- | ------------------- | ------------------- |
| **Truth: Flag** | True Positive (TP)  | False Negative (FN) |
| **Truth: OK**   | False Positive (FP) | True Negative (TN)  |

**Metrics**

- `Recall = TP / (TP + FN)` — minimise FN; use for safety-critical cases (fraud, medical, legal)
- `Precision = TP / (TP + FP)` — minimise FP; use for UX-critical cases (spam filters, recommendations)
- `F1 = 2 * (P * R) / (P + R)` — penalises imbalance between precision and recall
- `Reason Consistency` — % of cases where AI reason category matches human label; tracks drift over time

**Metric selection by use case**

| Use Case              | Minimise | Why                                 |
| --------------------- | -------- | ----------------------------------- |
| Credit card fraud     | FN       | Missing fraud = real financial loss |
| Email spam filter     | FP       | Legit emails in junk = trust broken |
| Contract risk review  | FN       | Missed clause = legal liability     |
| Support ticket triage | FN       | Missed P1 = production down         |
| Content moderation    | FN       | Wrong-age content = serious harm    |

Rule of thumb: **Safety-critical → minimise FN. UX-critical → minimise FP. Business tradeoff → cost model decides.**

------

## How to run

### Prerequisites

```bash
pip install httpx
```

Set your OpenRouter API key in the relevant `.py` file (replace `"Bearer KEY HERE"`).

> ⚠️ Never commit real API keys. Use environment variables in any real project.

### Batch eval (preloaded dataset)

```bash
python run_preloaded.py
```

Runs a fixed set of pre-labelled tickets through the AI and outputs metrics + a timestamped JSON file.

### Live HITL eval (one ticket at a time)

```bash
python run_interactive.py
```

You enter a ticket title → AI predicts → you provide ground truth → repeat until `done` → metrics calculated and saved.

------

## What the output looks like

```json
{
  "evaluation_completed_at": "2026-05-30T17:14:59",
  "summary_metrics": {
    "precision": 0.91,
    "recall": 0.88,
    "reason_consistency": 0.75
  },
  "total_items_evaluated": 12,
  "results": [...]
}
```

------

## Why this exists

Most evals content either throws you into a framework (Ragas, LangSmith) or stays at the theory level. This is the gap in between — understanding what the numbers mean and writing the harness yourself before you trust a library to do it for you.

The support ticket example is intentional: it's a real-world AI agent use case where getting FN wrong means production is down.

------

## What's next

- [ ] Threshold sweep — vary decision boundary, plot precision-recall curve
- [ ] Multi-label support (beyond binary flag/ok)
- [ ] LLM-as-judge consistency variant

------

## Author

Built by [productiser](https://github.com/productiser) as part of a practical AI skills sprint.
