from typing import List, Literal, Counter as CounterType, Mapping
from collections import Counter


def q1(data: List[str]) -> int:
    line_length = len(data[0])
    trackers: List[CounterType[str]] = [Counter() for _ in range(line_length)]

    for line in data:
        for i, c in enumerate(line):
            trackers[i].update(c)

    gamma_string = "".join([tracker.most_common()[0][0] for tracker in trackers])
    gamma = int(gamma_string, 2)
    epsilon = gamma ^ (2 ** line_length - 1)

    return int(gamma * epsilon)


def find_rating(
    data: List[str], dominant_value: Literal["0", "1"], count_direction: Literal[1, -1]
) -> int:
    for position in range(len(data[0])):
        tracker: CounterType[str] = Counter()
        # primes tracker.most_common() to return dominant_value
        tracker[dominant_value] = 0
        bins: Mapping[str, List[str]] = {"0": [], "1": []}

        for line in data:
            current_char = line[position]
            tracker[current_char] += count_direction
            bins[current_char].append(line)
        data = bins[tracker.most_common(1)[0][0]]
        if len(data) == 1:
            break
    return int(data[0], 2)


def q2(data: List[str]) -> int:
    oxygen_rating = find_rating(list(data), dominant_value="1", count_direction=1)
    co2_rating = find_rating(list(data), dominant_value="0", count_direction=-1)
    return oxygen_rating * co2_rating
