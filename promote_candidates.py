"""Move candidates a person has approved into eval/questions.json.

Review eval/candidates.json first. Set "status" to "approved" for keepers and
"rejected" for the rest, and edit any wording or key facts that are wrong.
Only items marked "approved" are promoted. Each promoted item is marked "promoted"
so a second run doesn't add it again.

Usage: python promote_candidates.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
CANDIDATES = ROOT / "eval" / "candidates.json"
QUESTIONS = ROOT / "eval" / "questions.json"
HELPER_FIELDS = {"cand_id", "status", "source", "passage"}


def main() -> None:
    candidates = json.loads(CANDIDATES.read_text())
    questions = json.loads(QUESTIONS.read_text())
    next_id = max(q["id"] for q in questions) + 1

    promoted = 0
    for c in candidates:
        if c["status"] != "approved":
            continue
        item = {k: v for k, v in c.items() if k not in HELPER_FIELDS}
        item["id"] = next_id
        item["category"] = c["category"]
        questions.append(item)
        c["status"] = "promoted"
        next_id += 1
        promoted += 1

    QUESTIONS.write_text(json.dumps(questions, indent=2))
    CANDIDATES.write_text(json.dumps(candidates, indent=2))
    counts = {}
    for c in candidates:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    print(f"promoted {promoted} item(s); candidate status counts: {counts}")
    print(f"eval/questions.json now has {len(questions)} questions")


if __name__ == "__main__":
    main()
