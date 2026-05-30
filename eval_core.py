import httpx
import json
import datetime
import os


def save_batch_evaluation(trials, metrics, filename_prefix="eval_run"):
    timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp_iso = datetime.datetime.now().isoformat()
    evaluation_packet = {
        "evaluation_completed_at": timestamp_iso,
        "summary_metrics": metrics,  # e.g., {"precision": 0.92, "accuracy": 0.94}
        "total_items_evaluated": len(trials),
        "results": trials,  # Your array of dicts
    }
    filename = f"{filename_prefix}_{timestamp_file}.json"
    with open(filename, "w", encoding="utf-8") as f:
        # indent=4 makes it human-readable if you open the file directly
        json.dump(evaluation_packet, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved evaluation to: {filename}")


def evaluate_tickets(tickets):
    url = "https://openrouter.ai/api/v1/chat/completions"
    tp = fp = fn = tn = 0
    reasonmatches = 0
    for ticket in tickets:
        json_data = {
            "model": "~openai/gpt-mini-latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"Classify the following support decision as 'flag' or 'ok'. Assign a reason for each decision from security, financial impact, executive escalation, service outage, account access, and compliance. If reason is not listed, state a different reason. Don not include any other text or explanations in the response or fields. Return JSON only with 2 fields aireason and aidecision: {ticket['title']}",
                }
            ],
        }
        r = httpx.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-KEYHERE",
            },
            json=json_data,
        )

        response = r.json()
        content = response["choices"][0]["message"]["content"].strip().lower()
        data = json.loads(content)
        ticket["aidecision"] = data["aidecision"]
        ticket["aireason"] = data["aireason"]
        print(
            f"Ticket ID: Truth: {ticket['truth']} - AI Classification: {ticket['aidecision']} - AI Reason: {ticket['aireason']}\n"
        )

        if ticket["truth"] == "flag" and ticket["aidecision"] == "flag":
            tp += 1
        elif ticket["truth"] == "flag" and ticket["ai"] == "ok":
            fn += 1
        elif ticket["truth"] == "ok" and ticket["aidecision"] == "flag":
            fp += 1
        elif ticket["truth"] == "ok" and ticket["aidecision"] == "ok":
            tn += 1

        if ticket["reason"] == ticket["aireason"]:
            reasonmatches += 1

        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        consistency = reasonmatches / len(tickets) if len(tickets) > 0 else 0

        metrics = {
            "recall": recall,
            "precision": precision,
            "reason_consistency": consistency,
        }
    print(f"Completed evaluation of {len(tickets)} tickets.")
    print(
        f"Final Metrics: Recall: {metrics['recall']*100:.2f}%, Precision: {metrics['precision']*100:.2f}%, Reason Consistency: {metrics['reason_consistency']*100:.2f}%\n"
    )
    return tickets, metrics
