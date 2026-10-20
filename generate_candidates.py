"""Draft candidate eval questions from the indexed chunks.

Writes eval/candidates.json. Every candidate starts as "pending". Nothing reaches
eval/questions.json until a person sets its status to "approved" and runs
promote_candidates.py.

Usage: python generate_candidates.py
Needs ANTHROPIC_API_KEY in the environment.
"""
import json
import re
from pathlib import Path

from ingest import build_chunks
from rag import ANSWER_MODEL, require_api_key

ROOT = Path(__file__).parent
MANIFEST = ROOT / "corpus" / "manifest.json"
OUT = ROOT / "eval" / "candidates.json"
ROLE_FOR_TAG = {"all": "all", "hr": "hr", "finance": "finance", "security": "security"}
QUESTIONS_PER_CHUNK = 2
REFUSAL_QUESTIONS = 8

SYSTEM = "You write test questions for a policy-search evaluation. Reply with JSON only, no commentary."


def ask(client, prompt: str) -> list:
    resp = client.messages.create(
        model=ANSWER_MODEL,
        max_tokens=1200,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    # Tolerate a fenced code block around the JSON.
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)


def answerable_prompt(ref: str, title: str, passage: str) -> str:
    return (
        f"Passage from {ref} ({title}):\n{passage}\n\n"
        f"Write {QUESTIONS_PER_CHUNK} questions a company employee might ask that this passage fully answers. "
        "Use plain, natural wording and do not copy sentences from the passage. "
        "For each question give key_facts: one to three short words or numbers the correct answer must include, "
        "copied exactly from the passage. "
        'Return a JSON list of objects with keys "question" and "key_facts".'
    )


def refusal_prompt(titles: list[str]) -> str:
    return (
        "The company's documents cover these topics:\n- " + "\n- ".join(titles) + "\n\n"
        f"Write {REFUSAL_QUESTIONS} questions an employee might ask that these documents do NOT answer. "
        'Return a JSON list of objects with the key "question".'
    )


def main() -> None:
    require_api_key()
    import anthropic

    client = anthropic.Anthropic()
    manifest = json.loads(MANIFEST.read_text())
    titles = [d["title"] for d in manifest["documents"] if d["status"] == "current"]

    candidates = []
    for chunk in build_chunks():
        meta = chunk["metadata"]
        if meta["status"] != "current":
            continue  # superseded text is never a source for a question
        ref = f"{meta['doc_id']} p{meta['page']}"
        for item in ask(client, answerable_prompt(ref, meta["title"], chunk["text"])):
            candidates.append({
                "status": "pending",
                "source": "generated",
                "category": "generated-factual",
                "role": ROLE_FOR_TAG[meta["access"]],
                "question": item["question"],
                "gold": [ref],
                "must_contain": item["key_facts"],
                "forbidden": [],
                "must_refuse": False,
                "passage": chunk["text"],
            })
        print(f"{ref}: drafted {QUESTIONS_PER_CHUNK}")

    for item in ask(client, refusal_prompt(titles)):
        candidates.append({
            "status": "pending",
            "source": "generated",
            "category": "generated-refusal",
            "role": "all",
            "question": item["question"],
            "gold": [],
            "must_contain": [],
            "forbidden": [],
            "must_refuse": True,
            "passage": "",
        })

    for n, c in enumerate(candidates, start=1):
        c["cand_id"] = n
    OUT.write_text(json.dumps(candidates, indent=2))
    print(f"wrote {len(candidates)} pending candidates to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
