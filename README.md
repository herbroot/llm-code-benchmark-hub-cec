# ByteBench Hub

A reproducible benchmark hub for comparing LLM coding performance across:

- HumanEval
- MBPP
- HumanEval Infilling
- DS-1000
- SWE-bench
- EvalPlus (HumanEval+/MBPP+)

## Framework Choice

Primary framework: **EvalScope**

Why:

- Covers the broadest benchmark surface as a unified entry.
- Works well as orchestration layer for API and local models.
- Can coexist with dedicated tools (`EvalPlus`, `SWE-bench` harness) under one runner.

## What Is Integrated

- EvalScope-first unified runner: `scripts/run_benchmarks.py`
- Benchmarks config: `configs/benchmarks/benchmarks.yaml`
- Models config: `configs/models/models.yaml`
- Runtime template: `configs/runtime/evalscope_runtime.example.yaml`
- Eval bootstrap script: `scripts/bootstrap_eval.ps1`
- Public scores source data: `opensource_score/`
- GitHub Pages score site: `docs/`

## Quick Start (Local)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-eval.txt
```

Dry run command generation:

```powershell
python scripts/run_benchmarks.py --dry-run --benchmarks "humaneval,mbpp"
```

Run selected benchmarks on selected models:

```powershell
python scripts/run_benchmarks.py --benchmarks "humaneval,mbpp,swebench" --model-names "Qwen2.5-Coder-32B-Instruct"
```

Install EvalScope in your conda env:

```powershell
conda run -p E:\conda_venv\spider2 pip install evalscope==1.6.0
```

Alternative one-command bootstrap:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap_eval.ps1
```

## Scoreboard Data Flow

1. Maintain public score records in `data/scores/public_scores.csv`.
2. Build JSON for web:

```powershell
python scripts/build_scores_json.py
```

3. GitHub Pages reads `docs/data/scores.json`.

## Server Deployment

See: `frameworks/server_deploy.md`

## Notes

- `HumanEval/MBPP`: routed to EvalScope by default.
- `EvalPlus`: routed to official `evalplus` CLI.
- `SWE-bench`: routed to official harness invocation.
- `DS-1000` and `HumanEval Infilling`: current adapters are placeholders for custom evaluator wiring.

## References

- EvalScope: https://github.com/modelscope/evalscope
- EvalScope dataset support docs: https://evalscope.readthedocs.io/en/latest/get_started/supported_dataset/index.html
- OpenCompass: https://github.com/open-compass/opencompass
- EvalPlus: https://github.com/evalplus/evalplus
- SWE-bench: https://www.swebench.com/
- DS-1000: https://github.com/xlang-ai/DS-1000
