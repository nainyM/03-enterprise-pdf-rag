"""Retrieve relevant chunks for a role, then answer from them with Claude and citations.

Access rules (see README):
- A role can see documents tagged "all" plus its own tag.
- Only documents with status "current" are searchable. Superseded versions are hidden.
"""
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).parent
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION = "kestrel_docs"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
ANSWER_MODEL = "claude-sonnet-5-5"
REFUSAL = "I do not have enough evidence in the documents you can access to answer this."

ROLE_ACCESS = {
    "all": ["all"],
    "hr": ["all", "hr"],
    "finance": ["all", "finance"],
    "security": ["all", "security"],
}

SYSTEM_PROMPT = f"""You answer questions about Kestrel Logistics internal documents.
Rules:
1. Use only the excerpts provided. Do not use outside knowledge.
2. Cite every factual claim with the excerpt tag, for example [FIN-002 p1].
3. If the excerpts do not contain the answer, reply with exactly: {REFUSAL}
4. Keep the answer to one to three sentences."""

_model = None
_collection = None


def _load():
    """Load the embedding model and index once per process."""
    global _model, _collection
    if _collection is None:
        import chromadb
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(EMBED_MODEL)
        _collection = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(COLLECTION)
    return _model, _collection


@dataclass
class Retrieved:
    ref: str            # e.g. "FIN-002 p1"
    section: str
    text: str
    distance: float


@dataclass
class Answer:
    text: str
    refused: bool
    citations: list[str]
    retrieved: list[Retrieved] = field(default_factory=list)
    retrieval_ms: float = 0.0
    generation_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0


def retrieve(question: str, role: str, k: int = 4) -> tuple[list[Retrieved], float]:
    if role not in ROLE_ACCESS:
        raise ValueError(f"unknown role: {role}")
    model, collection = _load()
    start = time.perf_counter()
    query_vec = model.encode([question], normalize_embeddings=True).tolist()
    result = collection.query(
        query_embeddings=query_vec,
        n_results=k,
        where={"$and": [
            {"access": {"$in": ROLE_ACCESS[role]}},
            {"status": "current"},
        ]},
    )
    elapsed = (time.perf_counter() - start) * 1000
    hits = []
    for text, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append(Retrieved(
            ref=f"{meta['doc_id']} p{meta['page']}",
            section=meta["section"],
            text=text,
            distance=dist,
        ))
    return hits, elapsed


def answer(question: str, role: str, k: int = 4) -> Answer:
    import anthropic

    hits, retrieval_ms = retrieve(question, role, k)
    excerpts = "\n\n".join(f"[{h.ref}] {h.text}" for h in hits)
    user_msg = f"Excerpts:\n{excerpts}\n\nQuestion: {question}"

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    start = time.perf_counter()
    resp = client.messages.create(
        model=ANSWER_MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    generation_ms = (time.perf_counter() - start) * 1000

    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    citations = sorted(set(re.findall(r"\[([A-Z]{2,4}-\d{3} p\d+)\]", text)))
    return Answer(
        text=text,
        refused=REFUSAL.lower() in text.lower() or "do not have enough evidence" in text.lower(),
        citations=citations,
        retrieved=hits,
        retrieval_ms=retrieval_ms,
        generation_ms=generation_ms,
        input_tokens=resp.usage.input_tokens,
        output_tokens=resp.usage.output_tokens,
    )


def require_api_key() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is not set. Export it in your terminal, then retry.")
