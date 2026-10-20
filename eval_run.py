"""Run the 25-question eval set and write eval/report.md and eval/results.json.

Usage:
  python eval_run.py --retrieval-only   # no API key needed; tests retrieval alone
  python eval_run.py                    # full run: retrieval + Claude answers
"""
import argparse
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent
QUESTIONS = ROOT / "eval" / "questions.json"
RESULTS = ROOT / "eval" / "results.json"
REPORT = ROOT / "eval" / "report.md"
TOP_K = 4


def contains_term(text: str, term: str) -> bool:
    """Whole-term match, so "3" does not match "13:00" or "1.3", and "75" does not match "175"."""
    pattern = r"(?<![\w.])" + re.escape(term) + r"(?![\w])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def grade_answer(item: dict, text: str, cited: list[str], refused: bool,
                 gold_pages: set[str], retrieved_refs: set[str]) -> dict:
    """Score one answer. Returns the checks plus a failure label if any check failed.

    Citation rule: every cited page must have been retrieved, and at least one must be a
    gold page. A correct answer that also cites a second retrieved page that supports a
    claim is not penalised.
    """
    leaked = [f for f in item["forbidden"] if contains_term(text, f)]

    if not text.strip():
        # Usually means the token limit ran out before any text was written.
        return {"correct": False, "citation_ok": False, "label": "empty-answer", "leaked": []}

    if item["must_refuse"]:
        correct = refused and not leaked
        citation_ok = None
    else:
        correct = (not refused) and all(contains_term(text, k) for k in item["must_contain"]) and not leaked
        cited_set = set(cited)
        citation_ok = bool(cited_set) and cited_set <= retrieved_refs and bool(cited_set & gold_pages)

    if correct and citation_ok is not False:
        label = "pass"
    elif leaked:
        label = "access-or-stale-leak" if item["category"] in ("access-denied", "conflicting-or-stale") else "wrong-content"
    elif item["must_refuse"]:
        label = "answered-without-evidence"
    elif refused:
        label = "refused-answerable"
    elif citation_ok is False:
        label = "citation-error"
    else:
        label = "wrong-answer"
    return {"correct": correct, "citation_ok": citation_ok, "label": label, "leaked": leaked}


def run(retrieval_only: bool) -> dict:
    from rag import answer, retrieve, Answer

    items = json.loads(QUESTIONS.read_text())
    rows = []
    for item in items:
        gold = set(item["gold"])
        if retrieval_only:
            hits, retrieval_ms = retrieve(item["question"], item["role"], TOP_K)
            retrieved_refs = {h.ref for h in hits}
            row = {
                "id": item["id"], "category": item["category"], "role": item["role"],
                "question": item["question"], "gold": sorted(gold),
                "retrieved": [h.ref for h in hits],
                "retrieval_hit": bool(gold) and gold <= retrieved_refs,
                "retrieval_ms": round(retrieval_ms, 1),
            }
        else:
            result: Answer = answer(item["question"], item["role"], TOP_K)
            retrieved_refs = {h.ref for h in result.retrieved}
            graded = grade_answer(item, result.text, result.citations, result.refused, gold, retrieved_refs)
            row = {
                "id": item["id"], "category": item["category"], "role": item["role"],
                "question": item["question"], "gold": sorted(gold),
                "must_refuse": item["must_refuse"],
                "retrieved": [h.ref for h in result.retrieved],
                "retrieval_hit": bool(gold) and gold <= retrieved_refs,
                "answer": result.text, "citations": result.citations,
                "refused": result.refused,
                "retrieval_ms": round(result.retrieval_ms, 1),
                "generation_ms": round(result.generation_ms, 1),
                "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                **graded,
            }
            # A failed answer is a retrieval failure when the gold page never reached the model.
            if not graded["correct"] and gold and not row["retrieval_hit"]:
                row["label"] = "retrieval-failure"
        rows.append(row)
        status = row.get("label", "retrieved" if row["retrieval_hit"] else ("refusal-item" if not gold else "retrieval-miss"))
        print(f"{item['id']:>2} {item['category']:<22} {status}")
    return {"mode": "retrieval-only" if retrieval_only else "full", "rows": rows}


def summarise(results: dict) -> dict:
    rows = results["rows"]
    answerable = [r for r in rows if r["gold"]]
    summary = {
        "questions": len(rows),
        "recall_at_4": sum(r["retrieval_hit"] for r in answerable) / len(answerable),
    }
    if results["mode"] == "full":
        scored = [r for r in rows if "correct" in r]
        summary["answer_accuracy"] = sum(r["correct"] for r in scored) / len(scored)
        cited = [r for r in scored if r["citation_ok"] is not None]
        summary["citation_correctness"] = sum(r["citation_ok"] for r in cited) / len(cited)
        refusal_items = [r for r in scored if r["must_refuse"]]
        summary["refusal_accuracy"] = sum(r["correct"] for r in refusal_items) / len(refusal_items)
        summary["median_retrieval_ms"] = round(statistics.median(r["retrieval_ms"] for r in rows), 1)
        summary["median_generation_ms"] = round(statistics.median(r["generation_ms"] for r in scored), 1)
        summary["total_input_tokens"] = sum(r["input_tokens"] for r in scored)
        summary["total_output_tokens"] = sum(r["output_tokens"] for r in scored)
    return summary


def write_report(results: dict, summary: dict) -> None:
    lines = [f"# Eval report ({results['mode']})", "", "## Summary", ""]
    for k, v in summary.items():
        val = f"{v:.0%}" if isinstance(v, float) and v <= 1 and k.endswith(("recall_at_4", "accuracy", "correctness")) else v
        lines.append(f"- **{k}**: {val}")
    lines += ["", "## Per question", "", "| # | Category | Role | Retrieved | Hit | Result |", "|---|---|---|---|---|---|"]
    for r in results["rows"]:
        result = r.get("label", "retrieved" if r["retrieval_hit"] else "retrieval-miss")
        hit = "yes" if r["retrieval_hit"] else ("n/a" if not r["gold"] else "no")
        lines.append(f"| {r['id']} | {r['category']} | {r['role']} | {', '.join(r['retrieved'])} | {hit} | {result} |")
    failures = [r for r in results["rows"] if r.get("label") not in (None, "pass")]
    if failures:
        lines += ["", "## Failures", ""]
        for r in failures:
            lines += [f"### Q{r['id']}: {r['question']}", f"- Label: `{r['label']}`",
                      f"- Gold: {', '.join(r['gold']) or 'none (should refuse)'}",
                      f"- Retrieved: {', '.join(r['retrieved'])}"]
            if "answer" in r:
                lines.append(f"- Answer: {r['answer']}")
            lines.append("")
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrieval-only", action="store_true")
    args = parser.parse_args()

    if not args.retrieval_only:
        from rag import require_api_key
        require_api_key()

    results = run(args.retrieval_only)
    summary = summarise(results)
    RESULTS.write_text(json.dumps({"summary": summary, **results}, indent=2))
    write_report(results, summary)
    print(json.dumps(summary, indent=2))
    print(f"wrote {REPORT.relative_to(ROOT)} and {RESULTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
