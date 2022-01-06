from typing import List, Dict, Tuple
from collections import Counter
from abc import ABC, abstractmethod


def preprocess_data(data: str) -> List[str]:
    return data.strip().split("\n\n")


def create_insert_map(rules: str) -> Dict[str, str]:
    insert_map = {}
    for rule in rules.split("\n"):
        input, output = rule.split(" -> ")
        insert_map[input] = output
    return insert_map


def naive_pair_insertion_step(template: List[str], rules: Dict[str, str]) -> List[str]:
    new_template = []
    try:
        for i, value in enumerate(template):
            new_template.append(value)
            pair = template[i] + template[i + 1]
            new_char = rules[pair]
            new_template.append(new_char)
    except IndexError:
        pass
    return new_template


class InserterBase(ABC):
    def __init__(self, template: List[str], rules: Dict[str, str]) -> None:
        self.template = template
        self.rules = rules

    def perform_n_pair_insertions(self, n: int) -> None:
        for _ in range(n):
            self._pair_insertion()

    @abstractmethod
    def _pair_insertion(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def most_common_char(self) -> Tuple[str, int]:
        raise NotImplementedError

    @property
    @abstractmethod
    def least_common_char(self) -> Tuple[str, int]:
        raise NotImplementedError


class NaiveInserter(InserterBase):
    def _pair_insertion(self) -> None:
        new_template = []
        try:
            for i, value in enumerate(self.template):
                new_template.append(value)
                pair = self.template[i] + self.template[i + 1]
                new_char = self.rules[pair]
                new_template.append(new_char)
        except IndexError:
            pass
        self.template = new_template

    @property
    def most_common_char(self) -> Tuple[str, int]:
        return Counter(self.template).most_common()[0]

    @property
    def least_common_char(self) -> Tuple[str, int]:
        return Counter(self.template).most_common()[-1]


class OptimizedInserter(InserterBase):
    def __init__(self, template: List[str], rules: Dict[str, str]) -> None:
        super().__init__(template, rules)

        self.pair_counter = Counter("")
        for i, _ in enumerate(self.template[:-1]):
            pair = self.template[i] + self.template[i + 1]
            self.pair_counter[pair] += 1

        self.char_counter = Counter(self.template)

    def _pair_insertion(self) -> None:
        new_pair_counter = Counter("")
        for pair, count in self.pair_counter.items():
            new_char = self.rules[pair]
            self.char_counter[new_char] += count
            new_pair_counter[pair[0] + new_char] += count
            new_pair_counter[new_char + pair[1]] += count
        self.pair_counter = new_pair_counter

    @property
    def most_common_char(self) -> Tuple[str, int]:
        return self.char_counter.most_common()[0]

    @property
    def least_common_char(self) -> Tuple[str, int]:
        return self.char_counter.most_common()[-1]


def q1(data: List[str]) -> int:
    template, rules = data
    insert_map = create_insert_map(rules)

    inserter = NaiveInserter(list(template), insert_map)
    inserter.perform_n_pair_insertions(10)
    return inserter.most_common_char[1] - inserter.least_common_char[1]


def q2(data: List[str]) -> int:
    template, rules = data
    insert_map = create_insert_map(rules)

    inserter = OptimizedInserter(list(template), insert_map)
    inserter.perform_n_pair_insertions(40)
    return inserter.most_common_char[1] - inserter.least_common_char[1]
