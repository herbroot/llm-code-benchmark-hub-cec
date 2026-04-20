# Evaluation Framework Decision

Date: 2026-04-20

## Requirement Mapping

Benchmarks required:

- HumanEval
- MBPP
- HumanEval Infilling
- DS-1000
- SWE-bench
- EvalPlus

Need:

- one-command orchestration
- easy server deployment
- extensible benchmark registry

## Option Review

### EvalScope (recommended as orchestration layer)

Pros:

- Unified CLI/config style and broad benchmark coverage.
- Built-in docs for third-party integrations including SWE-bench.
- Practical for combining API models and local-serving models.

Gaps:

- Some niche tasks (e.g., specific infilling variants) may still require custom adapter.

### OpenCompass (recommended backend for classic code benchmarks)

Pros:

- Mature benchmark configs and reporting ecosystem.
- Good support for HumanEval/MBPP style tasks.

Gaps:

- Not the cleanest single entrypoint for all requested benchmarks without wrappers.

### EvalPlus (required for HumanEval+/MBPP+)

Pros:

- Official extension benchmark with stronger tests.

Gaps:

- Separate CLI; better wrapped under a unified runner.

### SWE-bench official harness

Pros:

- Most faithful evaluation for SWE-bench tasks.

Gaps:

- Heavier runtime/dependency requirements.

## Final Architecture

Use a wrapper runner (`scripts/run_benchmarks.py`) that dispatches to:

- EvalScope/OpenCompass for HumanEval/MBPP
- EvalPlus for HumanEval+/MBPP+
- SWE-bench harness for SWE-bench
- custom adapters for HumanEval Infilling and DS-1000

This keeps a single command UX while preserving benchmark-faithful implementations.

## Initial Deployment Approach (server)

- Containerize each backend runtime in separate images or compose services.
- Keep model serving decoupled (vLLM/TGI/API gateway).
- Run evaluation jobs via one orchestrator command and write standardized result JSON into `outputs/`.
