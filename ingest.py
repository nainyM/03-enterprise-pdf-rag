"""Ingest the PDF corpus: parse -> clean -> chunk -> metadata -> embed -> index.

Run once after make_corpus.py: python ingest.py
Re-running rebuilds the index from scratch.
"""
import json
import re
import shutil
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "corpus" / "pdfs"
MANIFEST = ROOT / "corpus" / "manifest.json"
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION = "kestrel_docs"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

CHUNK_CHARS = 600
OVERLAP_CHARS = 80


def clean(text: str) -> str:
    """Normalise whitespace and drop the running page header we added to each page."""
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not re.search(r"\| page \d+$", ln)]
    return "\n".join(lines)


def split_sections(page_text: str) -> list[tuple[str, str]]:
    """Split a page into (heading, body) pairs.

    Heuristic: a short line with no final punctuation is a heading. Body lines
    end with a full stop, so this separates them cleanly for this corpus.
    """
    sections, heading, body = [], "General", []
    for line in page_text.splitlines():
        is_heading = len(line) <= 45 and not line.endswith((".", ":", ","))
        if is_heading:
            if body:
                sections.append((heading, " ".join(body)))
            heading, body = line, []
        else:
            body.append(line)
    if body:
        sections.append((heading, " ".join(body)))
    return sections


def window(text: str) -> list[str]:
    """Split long section bodies into overlapping character windows."""
    if len(text) <= CHUNK_CHARS:
        return [text]
    pieces, start = [], 0
    while start < len(text):
        pieces.append(text[start:start + CHUNK_CHARS])
        if start + CHUNK_CHARS >= len(text):
            break
        start += CHUNK_CHARS - OVERLAP_CHARS
    return pieces


def build_chunks() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text())
    chunks = []
    for doc in manifest["documents"]:
        reader = PdfReader(str(PDF_DIR / doc["file"]))
        for page_no, page in enumerate(reader.pages, start=1):
            for heading, body in split_sections(clean(page.extract_text() or "")):
                for i, piece in enumerate(window(body)):
                    chunks.append({
                        "id": f"{doc['doc_id']}-p{page_no}-{heading[:20].replace(' ', '_')}-{i}",
                        # The heading is prepended so the embedding carries section context.
                        "text": f"{heading}. {piece}",
                        "metadata": {
                            "doc_id": doc["doc_id"],
                            "title": doc["title"],
                            "page": page_no,
                            "section": heading,
                            "date": doc["date"],
                            "status": doc["status"],
                            "access": doc["access"],
                            "owner": doc["owner"],
                        },
                    })
    return chunks


def main() -> None:
    import chromadb
    from sentence_transformers import SentenceTransformer

    chunks = build_chunks()
    print(f"parsed {len(chunks)} chunks from {len(list(PDF_DIR.glob('*.pdf')))} PDFs")

    model = SentenceTransformer(EMBED_MODEL)
    vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True).tolist()

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=vectors,
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"indexed {collection.count()} chunks into {CHROMA_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
