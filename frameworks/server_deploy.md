# Server Deployment Notes (EvalScope-first)

## 1) Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-eval.txt
```

## 2) Model serving

Use one OpenAI-compatible endpoint (vLLM/TGI/proxy):

- base URL example: `http://127.0.0.1:8000/v1`
- key env example: `OPENAI_API_KEY`

## 3) Configure

- `configs/models/models.yaml`: model list
- `configs/benchmarks/benchmarks.yaml`: benchmark list
- `configs/runtime/evalscope_runtime.example.yaml`: runtime template

## 4) Dry run

```powershell
python scripts/run_benchmarks.py --dry-run --benchmarks humaneval,mbpp
```

## 5) Run selected benchmark set

```powershell
python scripts/run_benchmarks.py --benchmarks humaneval,mbpp,swebench --model-names Qwen2.5-Coder-32B-Instruct
```

## 6) Publish scoreboard

```powershell
python scripts/build_scores_json.py
```

Then push to GitHub and Pages workflow will update site data.
