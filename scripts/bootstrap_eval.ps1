param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/3] Create virtual env (.venv)"
& $Python -m venv .venv

Write-Host "[2/3] Install evaluation dependencies"
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements-eval.txt

Write-Host "[3/3] Dry-run benchmark command generation"
& .\.venv\Scripts\python.exe scripts\run_benchmarks.py --dry-run --benchmarks humaneval,mbpp

Write-Host "Done. Next: edit configs/models/models.yaml and run real benchmarks."
