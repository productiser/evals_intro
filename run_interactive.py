from eval_core import evaluate_tickets, save_batch_evaluation
import json

if __name__ == "__main__":

    user_tickets = []
    print("\n--- Interactive Evaluation Data Collector ---")
    print("Type 'done' when you are finished entering test cases.")

    while True:
        user_title = input("\nEnter issue/title: ").strip()
        if user_title.lower() == "done":
            break
        if not user_title:
            continue
        user_truth = input("Enter truth value (flag/ok): ").strip()
        user_reason = input(
            "Enter reason (security, financial impact, executive escalation, service outage, account access, compliance, or other): "
        ).strip()

        user_tickets.append(
            {"title": user_title, "truth": user_truth, "reason": user_reason}
        )
    # If the user actually entered data, evaluate and save it
    if user_tickets:
        trials, metrics = evaluate_tickets(user_tickets)
        save_batch_evaluation(trials, metrics, filename_prefix="user_eval_run")
    else:
        print("No data entered. Exiting.")
