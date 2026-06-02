from datetime import datetime
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from a .env file if present

api_key = os.getenv("OPENROUTER_API_KEY")


# =====================================================================
# 1. CORE AI COMPLETION INFRASTRUCTURE
# =====================================================================
def predict_single_ticket(ticket_title):
    """Calls OpenRouter to predict a single ticket on the fly."""
    url = "https://openrouter.ai/api/v1/chat/completions"

    json_data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"Classify the following support decision as 'flag' or 'ok'. "
                f"Assign a reason for each decision from security, financial impact, "
                f"executive escalation, service outage, account access, and compliance. "
                f"If reason is not listed, state a different reason. Do not include any . Priority is P1-P4 with P1 being the most severe. Do not include any other."
                f"other text or explanations in the response or fields. Return JSON only "
                f"with 3 fields aireason, aipriority, and aidecision: {ticket_title}",
            }
        ],
        "response_format": {"type": "json_object"},
    }

    try:
        r = httpx.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",  # Replace with your actual key safely
            },
            json=json_data,
        )
        response = r.json()
        content = response["choices"][0]["message"]["content"].strip()

        if content.startswith("```"):
            content = content.strip("```").replace("json", "", 1).strip()

        data = json.loads(content)
        return (
            data["aidecision"].strip().lower(),
            data["aireason"].strip().lower(),
            data["aipriority"].strip().upper(),
        )

    except Exception as e:
        print(f"   ⚠️ Error communicating with AI: {e}")
        return "error", "api failed"


# =====================================================================
# 2. CORE CONFUSION MATRIX MATH FUNCTION
# =====================================================================
def calculate_evaluation_metrics(tickets):
    """Calculates True/False Positives/Negatives, Precision, Recall, and F1."""
    tp = fp = tn = fn = 0

    for t in tickets:
        ai = t["aidecision"]
        truth = t["truth"]

        if ai == "flag" and truth == "flag":
            tp += 1
        elif ai == "flag" and truth == "ok":
            fp += 1
        elif ai == "ok" and truth == "ok":
            tn += 1
        elif ai == "ok" and truth == "flag":
            fn += 1

    # Safe division helpers to prevent ZeroDivisionError
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
        },
        "f1_score": round(f1_score, 3),
    }


# =====================================================================
# 3. DATA SAVING ENGINE
# =====================================================================
def save_batch_evaluation(trials, metrics, filename_prefix="eval_session"):
    """Saves everything into a single timestamped JSON file."""
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")

    evaluation_packet = {
        "evaluation_completed_at": datetime.now().isoformat(),
        "summary_metrics": metrics,
        "total_items_evaluated": len(trials),
        "results": trials,
    }

    filename = f"{filename_prefix}_{timestamp_file}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(evaluation_packet, f, indent=4, ensure_ascii=False)

    print(f"\n[SUCCESS] Entire session saved safely to: {filename}")


# =====================================================================
# 4. MAIN INTERACTIVE EXECUTION FLOW
# =====================================================================
if __name__ == "__main__":
    session_tickets = []

    print("\n==================================================")
    print("📋 LIVE LIFECYCLE EVALUATION RUNNER")
    print("==================================================")
    print("Process tickets one by one. Type 'done' to stop and calculate.")

    while True:
        # Step 1: User enters ticket title for *each* one
        user_title = input("\nEnter issue/title: ").strip()

        if user_title.lower() == "done":
            break
        if not user_title:
            continue

        # Step 2: Runs the AI immediately on this single ticket
        print("   🤖 Running AI prediction...")
        ai_decision, ai_reason, ai_priority = predict_single_ticket(user_title)

        print(f"\n   [AI Result]")
        print(f"   -> Decision: {ai_decision.upper()}")
        print(f"   -> Reason:   {ai_reason}")
        print(f"   -> Priority: {ai_priority}")
        print("   -----------------------------------------------")

        # Step 3: Hand over to the user to evaluate / validate right away
        while True:
            user_truth = input("   👤 Enter ground truth (flag/ok): ").strip().lower()
            if user_truth in ["flag", "ok"]:
                break
            print("   ⚠️ Please enter exactly 'flag' or 'ok'.")

        user_reason = input("   👤 Enter human category reason: ").strip().lower()
        print("==================================================")

        # Append data to the running session array
        session_tickets.append(
            {
                "title": user_title,
                "aidecision": ai_decision,
                "aireason": ai_reason,
                "ai_priority": ai_priority,
                "truth": user_truth,
                "reason": user_reason,
            }
        )

    # Step 4 & 5: When 'done' is hit, execute core stats and save the whole session
    if session_tickets:
        print("\n📊 Session finished. Calculating confusion matrix stats...")

        # Run core matrix calculation
        final_metrics = calculate_evaluation_metrics(session_tickets)

        # Print quick recap to console
        print(f"   - Recall:    {final_metrics['recall']}")
        print(f"   - F1-Score:  {final_metrics['f1_score']}")

        # Save everything to a single file
        save_batch_evaluation(
            session_tickets, final_metrics, filename_prefix="consistency_session"
        )
    else:
        print("\nNo tickets processed. Goodbye!")
