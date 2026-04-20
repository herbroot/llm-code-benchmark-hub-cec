from pathlib import Path


def main() -> None:
    Path('outputs').mkdir(parents=True, exist_ok=True)
    print('TODO: implement HumanEval Infilling adapter runner.')


if __name__ == '__main__':
    main()
