from typing import List


class OccurenceTracker:
    def __init__(self):
        self.zeros = 0
        self.ones = 0

    def most_common(self, default=None) -> str:
        if self.zeros == self.ones:
            if default is not None:
                return default
            else:
                raise Exception("I was not prepared to handle this!")
        if self.zeros > self.ones:
            return "0"
        else:
            return "1"

    def least_common(self, default=None) -> str:
        if self.zeros == self.ones:
            if default is not None:
                return default
            else:
                raise Exception("I was not prepared to handle this!")
        if self.zeros < self.ones:
            return "0"
        else:
            return "1"

    def count_char(self, char: str) -> None:
        if char == "0":
            self.zeros += 1
        else:
            self.ones += 1


def q1(data: List[str]) -> int:
    line_length = len(data[0])
    trackers = [OccurenceTracker() for _ in range(line_length)]

    for line in data:
        for i, c in enumerate(line):
            trackers[i].count_char(c)

    gamma_string = "".join([tracker.most_common() for tracker in trackers])
    gamma = int(gamma_string, 2)
    epsilon = gamma ^ (2 ** line_length - 1)

    return gamma * epsilon


def q2(data: List[str]) -> int:
    line_length = len(data[0])

    oxygen_data = list(data)
    for position in range(line_length):
        tracker = OccurenceTracker()
        bins = {"0": [], "1": []}
        for line in oxygen_data:
            current_char = line[position]
            tracker.count_char(current_char)
            bins[current_char].append(line)
        oxygen_data = bins[tracker.most_common(default="1")]
    else:
        oxygen_rating = int(oxygen_data[0], 2)

    co2_data = list(data)
    for position in range(line_length):
        tracker = OccurenceTracker()
        bins = {"0": [], "1": []}
        for line in co2_data:
            current_char = line[position]
            tracker.count_char(current_char)
            bins[current_char].append(line)
        co2_data = bins[tracker.least_common(default="0")]
        if len(co2_data) == 1:
            break
    co2_rating = int(co2_data[0], 2)

    return oxygen_rating * co2_rating
