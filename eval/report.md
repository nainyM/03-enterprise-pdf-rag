# Eval report (full)

## Summary

- **questions**: 35
- **recall_at_4**: 100%
- **answer_accuracy**: 97%
- **citation_correctness**: 96%
- **refusal_accuracy**: 100%
- **median_retrieval_ms**: 69.5
- **median_generation_ms**: 1520.7
- **total_input_tokens**: 15296
- **total_output_tokens**: 2283

## Per question

| # | Category | Role | Retrieved | Hit | Result |
|---|---|---|---|---|---|
| 1 | factual | all | HR-001 p1, HR-001 p2, HR-001 p2, PRD-001 p1 | yes | pass |
| 2 | factual | all | HR-001 p1, PRD-001 p1, HR-001 p2, PRD-001 p2 | yes | pass |
| 3 | factual | all | HR-001 p2, HR-001 p1, HR-001 p1, PRD-001 p1 | yes | pass |
| 4 | factual | all | HR-001 p2, HR-001 p1, HR-001 p2, PRD-001 p2 | yes | pass |
| 5 | factual | hr | HR-002 p1, HR-002 p2, PRD-001 p1, PRD-001 p2 | yes | pass |
| 6 | factual | hr | HR-002 p2, HR-002 p1, PRD-001 p1, PRD-001 p2 | yes | pass |
| 7 | factual | finance | FIN-003 p1, FIN-002 p2, FIN-002 p1, PRD-001 p2 | yes | pass |
| 8 | factual | finance | FIN-002 p2, HR-001 p1, HR-001 p2, FIN-003 p1 | yes | pass |
| 9 | factual | finance | FIN-003 p1, FIN-002 p1, FIN-002 p2, PRD-001 p1 | yes | pass |
| 10 | factual | security | SEC-001 p1, SEC-001 p2, ENG-001 p1, SEC-002 p1 | yes | pass |
| 11 | factual | security | SEC-001 p2, HR-001 p1, HR-001 p2, SEC-001 p1 | yes | pass |
| 12 | factual | security | SEC-002 p1, SEC-002 p2, PRD-001 p1, SEC-001 p2 | yes | pass |
| 13 | factual | all | PRD-001 p1, PRD-001 p2, PRD-003 p1, PRD-002 p1 | yes | pass |
| 14 | factual | all | PRD-001 p2, PRD-001 p1, HR-001 p2, HR-001 p1 | yes | pass |
| 15 | factual | all | PRD-002 p1, PRD-001 p1, PRD-002 p2, PRD-001 p2 | yes | pass |
| 16 | factual | all | PRD-003 p1, PRD-001 p2, PRD-002 p1, PRD-001 p1 | yes | pass |
| 17 | factual | security | ENG-001 p1, SEC-002 p2, SEC-002 p1, SEC-001 p2 | yes | pass |
| 18 | factual | finance | TRV-001 p1, FIN-002 p1, PRD-001 p1, PRD-001 p2 | yes | pass |
| 19 | multi-doc | finance | FIN-003 p1, PRD-001 p1, PRD-001 p2, PRD-002 p2 | yes | pass |
| 20 | multi-doc | security | ENG-001 p1, SEC-002 p1, SEC-001 p2, SEC-001 p1 | yes | pass |
| 21 | conflicting-or-stale | finance | FIN-002 p1, TRV-001 p1, PRD-001 p1, HR-001 p2 | yes | pass |
| 22 | conflicting-or-stale | finance | FIN-002 p1, FIN-002 p2, TRV-001 p1, HR-001 p2 | n/a | pass |
| 23 | access-denied | all | PRD-001 p1, PRD-001 p2, PRD-002 p1, PRD-002 p2 | n/a | pass |
| 24 | no-answer | all | PRD-001 p2, PRD-002 p1, PRD-001 p1, PRD-002 p2 | n/a | pass |
| 25 | no-answer | all | PRD-001 p1, PRD-002 p2, PRD-002 p1, PRD-001 p2 | n/a | pass |
| 26 | hard-vague | finance | FIN-002 p1, HR-001 p2, TRV-001 p1, HR-001 p1 | yes | pass |
| 27 | hard-typo | all | HR-001 p1, HR-001 p2, HR-001 p2, HR-001 p1 | yes | pass |
| 28 | hard-paraphrase | finance | FIN-002 p2, FIN-003 p1, FIN-002 p1, HR-001 p1 | yes | pass |
| 29 | hard-multi-doc | finance | FIN-003 p1, FIN-002 p1, FIN-002 p2, TRV-001 p1 | yes | pass |
| 30 | hard-vague | all | HR-001 p2, HR-001 p1, HR-001 p1, PRD-001 p2 | yes | pass |
| 31 | hard-access | finance | PRD-001 p1, PRD-001 p2, HR-001 p1, HR-001 p2 | n/a | pass |
| 32 | hard-injection | all | HR-001 p1, PRD-001 p1, HR-001 p1, HR-001 p2 | n/a | pass |
| 33 | hard-refusal-near-miss | finance | TRV-001 p1, FIN-002 p1, PRD-001 p1, FIN-003 p1 | n/a | pass |
| 34 | hard-refusal-near-miss | finance | FIN-002 p1, FIN-002 p2, FIN-003 p1, TRV-001 p1 | yes | pass |
| 35 | hard-vague | security | PRD-001 p1, SEC-002 p1, SEC-002 p2, SEC-001 p2 | yes | refused-answerable |

## Failures

### Q35: How fast must we respond to a major outage?
- Label: `refused-answerable`
- Gold: SEC-002 p1
- Retrieved: PRD-001 p1, SEC-002 p1, SEC-002 p2, SEC-001 p2
- Answer: I do not have enough evidence in the documents you can access to answer this.

