from typing import List, Tuple


def preprocess_data(data: str) -> Tuple[List[str], List[str]]:
    dots, fold_instructions = data.strip().split("\n\n")
    return dots.split("\n"), fold_instructions.split("\n")


class InstructionManual:
    def __init__(self, matrix: List[List[str]]) -> None:
        self.matrix = matrix

    def __repr__(self) -> str:
        repr = "-" * len(self.matrix[0]) + "\n"
        repr += "\n".join(["".join(line) for line in self.matrix]) + "\n"
        repr += "-" * len(self.matrix[0])
        return repr

    def fold_along_x(self, x_fold: int) -> None:
        new_matrix = []
        for line in self.matrix:
            new_line: List[str] = []
            for x, value in enumerate(line):
                if x == x_fold:
                    continue
                elif x > x_fold:
                    if value == "#":
                        new_line[x_fold - (x - x_fold)] = value
                else:
                    new_line.append(value)
            new_matrix.append(new_line)

        self.matrix = new_matrix

    def fold_along_y(self, y_fold: int) -> None:
        new_matrix: List[List[str]] = []
        for y, line in enumerate(self.matrix):
            if y == y_fold:
                continue
            elif y > y_fold:
                for x, value in enumerate(line):
                    if value == "#":
                        new_matrix[y_fold - (y - y_fold)][x] = value
            else:
                new_line = []
                for value in line:
                    new_line.append(value)
                new_matrix.append(new_line)

        self.matrix = new_matrix

    def find_number_of_dots(self) -> int:
        return sum([line.count("#") for line in self.matrix])

    def process_fold_instruction(self, instruction: str) -> None:
        fold_axis, fold_index_str = instruction.split("=")
        fold_index = int(fold_index_str)
        if fold_axis == "fold along x":
            self.fold_along_x(fold_index)
        elif fold_axis == "fold along y":
            self.fold_along_y(fold_index)
        else:
            raise Exception(f"Illegal fold axis given: {fold_axis}")


def create_manual_from_dots(dots: List[str]) -> InstructionManual:
    max_x = max([int(d.split(",")[0]) for d in dots])
    max_y = max([int(d.split(",")[1]) for d in dots])

    matrix = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for line in dots:
        x, y = map(int, line.split(","))
        matrix[y][x] = "#"

    return InstructionManual(matrix)


def q1(data: Tuple[List[str], List[str]]) -> int:
    dots, fold_instructions = data
    manual = create_manual_from_dots(dots)
    manual.process_fold_instruction(fold_instructions[0])
    return manual.find_number_of_dots()


def q2(data: Tuple[List[str], List[str]]) -> str:
    dots, fold_instructions = data
    manual = create_manual_from_dots(dots)

    for instruction in fold_instructions:
        manual.process_fold_instruction(instruction)

    return str(manual)
