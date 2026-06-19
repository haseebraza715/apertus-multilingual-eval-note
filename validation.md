# Validation

This file records the checks used for the committed professor-facing artifact. Run them from the repository root.

## Python checks

```bash
python3 -m py_compile run_eval.py
python3 run_eval.py --prompts prompts.jsonl --output results.csv
python3 run_eval.py --summarize sample_results.csv
```

Result: Python compilation, result generation, and sample-result summarization passed.

## JSONL check

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path("prompts.jsonl")
lines = path.read_text(encoding="utf-8").splitlines()
assert len(lines) == 36, len(lines)

ids = []
for i, line in enumerate(lines, 1):
    obj = json.loads(line)
    required = {"id", "category", "language", "pair_id", "prompt", "expected_behavior", "requires_tool"}
    assert required.issubset(obj), (i, obj)
    ids.append(obj["id"])

assert len(ids) == len(set(ids)), "duplicate prompt ids"
print("prompts.jsonl valid:", len(lines), "lines")
PY
```

Result: 36 unique, valid JSON objects on 36 physical lines.

## CSV check

```bash
python3 - <<'PY'
import csv
from pathlib import Path

for file, expected in [("evaluation_template.csv", 37), ("sample_results.csv", 7)]:
    lines = Path(file).read_text(encoding="utf-8").splitlines()
    assert len(lines) == expected, (file, len(lines))
    with open(file, encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected - 1, (file, len(rows))
    print(file, "valid:", len(lines), "physical lines")
PY
```

Result: the template has 1 header plus 36 prompt rows; the sample has 1 header plus 6 illustrative rows.

## Committed raw-file check

```bash
COMMIT_SHA="$(git rev-parse HEAD)"
BASE="https://raw.githubusercontent.com/haseebraza715/apertus-multilingual-eval-note/$COMMIT_SHA"

curl -L "$BASE/README.md" | wc -l
curl -L "$BASE/technical_note.md" | wc -l
curl -L "$BASE/run_eval.py" | wc -l
curl -L "$BASE/prompts.jsonl" | wc -l
curl -L "$BASE/evaluation_template.csv" | wc -l
curl -L "$BASE/sample_results.csv" | wc -l
```

| File | Local lines | Committed raw lines |
| ----------------------- | ----------: | ------------------: |
| `README.md` | 83 | 83 |
| `technical_note.md` | 84 | 84 |
| `run_eval.py` | 99 | 99 |
| `prompts.jsonl` | 36 | 36 |
| `evaluation_template.csv` | 37 | 37 |
| `sample_results.csv` | 7 | 7 |

The raw-file counts are checked against the immutable commit URL after pushing. `sample_results.csv` is illustrative and is not model output or a benchmark result.
