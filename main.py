import importlib
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    "Advent of Code 2021 utility script\n\nGives answers to the questions you have"
)
parser.add_argument("DAY", type=int, help="The day that you want the solutions for")
parser.add_argument(
    "--test", action="store_true", help="Runs the algorithm on test data"
)
args = parser.parse_args()

if __name__ == "__main__":
    day = args.DAY

    if args.test:
        input_data_path = Path(f"./day{day}/test_input.txt")
    else:
        input_data_path = Path(f"./day{day}/input.txt")

    try:
        with open(input_data_path) as f:
            input_data = f.read().strip().split("\n")
    except FileNotFoundError:
        print(
            f"No file found at path '{input_data_path}'. "
            "Make sure you have everything set up correctly."
        )
        exit(1)

    solution = importlib.import_module(".solution", f"day{day}")

    print(solution.q1(input_data))
    print(solution.q2(input_data))
