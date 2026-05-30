from eval_core import evaluate_tickets, save_batch_evaluation
import json

# Preloaded mock dataset (Your fixed consistency test-bed)

if __name__ == "__main__":
    print("Running preloaded evaluation dataset...")

    # Your fixed, preloaded test-bed matching your exact shape
    tickets = [
        {
            "title": "My payment failed twice and I was charged both times.",
            "reason": "financial impact",
            "rationale": "potential fraud",
            "truth": "flag",
        },
        {
            "title": "How can I reset my password?",
            "reason": "account access",
            "rationale": "user request",
            "truth": "ok",
        },
        {
            "title": "My laptop wont start and I need to give a CTO presentation by EOD.",
            "reason": "service outage",
            "rationale": "potential escalation",
            "truth": "flag",
        },
        {
            "title": "I am unable to access some sites from my office network, but I can access them from home.",
            "reason": "account access",
            "rationale": "potential blocking of sites on office network",
            "truth": "ok",
        },
        {
            "title": "I clicked on a spam email and now my computer is acting weird.",
            "reason": "security",
            "rationale": "potential threat",
            "truth": "flag",
        },
    ]
    completed_tickets, metrics = evaluate_tickets(tickets)
    save_batch_evaluation(
        completed_tickets, metrics, filename_prefix="preloaded_eval_run"
    )
