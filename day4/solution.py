from typing import List


def preprocess_data(data: str) -> List[str]:
    return data.strip().split("\n\n")


class BINGO(Exception):
    pass


class BingoCard:
    def __init__(self, card_numbers: str) -> None:
        self.number_to_coordinate_map = {}
        self.layout = []
        self.marked_numbers_map = []
        self.unmarked_numbers = set()

        rows = card_numbers.split("\n")
        for y, row_string in enumerate(rows):
            row = row_string.split()
            self.layout.append(row)
            self.marked_numbers_map.append([0] * len(row))

            for x, number in enumerate(row):
                self.number_to_coordinate_map[number] = (x, y)
                self.unmarked_numbers.add(number)

    def __repr__(self) -> str:
        return "\n".join(["\t".join(row) for row in self.layout])

    def pretty_marked_numbers(self) -> str:
        return "\n".join([" ".join(map(str, row)) for row in self.marked_numbers_map])

    def process_drawn_number(self, number: str) -> None:
        if number not in self.number_to_coordinate_map:
            return

        x, y = self.number_to_coordinate_map[number]

        self.marked_numbers_map[y][x] = 1
        self.unmarked_numbers.remove(number)

        self.check_for_bingo()

    def check_for_bingo(self) -> None:
        # fmt: off
        card_size = len(self.marked_numbers_map)

        # Scan rows for bingo
        for y in range(card_size):
            if all(
                self.marked_numbers_map[y][x] == 1
                for x in range(card_size)
            ):
                raise BINGO()

        # Scan columns for bingo
        for x in range(card_size):
            if all(
                self.marked_numbers_map[y][x] == 1
                for y in range(card_size)
            ):
                raise BINGO()
        # fmt: on

    def unmarked_numbers_sum(self) -> int:
        return sum(map(int, self.unmarked_numbers))


def q1(data: List[str]) -> int:
    numbers_to_draw: List[str] = data[0].split(",")

    bingo_cards = [BingoCard(card_numbers) for card_numbers in data[1:]]

    for number in numbers_to_draw:
        for bingo_card in bingo_cards:
            try:
                bingo_card.process_drawn_number(number)
            except BINGO:
                sum = bingo_card.unmarked_numbers_sum()
                return sum * int(number)
    else:
        raise Exception("This should not happen, no bingo was found??")


def q2(data: List[str]) -> int:
    numbers_to_draw: List[str] = data[0].split(",")

    bingo_cards = [BingoCard(card_numbers) for card_numbers in data[1:]]

    for number in numbers_to_draw:
        for bingo_card in list(bingo_cards):
            try:
                bingo_card.process_drawn_number(number)
            except BINGO:
                if len(bingo_cards) == 1:
                    sum = bingo_card.unmarked_numbers_sum()
                    return sum * int(number)
                else:
                    bingo_cards.remove(bingo_card)
    else:
        raise Exception("This should not happen, no bingo was found??")
