from typing import List, Tuple
from math import sqrt, ceil


def preprocess_data(data: str) -> Tuple[List[int], List[int]]:
    x_str, y_str = data.strip().replace("target area: ", "").split(", ")

    x_start, x_end = map(int, x_str.replace("x=", "").split(".."))
    x_range = list(range(x_start, x_end + 1))

    y_start, y_end = map(int, y_str.replace("y=", "").split(".."))
    y_range = list(range(y_start, y_end + 1))
    return x_range, y_range


def triangular(n: int) -> int:
    return int(n * (n + 1) / 2)


def find_smallest_x_to_reach_range(x_range: List[int]) -> int:
    # Rewriting the triangular x = n(n+1)/2
    # gives n = (-1 + sqrt(1 + 8x) / 2)
    smallest_x = (-1 + sqrt(1 + 8 * min(x_range))) / 2
    # Since x might not be an int we have to take the upper value and check
    # if it still falls within the range.
    smallest_x = ceil(smallest_x)
    if triangular(smallest_x) not in x_range:
        raise Exception(
            "Unexpected input, the x-range cannot be hit with a triangular number, "
            "even the smallest number overshoots."
        )
    return smallest_x


def find_largest_x_to_reach_range(x_range: List[int]) -> int:
    return max(x_range)


def find_largest_y_to_reach_range(y_range: List[int]) -> int:
    # Note: This does not work if the x_range is such that x(x+1)/2 is never satisfied.
    # The probe would overshoot.
    return abs(min(y_range)) - 1


def does_it_hit_target(initial_velocity, x_range, y_range):
    dx, dy = initial_velocity
    position = (0, 0)
    for _ in range(1000):  # Can probably be calculated cleanly, but..
        position = position[0] + dx, position[1] + dy
        if position[0] in x_range and position[1] in y_range:
            return True
        if position[0] > max(x_range) or position[1] < min(y_range):
            return False
        dy -= 1
        if dx > 0:
            dx -= 1
    else:
        raise Exception(
            f"Never got a solution for {initial_velocity}. Current position: {position}"
        )


def q1(data: Tuple[List[int], List[int]]) -> int:
    # Actually not completely correct, this answer is wrong for an input as
    # for instance 'target area: x=352..377, y=-49..-30'.
    # See q1_actually_more_correct for the correct but less neat solution.
    _, y_range = data
    y = find_largest_y_to_reach_range(y_range)
    return triangular(y)


def q1_actually_more_correct(data: Tuple[List[int], List[int]]) -> int:
    x_range, y_range = data

    max_x = find_largest_x_to_reach_range(x_range)
    max_y = find_largest_y_to_reach_range(y_range)

    correct_velocities = []
    for x in range(max_x + 1):
        for y in range(min(y_range), max_y + 1):
            if does_it_hit_target((x, y), x_range, y_range):
                correct_velocities.append((x, y))

    correct_velocities.sort(key=lambda x: x[1])
    actual_max_y = correct_velocities[-1][1]
    return triangular(actual_max_y)


def q2(data: Tuple[List[int], List[int]]) -> int:
    x_range, y_range = data

    max_x = find_largest_x_to_reach_range(x_range)
    max_y = find_largest_y_to_reach_range(y_range)

    correct_velocities = []
    for x in range(max_x + 1):
        for y in range(min(y_range), max_y + 1):
            if does_it_hit_target((x, y), x_range, y_range):
                correct_velocities.append((x, y))

    correct_velocities.sort(key=lambda x: x[1])
    return len(correct_velocities)
