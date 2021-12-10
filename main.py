import importlib
from pathlib import Path
import argparse
import textwrap

import requests

parser = argparse.ArgumentParser(
    "Advent of Code 2021 utility script\n\n👀 Gives answers to the questions you have 👀"
)
parser.add_argument("DAY", type=int, help="The day that you want the solutions for")
parser.add_argument(
    "--test", action="store_true", help="Runs the algorithm on test data"
)
parser.add_argument(
    "--create", action="store_true", help="Creates a folder for this day and downloads your input"
)
args = parser.parse_args()


def create_new_day_folder(day: int):
    directory = Path(__file__).parent / f"day{day}"
    directory.mkdir(exist_ok=False)
    (directory / "__init__.py").touch()
    (directory / "test_input.txt").touch()


    standard_solutions_content = textwrap.dedent(
        """\
        from typing import List


        def q1(data: List[str]) -> int:
            return 0

        def q2(data: List[str]) -> int:
            return 0
        """
    )
    with (directory / "solution.py").open("w", newline="\n") as f:
        f.write(standard_solutions_content)

    aoc_cookie = (Path().parent / "aoc_cookie").read_text()

    r = requests.get(f"https://adventofcode.com/2021/day/{day}/input", headers={"cookie": aoc_cookie})
    r.raise_for_status()
    with (directory / "input.txt").open("w", newline="\n") as f:
        f.write(r.text)



def preprocess_data(data):
    return data.strip().split("\n")


if __name__ == "__main__":
    day = args.DAY

    if args.create:
        create_new_day_folder(day)
        exit(0)

    if args.test:
        input_data_path = Path(f"./day{day}/test_input.txt")
    else:
        input_data_path = Path(f"./day{day}/input.txt")

    try:
        with open(input_data_path) as f:
            input_data = f.read()
    except FileNotFoundError:
        print(
            f"No file found at path '{input_data_path}'. "
            "Make sure you have everything set up correctly."
        )
        exit(1)

    solution = importlib.import_module(".solution", f"day{day}")
    pd = getattr(solution, "preprocess_data", preprocess_data)

    print(solution.q1(pd(input_data)))
    print(solution.q2(pd(input_data)))
