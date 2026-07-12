"""
evaluate.py
-----------
Runs the grammar-based QueryParser over every query in data/queries.json,
compares the predicted category to the gold label, and reports overall +
per-category accuracy. Results are written to results/evaluation_results.csv
for inclusion in the project report.
"""
import json
import csv
from collections import defaultdict
from grammar.parser import QueryParser
from responses.response_bank import generate_response


def main():
    with open("data/queries.json") as f:
        dataset = json.load(f)

    qp = QueryParser()
    rows = []
    correct = 0
    per_cat_total = defaultdict(int)
    per_cat_correct = defaultdict(int)

    for item in dataset:
        result = qp.parse(item["text"])
        is_correct = result.category == item["category"]
        correct += int(is_correct)
        per_cat_total[item["category"]] += 1
        per_cat_correct[item["category"]] += int(is_correct)
        response = generate_response(result)
        rows.append({
            "id": item["id"],
            "text": item["text"],
            "gold_category": item["category"],
            "predicted_category": result.category,
            "confidence": result.confidence,
            "correct": is_correct,
            "matched_keywords": ";".join(result.matched_keywords),
            "simulated_response": response,
        })

    accuracy = correct / len(dataset)

    with open("results/evaluation_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Overall accuracy: {correct}/{len(dataset)} = {accuracy:.2%}\n")
    print(f"{'Category':28s} {'Correct/Total':15s} {'Accuracy':10s}")
    print("-" * 55)
    for cat in sorted(per_cat_total):
        c, t = per_cat_correct[cat], per_cat_total[cat]
        print(f"{cat:28s} {f'{c}/{t}':15s} {c/t:.0%}")

    misclassified = [r for r in rows if not r["correct"]]
    if misclassified:
        print(f"\nMisclassified ({len(misclassified)}):")
        for r in misclassified:
            print(f"  [{r['id']}] gold={r['gold_category']} pred={r['predicted_category']} :: {r['text']}")
    else:
        print("\nNo misclassifications.")

    return accuracy


if __name__ == "__main__":
    main()
