from typing import List


class PositionBase:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def process_instruction(self, instruction: str):
        command_map = {
            "forward": self.forward,
            "up": self.up,
            "down": self.down,
        }

        command, value = instruction.split(" ")[0], int(instruction.split(" ")[1])
        command_map[command](value)

    def result(self):
        return self.horizontal * self.depth


class PositionQ1(PositionBase):
    def down(self, value: int) -> None:
        self.depth += value

    def up(self, value: int) -> None:
        self.depth -= value

    def forward(self, value: int) -> None:
        self.horizontal += value


class PositionQ2(PositionBase):
    def __init__(self):
        super().__init__()
        self.aim = 0

    def down(self, value: int) -> None:
        self.aim += value

    def up(self, value: int) -> None:
        self.aim -= value

    def forward(self, value: int) -> None:
        self.horizontal += value
        self.depth += self.aim * value


def q1(data: List[str]) -> int:
    position = PositionQ1()

    for line in data:
        position.process_instruction(line)

    return position.result()


def q2(data: List[str]) -> int:
    position = PositionQ2()

    for line in data:
        position.process_instruction(line)

    return position.result()
