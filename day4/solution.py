from typing import List


class BingoCard:
    def __init__(self):
        self.number_to_coordinate_map = {}
        self.drawn_numbers_map = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]

    @property
    def layout(self):
        card = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        print(self.number_to_coordinate_map)
        for number, coordinates in self.number_to_coordinate_map.items():
            card[coordinates["y"]][coordinates["x"]] = number

        return card

    def __repr__(self):
        return "\n".join(map(str, self.layout))

    def process_drawn_number(self, number):
        coordinates = self.number_to_coordinate_map.get(number)
        if coordinates is None:
            return

        self.drawn_numbers_map[coordinates["y"]][coordinates["x"]] = 1

    def check_for_bingo(self):
        card_size = len(self.drawn_numbers_map)

        # Scan rows for bingo
        for i in range(card_size):
            for j in range(card_size):
                is_drawn = self.drawn_numbers_map[i][j]
                if not is_drawn:
                    break
            else:
                print(f"BINGO!!!!!!!!!!!")
                return True

        # Scan columns for bingo
        for i in range(card_size):
            for j in range(card_size):
                is_drawn = self.drawn_numbers_map[j][i]
                if not is_drawn:
                    break
            else:
                print(f"BINGO!!!!!!!!!!!")
                return True

    def unmarked_numbers_sum(self):
        total_sum = 0
        for number, coordinates in self.number_to_coordinate_map.items():
            is_marked = self.drawn_numbers_map[coordinates["y"]][coordinates["x"]]
            if not is_marked:
                total_sum += int(number)
        return total_sum

def q1(data: List[str]) -> int:
    # Create boards by:
    # Saving a map with the coordinates for each number, that way when a new number is pulled you can access it in O(1)
    # Save a meta map with markings

    # Pull new number
    # Update board with new number    # Assume no boards can win at the same time
    # Check if board has BINGO by:
        # Looping through the rows and the columns.
    # If so: calculate total
    numbers_to_draw: List[str] = data[0].split(",")

    bingo_cards: List[BingoCard] = []

    no_of_cards = int(len(data[1:]) / 6)
    print(no_of_cards)

    for card_number in range(no_of_cards):

        bingo_card = BingoCard()
        start_index = card_number * 6 + 2

        for i in range(5):
            row_of_numbers = data[start_index + i].split()
            for j, number in enumerate(row_of_numbers):
                bingo_card.number_to_coordinate_map[number] = {"x": j, "y": i}

        bingo_cards.append(bingo_card)
    print(bingo_cards[0])


    for number in numbers_to_draw:
        for bingo_card in bingo_cards:
            bingo_card.process_drawn_number(number)
            if bingo_card.check_for_bingo():
                print(f"Oh yeahhh BINGO!!")
                print(bingo_card)
                print(bingo_card.drawn_numbers_map)

                sum = bingo_card.unmarked_numbers_sum()
                print(sum)
                print(sum * int(number))
                return sum * int(number)


    for bingo_card in bingo_cards:
        print(bingo_card.drawn_numbers_map)

def q2(data: List[str]) -> int:
    numbers_to_draw: List[str] = data[0].split(",")

    bingo_cards: List[BingoCard] = []

    no_of_cards = int(len(data[1:]) / 6)
    print(no_of_cards)

    for card_number in range(no_of_cards):

        bingo_card = BingoCard()
        start_index = card_number * 6 + 2

        for i in range(5):
            row_of_numbers = data[start_index + i].split()
            for j, number in enumerate(row_of_numbers):
                bingo_card.number_to_coordinate_map[number] = {"x": j, "y": i}

        bingo_cards.append(bingo_card)
    print(bingo_cards[0])


    for number in numbers_to_draw:
        for index, bingo_card in enumerate(list(bingo_cards)):
            bingo_card.process_drawn_number(number)
            if bingo_card.check_for_bingo():
                print(f"BINGO, removing this card")
                print(bingo_card)
                print(bingo_card.drawn_numbers_map)

                if len(bingo_cards) != 1:
                    #print(f"Popping at index {index} from list with lenght: {len(bingo_cards)}")
                    bingo_cards.remove(bingo_card)
                else:
                    sum = bingo_card.unmarked_numbers_sum()
                    print(sum)
                    print(sum * int(number))
                    return sum * int(number)


    for bingo_card in bingo_cards:
        print(bingo_card.drawn_numbers_map)