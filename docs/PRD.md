# RAG Product Requirements: Kestrel Policy Assistant

Status: draft for the portfolio demo. The corpus is synthetic.

## 1. Problem

Employees ask policy questions, and the answers are spread across PDFs that have different owners, access levels, and versions. A general chatbot answers confidently from memory or from an outdated document. The product must answer from the right current document, cite it, and refuse when the documents don't support an answer.

## 2. Users and roles

| Role | Can search |
|---|---|
| All staff | Documents tagged `all` |
| HR | `all` plus `hr` |
| Finance | `all` plus `finance` |
| Security | `all` plus `security` |

Role is chosen in the demo UI. In production it comes from the identity provider.

## 3. Scope

In scope: answering single-document and multi-document policy questions; citing the page for each claim; refusing when evidence is missing or access is denied; ignoring superseded versions.

Out of scope (for this version): conversation memory; actions in other systems; scanned PDFs or OCR; tables that need layout-aware parsing; a reranker or hybrid keyword search (added only if the eval shows a need).

## 4. Behaviour rules

1. Answer only from passages the user's role can access and that are marked current.
2. Cite every claim with document and page, e.g. `[FIN-002 p1]`.
3. If the passages don't contain the answer, reply with the fixed refusal sentence. Never fill the gap from general knowledge.
4. Never reveal content from a document the role cannot access, including in a refusal.
5. Superseded documents are never used. Their content can only be shown as history, which is out of scope.

## 5. Data assumptions

- **Freshness:** each document has an owner and a date. Owners mark a document superseded when a new version is published. The index is rebuilt when a document changes. Rebuilding is manual in this demo.
- **Access:** each document has one access tag. A document with several audiences would need several tags, which is not supported yet.
- **Quality:** the PDFs are text-based and contain clear section headings. Headings are used for chunking.

## 6. Success metrics and targets

| Metric | Target | Why it matters |
|---|---|---|
| Recall@4 on answerable questions | at least 90% | Without the right page, the model can't answer |
| Answer accuracy | at least 90% | The core job |
| Refusal accuracy on must-refuse questions | 100% | A wrong refusal is annoying; a wrong answer is a risk |
| Access leaks | 0 | A leak is a policy breach |
| Stale-document leaks | 0 | Outdated policy gives wrong answers |
| Citation correctness | at least 95% | Users must be able to check the source |
| Median generation latency | under 3 seconds | Keeps the tool usable in a meeting |

The eval set has 35 questions. It includes a few hard cases on purpose: vague wording, typos, paraphrase, two documents at once, prompt injection, and near-miss refusals.

## 7. Risks

- **Keyword grading** can give false passes or false fails. Manual review of failures is required before trusting the scores.
- **Small corpus** (12 documents). Retrieval results on a larger, messier corpus would be lower.
- **Simulated access control.** The app filters by role in code. That's acceptable for a demo but not for production.
- **Cost.** Each question calls the model once. The cost grows with traffic and is not capped in this version.

## 8. What we would do before production

- Enforce access in the document store, not in app code.
- Add a reranker or hybrid search if the eval shows the top 4 are missing the answer.
- Add a human-review queue for refusals and low-confidence answers.
- Set a monthly cost budget and alert on it.
- Re-run the eval on each change to documents, prompts, or models.
