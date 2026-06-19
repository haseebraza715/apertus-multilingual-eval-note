#!/usr/bin/env python3
"""Minimal model-adapter and manual-score summarizer for the prompt set."""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SCORE_FIELDS = (
    "factual_correctness",
    "groundedness",
    "multilingual_consistency",
    "uncertainty_handling",
    "instruction_following",
    "safety_fairness_sensitivity",
)


def call_model(prompt: str) -> str:
    """Replace with a local or remote model adapter; no API is assumed."""
    return "[MODEL ADAPTER NOT CONFIGURED]"


def load_prompts(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def run(prompts_path: Path, output_path: Path, model_name: str) -> None:
    fields = [
        "prompt_id", "category", "language", "pair_id", "requires_tool",
        "model_name", "model_response", *SCORE_FIELDS, "failure_labels",
        "evaluator_notes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in load_prompts(prompts_path):
            writer.writerow({
                "prompt_id": item["id"],
                "category": item["category"],
                "language": item["language"],
                "pair_id": item["pair_id"],
                "requires_tool": str(item["requires_tool"]).lower(),
                "model_name": model_name,
                "model_response": call_model(item["prompt"]),
            })
    print(f"Wrote {output_path}")


def summarize(results_path: Path) -> None:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    with results_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            scores = []
            for field in SCORE_FIELDS:
                try:
                    scores.append(float(row[field]))
                except (ValueError, TypeError):
                    pass
            if scores:
                grouped[(row["category"], row["language"])].append(
                    sum(scores) / len(scores)
                )

    print("category,language,n_scored,mean_dimension_score")
    for (category, language), values in sorted(grouped.items()):
        print(f"{category},{language},{len(values)},{sum(values) / len(values):.2f}")
    if not grouped:
        print("No numeric manual scores found.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, default=Path("prompts.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("results.csv"))
    parser.add_argument("--model-name", default="unconfigured")
    parser.add_argument("--summarize", type=Path)
    args = parser.parse_args()

    if args.summarize:
        summarize(args.summarize)
    else:
        run(args.prompts, args.output, args.model_name)


if __name__ == "__main__":
    main()
