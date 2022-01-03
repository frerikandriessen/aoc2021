from typing import List, Dict


def preprocess_data(data: str) -> List[List[List[str]]]:
    processed_data = []
    for line in data.strip().split("\n"):
        signals, outputs = line.split("|")
        processed_data.append([signals.split(), outputs.split()])
    return processed_data


def q1(data: List[List[List[str]]]) -> int:
    counter = 0
    for _, outputs in data:
        for output in outputs:
            if len(output) in (2, 3, 4, 7):
                counter += 1

    return counter


def q2(data: List[List[List[str]]]) -> int:
    total_output = 0

    for signals, outputs in data:
        numbers = {}
        grouped_by_len: Dict[int, List[str]] = {}
        for signal in signals:
            length = len(signal)
            grouped_by_len[length] = grouped_by_len.get(length, []) + [signal]

            if len(signal) == 2:
                numbers[1] = signal
            elif len(signal) == 3:
                numbers[7] = signal
            elif len(signal) == 4:
                numbers[4] = signal
            elif len(signal) == 7:
                numbers[8] = signal

        for signal in grouped_by_len[6]:
            if not set(numbers[1]).issubset(set(signal)):
                numbers[6] = signal
            elif set(numbers[4]).issubset(set(signal)):
                numbers[9] = signal
            else:
                numbers[0] = signal

        for signal in grouped_by_len[5]:
            if set(numbers[1]).issubset(set(signal)):
                numbers[3] = signal
            elif set(signal).issubset(set(numbers[9])):
                numbers[5] = signal
            else:
                numbers[2] = signal

        line_output_string = ""
        for output in outputs:
            for value, number in numbers.items():
                if set(number) == set(output):
                    line_output_string += str(value)

        line_output = int(line_output_string)
        total_output += line_output

    return total_output
