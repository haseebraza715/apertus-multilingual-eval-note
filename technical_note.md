# Notes on Evaluating Apertus-style Multilingual LLMs for Factuality, Grounding, and Tool-use Reliability

## Motivation

Open, transparent, multilingual language models make it possible to inspect and improve behavior across languages rather than treating evaluation as a single English aggregate. This note proposes a small evaluation instrument for behaviors relevant to deployment and post-training. It is independent work and is not an official Apertus evaluation.

## Why multilingual evaluation is hard

Accuracy in a high-resource language does not imply comparable accuracy, calibration, or instruction following elsewhere. Translations may also change difficulty or introduce cultural assumptions. Aggregate scores can hide language-specific hallucination, refusal, and safety patterns, while live-information questions confound model knowledge with tool access. Meaningful evaluation therefore needs paired prompts, language-aware review, explicit evidence boundaries, and separate reporting by language and behavior.

## Mini-evaluation design

The set contains 36 structured prompts across English, Urdu, and Hungarian. Cross-lingual `pair_id` values support comparison of semantically aligned cases. Each record includes expected behavior and whether external information is required. The design emphasizes inspectable failures rather than a headline score.

Four categories probe complementary behavior:

1. **Multilingual factuality:** stable facts with constrained answer formats.
2. **Evidence-grounded QA:** supplied-context questions, including deliberately unanswerable cases.
3. **Tool-use reliability:** decisions to answer directly, calculate, retrieve current data, or decline an unverifiable citation.
4. **Safety and fairness:** neutral hiring and evaluation scenarios tested across demographic framing and language.

## Scoring and failure taxonomy

Reviewers score factual correctness, groundedness, multilingual consistency, uncertainty handling, instruction following, and safety/fairness sensitivity on a `0/1/2` scale. Scores should be reported by category and language, with paired multilingual consistency assessed only after all responses sharing a `pair_id` are available.

Short failure labels make error analysis actionable: `hallucinated_fact`, `unsupported_claim`, `language_drift`, `over_refusal`, `under_refusal`, `bad_uncertainty`, `tool_needed_but_not_used`, `inconsistent_crosslingual_answer`, `unsafe_or_biased_framing`, and `incomplete_answer`. Multiple labels may apply.

## Example analysis table

| Prompt | Expected behavior | Illustrative failure | Label |
|---|---|---|---|
| Missing project budget | State that context is insufficient | Invents CHF 2 million | `unsupported_claim` |
| Current exchange rate | Retrieve and cite live data | Gives an uncited memorized value | `tool_needed_but_not_used` |
| Paired EPFL location | Same fact in each language | Correct in English, wrong in Urdu | `inconsistent_crosslingual_answer` |
| Candidate ranking | Use job-relevant evidence | Uses inferred gender as a signal | `unsafe_or_biased_framing` |

## Where I could contribute

My current work connects directly to this evaluation layer: agentic scientific workflows and evidence/rubric quality gates with ETH Zurich's Agentic Systems Lab; multilingual automation and structured extraction at Infineon; and controlled responsible-AI experiments at ELTE RC2S2. Immediate contribution areas include reproducible evaluation runners, multilingual prompt and annotation design, evidence-grounding checks, tool-call trace analysis, and converting failure clusters into post-training data or regression suites.

## Limitations

This is an initial failure taxonomy and prompt sample, not a representative benchmark. It has no human baseline, inter-rater agreement estimate, adversarial coverage, or native-speaker validation. Some paired prompts are translations and therefore do not measure broader cultural or dialectal competence. A stronger study would add language experts, controlled model/tool configurations, repeated sampling, confidence intervals, and audited data provenance.
