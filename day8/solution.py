from typing import List


def preprocess_data(data):
    data = data.strip().split("\n")
    processed_data = []
    for line in data:
        signals, outputs = line.split("|")
        processed_data.append([signals.split(), outputs.split()])
    return processed_data



def q1(data) -> int:
    counter = 0
    for signals, outputs in data:
        for output in outputs:
            if len(output) in (2, 3, 4, 7):
                counter += 1

    return counter

# table = {
#     "1": "CF",
#     "7": "ACF",
#     "4": "BCDF",
#     "2": "ACDEG",
#     "3": "ACDFG",
#     "5": "ABDFG",
#     "0": "ABCEFG",
#     "6": "ABDEFG",
#     "9": "ABCDFG",
#     "8": "ABCDEFG",
#     "8-9": "E",
#     "8-6": "C",
#     "8-0": "D",
#     "7-1": "A",
#   6-5: E,
#   6-3: BE -C
# }

# conv = {}




def q2(data) -> int:

    total_output = 0
    for signals, outputs in data:
        print(signals, outputs)
        conv = {}
        numbers = {}
        grouped_by_len = {}
        for signal in signals:
            length = len(signal)
            grouped_by_len[length] = grouped_by_len.get(length, []) + [signal]

            if len(signal) == 2:
                numbers["1"] = signal
            elif len(signal) == 3:
                numbers["7"] = signal
            elif len(signal) == 4:
                numbers["4"] = signal
            elif len(signal) == 7:
                numbers["8"] = signal
        
        print(grouped_by_len)
        conv["A"] = (set(numbers["7"]) - set(numbers["1"])).pop()

        for signal in grouped_by_len[6]:
            if len(set(numbers["1"]) - set(signal)) != 0:
                print(f"Found number 6!")
                numbers["6"] = signal
            if len(set(signal) - set(numbers["4"])) == 2:
                print("Found number 9")
                numbers["9"] = signal
        for signal in grouped_by_len[6]:
            if signal not in (numbers["6"], numbers["9"]):
                print("Found number 0")
                numbers["0"] = signal
        
        conv["C"] = (set(numbers["8"]) - set(numbers["6"])).pop()
        print(f"leter 'C' is here: {conv['C']}")
        for signal in grouped_by_len[5]:
            if len(set(numbers["1"]) - set(signal)) == 0:
                print(f"Found number 3!: {signal}")
                numbers["3"] = signal
            elif len(set(signal) - set(conv["C"])) == 5:
                print(f"Found number 5: {signal}")
                numbers["5"] = signal
            else:
                print(f"Found number 2: {signal}")
                numbers["2"] = signal

        conv["G"] = (set(numbers["3"]) - set(numbers["4"]) - set(conv["A"])).pop()
        
        # print(len(numbers))
        print(numbers)
        # print(conv)

        line_output_string = ""
        for output in outputs:
            for value, number in numbers.items():
                if set(number) == set(output):
                    line_output_string += value

        line_output = int(line_output_string)
        print(f"Value found: {line_output}")

        total_output += line_output

        # print("Exiting prematurely")
        # exit(1)
    return total_output