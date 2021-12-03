from typing import List


def q1(data: List[str]) -> int:
    increase_counter = 0

    for i, reading in enumerate(data):
        if i == 0:
            continue

        if int(reading) > int(data[i - 1]):
            increase_counter += 1
    return increase_counter


def q2(data: List[str]) -> int:
    def window_sum(start_index):
        return (
            int(data[start_index])
            + int(data[start_index + 1])
            + int(data[start_index + 2])
        )

    increase_counter = 0

    for i, _ in enumerate(data[:-2]):
        if i == 0:
            continue

        current_sum = window_sum(i)
        previous_sum = window_sum(i - 1)
        if current_sum > previous_sum:
            increase_counter += 1
    return increase_counter
