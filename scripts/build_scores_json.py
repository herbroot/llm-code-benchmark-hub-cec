import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / 'data' / 'scores' / 'public_scores.csv'
JSON_PATH = ROOT / 'docs' / 'data' / 'scores.json'


def normalize_score(value: str):
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return value


def main() -> None:
    parser = argparse.ArgumentParser(description='Build docs/data/scores.json from CSV.')
    parser.add_argument('--input', default=str(CSV_PATH))
    parser.add_argument('--output', default=str(JSON_PATH))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with input_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['score'] = normalize_score(row.get('score', ''))
            rows.append(row)

    payload = {
        'generated_from': str(input_path),
        'rows': rows,
        'count': len(rows),
    }

    with output_path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f'Wrote {len(rows)} rows to {output_path}')


if __name__ == '__main__':
    main()
