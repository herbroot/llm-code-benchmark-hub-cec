import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print('PyYAML is required. Install with: pip install pyyaml')
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def command_for(
    bench: dict,
    model: dict,
    api_url: str = '',
    api_key: str = '',
    timeout: float | None = None,
) -> list[str]:
    bench_id = bench['id']
    framework = bench.get('framework', '').lower()
    model_name = model['name']

    if framework == 'evalscope':
        evalscope_task = bench.get('evalscope_task', bench_id)
        cmd = ['evalscope', 'eval', '--model', model_name, '--datasets', evalscope_task]
        if api_url:
            cmd.extend(['--api-url', api_url])
        if api_key:
            cmd.extend(['--api-key', api_key])
        if timeout is not None:
            cmd.extend(['--timeout', str(timeout)])
        return cmd

    if framework == 'evalplus':
        dataset = 'humaneval' if bench_id.endswith('humaneval') else 'mbpp'
        return ['evalplus.evaluate', '--dataset', dataset, '--model', model_name]

    if framework == 'swebench':
        return ['python', '-m', 'swebench.harness.run_evaluation', '--model_name_or_path', model_name]

    if bench_id == 'ds1000':
        return ['python', 'adapters/ds1000_runner.py', '--model', model_name]

    if bench_id == 'humaneval_infilling':
        return ['python', 'adapters/humaneval_infilling_runner.py', '--model', model_name]

    return ['echo', f'Unsupported benchmark: {bench_id}']


def parse_csv_filter(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {v.strip() for v in value.split(',') if v.strip()}


def main() -> None:
    parser = argparse.ArgumentParser(description='Unified benchmark runner (EvalScope-first).')
    parser.add_argument('--config', default='configs/benchmarks/benchmarks.yaml', help='Benchmarks yaml path')
    parser.add_argument('--models', default='configs/models/models.yaml', help='Models yaml path')
    parser.add_argument('--benchmarks', default='', help='Optional CSV filter by benchmark id (e.g. humaneval,mbpp)')
    parser.add_argument('--model-names', default='', help='Optional CSV filter by model name')
    parser.add_argument('--dry-run', action='store_true', help='Print commands only')
    parser.add_argument('--stop-on-error', action='store_true', help='Stop after first failed command')
    parser.add_argument('--api-url', default='', help='OpenAI-compatible API base URL for EvalScope')
    parser.add_argument('--api-key', default='', help='API key for OpenAI-compatible API')
    parser.add_argument('--timeout', type=float, default=None, help='Request timeout in seconds for API mode')
    args = parser.parse_args()

    bench_cfg = load_yaml(Path(args.config))
    model_cfg = load_yaml(Path(args.models))

    bench_filter = parse_csv_filter(args.benchmarks)
    model_filter = parse_csv_filter(args.model_names)

    benchmarks = [b for b in bench_cfg.get('benchmarks', []) if b.get('enabled', False)]
    models = model_cfg.get('models', [])

    if bench_filter:
        benchmarks = [b for b in benchmarks if b.get('id') in bench_filter]
    if model_filter:
        models = [m for m in models if m.get('name') in model_filter]

    if not benchmarks:
        raise SystemExit('No enabled benchmarks found after filtering.')
    if not models:
        raise SystemExit('No models found after filtering.')

    failures = 0

    for bench in benchmarks:
        for model in models:
            effective_api_url = args.api_url if args.api_url else model.get('api_url', '')
            effective_api_key = args.api_key if args.api_key else model.get('api_key', '')
            effective_timeout = args.timeout if args.timeout is not None else model.get('timeout', None)

            cmd = command_for(
                bench,
                model,
                api_url=effective_api_url,
                api_key=effective_api_key,
                timeout=effective_timeout,
            )
            cmd_str = ' '.join(cmd)
            print(f"[{bench['id']}] [{model['name']}] {cmd_str}")

            if args.dry_run:
                continue

            result = subprocess.run(cmd, cwd=ROOT)
            if result.returncode != 0:
                failures += 1
                print(f'Command failed ({result.returncode}): {cmd_str}', file=sys.stderr)
                if args.stop_on_error:
                    raise SystemExit(result.returncode)

    if failures:
        raise SystemExit(f'Finished with {failures} failed command(s).')


if __name__ == '__main__':
    main()
