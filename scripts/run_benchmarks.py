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


def command_for(bench_id: str, model_name: str) -> list[str]:
    if bench_id in {'humaneval', 'mbpp'}:
        return ['python', '-m', 'evalscope', 'run', '--benchmark', bench_id, '--model', model_name]
    if bench_id in {'evalplus_humaneval', 'evalplus_mbpp'}:
        dataset = 'humaneval' if bench_id.endswith('humaneval') else 'mbpp'
        return ['evalplus.evaluate', '--dataset', dataset, '--model', model_name]
    if bench_id == 'swebench':
        return ['python', '-m', 'swebench.harness.run_evaluation', '--model_name_or_path', model_name]
    if bench_id == 'ds1000':
        return ['python', 'adapters/ds1000_runner.py', '--model', model_name]
    if bench_id == 'humaneval_infilling':
        return ['python', 'adapters/humaneval_infilling_runner.py', '--model', model_name]
    return ['echo', f'Unsupported benchmark: {bench_id}']


def main() -> None:
    parser = argparse.ArgumentParser(description='Unified benchmark runner.')
    parser.add_argument('--config', required=True, help='Benchmarks yaml path')
    parser.add_argument('--models', required=True, help='Models yaml path')
    parser.add_argument('--dry-run', action='store_true', help='Print commands only')
    args = parser.parse_args()

    bench_cfg = load_yaml(Path(args.config))
    model_cfg = load_yaml(Path(args.models))

    benchmarks = [b for b in bench_cfg.get('benchmarks', []) if b.get('enabled', False)]
    models = model_cfg.get('models', [])

    if not benchmarks:
        raise SystemExit('No enabled benchmarks found.')
    if not models:
        raise SystemExit('No models found.')

    for bench in benchmarks:
        bench_id = bench['id']
        for model in models:
            model_name = model['name']
            cmd = command_for(bench_id, model_name)
            cmd_str = ' '.join(cmd)
            print(f'[{bench_id}] [{model_name}] {cmd_str}')
            if args.dry_run:
                continue

            result = subprocess.run(cmd, cwd=ROOT)
            if result.returncode != 0:
                print(f'Command failed: {cmd_str}', file=sys.stderr)


if __name__ == '__main__':
    main()
