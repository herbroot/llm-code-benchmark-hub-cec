# ByteBench Hub

A reproducible benchmark hub for comparing LLM coding performance across:

- HumanEval
- MBPP
- HumanEval Infilling
- DS-1000
- SWE-bench
- EvalPlus (HumanEval+/MBPP+)

Target model families:

- Qwen
- DeepSeek
- Seed
- Llama
- StarCoder2
- Google Gemma

## Repo Goals

1. Aggregate public benchmark scores into a single table with source links.
2. Provide one-click local/server benchmark execution for the same benchmark set.
3. Publish a lightweight GitHub Pages site that auto-renders scoreboards from local data files.
4. Keep architecture extensible for adding more benchmarks later.

## Current Status

- GitHub Pages scaffold: ready (`docs/`)
- Public score schema + sample records: ready (`data/scores/public_scores.csv`)
- Unified benchmark runner skeleton: ready (`scripts/run_benchmarks.py`)
- Framework selection notes (EvalScope/OpenCompass/EvalPlus/SWE-bench): ready (`frameworks/eval_framework_decision.md`)

## Recommended Evaluation Stack

Primary orchestration: `EvalScope`

Reasons:

- Unified task abstraction and multi-backend support (native + OpenCompass + third-party integrations).
- Documented support for SWE-bench variants and broad benchmark registry.
- Good fit for API models and local models under one config format.

Add-on backends/tools:

- `EvalPlus` for HumanEval+/MBPP+ rigorous test extension.
- `SWE-bench` official harness for the most faithful SWE evaluation.
- `OpenCompass` backend for classic HumanEval/MBPP and broader ecosystem compatibility.

## Quick Start

### 1) Create env

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Inspect sample score table

```powershell
python scripts/build_scores_json.py
```

### 3) Run benchmark command generation (dry-run)

```powershell
python scripts/run_benchmarks.py --config configs/benchmarks/benchmarks.yaml --models configs/models/models.yaml --dry-run
```

### 4) Serve GitHub Pages locally

```powershell
python -m http.server 8000 --directory docs
```

Open: `http://localhost:8000`

## Data Model

Primary score file:

- `data/scores/public_scores.csv`

Key columns:

- `benchmark`
- `metric`
- `model_family`
- `model_name`
- `score`
- `score_unit`
- `source_name`
- `source_url`
- `source_date`
- `notes`

After editing CSV, run:

```powershell
python scripts/build_scores_json.py
```

This refreshes `docs/data/scores.json` used by the GitHub Pages front-end.

## GitHub Pages Setup

1. Push this repo to GitHub.
2. In `Settings -> Pages`, set source to `GitHub Actions`.
3. Workflow `.github/workflows/pages.yml` will publish the `docs/` site.

## Benchmarks Coverage Plan

- HumanEval: via OpenCompass/EvalScope; public scores from curated leaderboards/model reports.
- MBPP: via OpenCompass/EvalScope; public scores from curated leaderboards/model reports.
- HumanEval Infilling: custom adapter (dataset + evaluator), integrated into runner.
- DS-1000: official dataset + evaluator script wrapper.
- SWE-bench: official harness invocation wrapped by unified runner.
- EvalPlus: official `evalplus` CLI integrated for HumanEval+/MBPP+.

## References

- EvalScope: https://github.com/modelscope/evalscope
- EvalScope supported benchmarks: https://evalscope.readthedocs.io/en/latest/get_started/supported_dataset/index.html
- EvalScope SWE-bench integration: https://evalscope.readthedocs.io/en/latest/third_party/swe_bench.html
- OpenCompass: https://github.com/open-compass/opencompass
- EvalPlus: https://github.com/evalplus/evalplus
- EvalPlus leaderboard: https://evalplus.github.io/leaderboard.html
- SWE-bench: https://www.swebench.com/
- SWE-bench website repo (leaderboard data source): https://github.com/SWE-bench/swe-bench.github.io
- DS-1000 project page: https://ds1000-code-gen.github.io/
- DS-1000 official repo: https://github.com/xlang-ai/DS-1000
- BigCode models leaderboard (public HumanEval-Python): https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard
