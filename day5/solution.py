from typing import List


class SimpleHydrothermalMap:
    def __init__(self):
        self.matrix = {}
        self.overlaps = 0

    def process_instruction(self, instruction):
        start, end = instruction.split(" -> ")
        x1, y1 = map(int, start.split(","))
        x2, y2 = map(int, end.split(","))

        if x1 != x2 and y1 != y2:
            self.handle_diagonal_line(x1, x2, y1, y2)
        elif x1 != x2:
            self.handle_horizontal_line(x1, x2, y1)
        elif y1 != y2:
            self.handle_vertical_line(y1, y2, x1)

    def handle_diagonal_line(self, x1, x2, y1, y2):
        # Do nothing
        pass

    def handle_horizontal_line(self, x1, x2, y):
        x_range = self.create_range_of_points(x1, x2)
        for x in x_range:
            self.mark_coordinate(f"{x},{y}")

    def handle_vertical_line(self, y1, y2, x):
        y_range = self.create_range_of_points(y1, y2)
        for y in y_range:
            self.mark_coordinate(f"{x},{y}")

    @staticmethod
    def create_range_of_points(a1, a2):
        a_step = 1 if a2 > a1 else -1
        return range(a1, a2 + a_step, a_step)

    def mark_coordinate(self, coordinate):
        overlaps = self.matrix.get(coordinate, 0)
        if overlaps == 1:
            self.overlaps += 1
        self.matrix[coordinate] = overlaps + 1


class DiagonalHydrothermalMap(SimpleHydrothermalMap):
    def handle_diagonal_line(self, x1, x2, y1, y2):
        x_range = self.create_range_of_points(x1, x2)
        y_range = self.create_range_of_points(y1, y2)
        for x, y in zip(x_range, y_range):
            self.mark_coordinate(f"{x},{y}")



def q1(data: List[str]) -> int:
    hydro_map = SimpleHydrothermalMap()

    for instruction in data:
        hydro_map.process_instruction(instruction)

    return hydro_map.overlaps


def q2(data: List[str]) -> int:
    hydro_map = DiagonalHydrothermalMap()

    for instruction in data:
        hydro_map.process_instruction(instruction)

    return hydro_map.overlaps
