from typing import List
import textwrap


class WrongBracketError(Exception):
    pass


class BracketChecker:
    bracket_matches = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }
    opening_brackets = ("(", "[", "{", "<")

    def __init__(self, line: str):
        self.line = line
        self.opened_brackets: List[str] = []
        self.index = 0

    @property
    def bracket(self) -> str:
        if len(self.opened_brackets) == 0:
            return ""
        return self.opened_brackets[-1]

    def process_line(self) -> None:
        for index, bracket in enumerate(self.line):
            self.index = index
            if bracket in self.opening_brackets:
                self.opened_brackets.append(bracket)
                continue

            if bracket != self.bracket_matches[self.bracket]:
                error_msg = textwrap.dedent(
                    f"""\
                    Syntax error, expected {self.bracket_matches[self.bracket]} but got {bracket}
                    {self.line}, problem occurs at index {self.index}
                    {" " * index + "^"}
                    """
                )
                raise WrongBracketError(error_msg)
            else:
                self.opened_brackets.pop()

    def find_missing_brackets(self) -> List[str]:
        return [self.bracket_matches[b] for b in reversed(self.opened_brackets)]


def q1(data: List[str]) -> int:
    bracket_values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    score = 0
    for line in data:
        bracket_checker = BracketChecker(line)
        try:
            bracket_checker.process_line()
        except WrongBracketError:
            score += bracket_values[bracket_checker.line[bracket_checker.index]]
    return score


def q2(data: List[str]) -> int:
    bracket_values = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    scores = []

    for line in data:
        bracket_checker = BracketChecker(line)
        try:
            bracket_checker.process_line()
            missing_brackets = bracket_checker.find_missing_brackets()

            score = 0
            for bracket in missing_brackets:
                value = bracket_values[bracket]
                score = score * 5 + value
            scores.append(score)
        except WrongBracketError:
            pass
    scores.sort()
    return scores[int((len(scores) - 1) / 2)]
