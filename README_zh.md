# ByteBench Hub（中文说明）

[English README](./README.md)

这是一个用于代码能力评测的 LLM Benchmark 项目。

## 当前项目支持状态

- `humaneval`（EvalScope）
- `mbpp`（EvalScope + sandbox）
- `humaneval_plus`（EvalPlus 对应数据集，走 EvalScope）
- `mbpp_plus`（EvalPlus 对应数据集，走 EvalScope + sandbox）
- `humaneval_infilling`（规划中，当前是自定义 adapter 占位）
- `ds1000`（规划中，当前是自定义 adapter 占位）
- `swebench`（本仓库后续集成，当前不作为首批）

## 是否支持多模型同时测试

支持。可以实现：

- 单模型 + 多 benchmark
- 多模型 + 单 benchmark
- 多模型 + 多 benchmark

由 `scripts/run_benchmarks.py` 和 `configs/models/models.yaml` 实现。

## 目录说明

- `configs/benchmarks/benchmarks.yaml`：benchmark 路由配置
- `configs/models/models.yaml`：模型列表配置
- `scripts/run_benchmarks.py`：统一调度入口
- `adapters/`：自定义 benchmark 适配器（当前有占位）
- `docs/`：GitHub Pages 页面
- `data/scores/`：公开分数源数据

## 安装依赖

```bash
pip install -r requirements-eval.txt
```

该文件已包含 `evalscope[sandbox]`，不需要再单独安装一次。

## 配置模型

编辑 `configs/models/models.yaml`。

示例：

```yaml
models:
  - family: Qwen
    name: Qwen3.5-122B-A10B-FP8
    provider: Alibaba
    api_url: http://127.0.0.1:24444/v1
    api_key: EMPTY
  - family: DeepSeek
    name: DeepSeek-Coder-V2-Instruct
    provider: DeepSeek
    api_url: http://127.0.0.1:25555/v1
    api_key: EMPTY
```

其中 `name` 必须和你服务端 `--served-model-name` 对齐。
`api_url`/`api_key`/`timeout` 也可以按模型单独配置，适用于多模型多端口。

## 启动模型服务（vLLM 示例）

```bash
CUDA_VISIBLE_DEVICES=4,5,6,7 vllm serve "/data/model/Qwen/Qwen3___5-122B-A10B-FP8/" \
  --served-model-name Qwen3.5-122B-A10B-FP8 \
  --host 127.0.0.1 \
  --port 24444 \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 128000 \
  --enable-prefix-caching \
  --enable-chunked-prefill \
  --dtype auto \
  --trust-remote-code \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --language-model-only
```

## 评测命令

### 方式 A：直接用 EvalScope（单模型）

跑单个数据集：

```bash
evalscope eval --eval-type openai_api --model Qwen3.5-122B-A10B-FP8 --datasets humaneval --api-url http://127.0.0.1:24444/v1 --api-key EMPTY --limit 1 --eval-batch-size 1
```

跑多个数据集：

```bash
evalscope eval --eval-type openai_api --model Qwen3.5-122B-A10B-FP8 --datasets humaneval humaneval_plus --api-url http://127.0.0.1:24444/v1 --api-key EMPTY --limit 1 --eval-batch-size 1
```

`mbpp/mbpp_plus` 需要 sandbox：

```bash
evalscope eval --eval-type openai_api --model Qwen3.5-122B-A10B-FP8 --datasets mbpp mbpp_plus --api-url http://127.0.0.1:24444/v1 --api-key EMPTY --limit 1 --use-sandbox --sandbox-type docker --eval-batch-size 1
```

### 方式 B：用统一入口脚本（支持多模型）

先看将要执行的命令：

```bash
python scripts/run_benchmarks.py --dry-run --benchmarks "humaneval,mbpp"
```

单模型 + 多 benchmark：

```bash
python scripts/run_benchmarks.py --benchmarks "humaneval,mbpp,evalplus_humaneval,evalplus_mbpp" --model-names "Qwen3.5-122B-A10B-FP8" --api-url "http://127.0.0.1:24444/v1" --api-key "EMPTY"
```

多模型 + 单 benchmark：

```bash
python scripts/run_benchmarks.py --benchmarks "humaneval" --model-names "Qwen3.5-122B-A10B-FP8,DeepSeek-Coder-V2-Instruct" --api-url "http://127.0.0.1:24444/v1" --api-key "EMPTY"
```

多模型 + 多 benchmark：

```bash
python scripts/run_benchmarks.py --benchmarks "humaneval,evalplus_humaneval" --model-names "Qwen3.5-122B-A10B-FP8,DeepSeek-Coder-V2-Instruct" --api-url "http://127.0.0.1:24444/v1" --api-key "EMPTY"
```

如果在 `configs/models/models.yaml` 里给模型单独设置了 `api_url`，会优先使用模型自己的地址（覆盖全局 `--api-url`）。

## 输出结果

每次运行都会写到 `outputs/<timestamp>/`：

- `logs/eval_log.log`
- `reports/<model>/<benchmark>.json`
- `reports/report.html`

快速查看最近结果：

```bash
ls -lt outputs/*/reports/*/*.json | head
```

## 页面数据构建

```bash
python scripts/build_scores_json.py
```

会刷新 `docs/data/scores.json`，供 `docs/` 页面展示。

## 说明

- `humaneval_infilling` 和 `ds1000` 目前在本仓库中还是占位 adapter，需要后续实现。
- `swebench` 由于环境和运行成本较重，建议放在后续阶段集成。
