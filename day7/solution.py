from typing import List


def preprocess_data(data):
    return list(map(int, data.strip().split(",")))


def q1(crab_positions: List[int]) -> int:
    max_position = max(crab_positions)

    lowest_fuel_position = None
    for alignment_position in range(max_position + 1):
        fuel = 0
        for crab_position in crab_positions:
            fuel += abs(alignment_position - crab_position)

        if lowest_fuel_position is None or lowest_fuel_position[1] > fuel:
            lowest_fuel_position = (alignment_position, fuel)

    return lowest_fuel_position[1]


def q2(crab_positions: List[int]) -> int:
    # I think the optimum solution is when the same amount of crabs need to move
    # forward and backward. The fuel consumption plotted over the possible positions
    # has probably some kind of V-shape. You can calculate the gradient and do some
    # variation of binary search to quicker converge I guess?
    # Not relevant: brute-force was fast enough.

    def triangular_number(n):
        return int(n * (n + 1) / 2)

    max_position = max(crab_positions)

    lowest_fuel_position = None
    for alignment_position in range(max_position + 1):
        fuel = 0
        for crab_position in crab_positions:
            fuel += triangular_number(abs(alignment_position - crab_position))

        if lowest_fuel_position is None or lowest_fuel_position[1] > fuel:
            lowest_fuel_position = (alignment_position, fuel)

    return lowest_fuel_position[1]
