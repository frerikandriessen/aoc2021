from typing import Any, List, Union, Tuple, Optional, Protocol
import json
from math import floor, ceil

SnailType = Union[int, Tuple[Any, Any]]


class Explosion(Exception):
    pass


class Split(Exception):
    pass


class Snail(Protocol):
    parent: Optional["SnailPair"]
    depth: int
    position: Optional[str]
    value: int

    @property
    def magnitude(self) -> int:
        ...

    def update_depth(self, modifier: int) -> None:
        ...

    def find_most_right_leaf(self) -> "SnailRegularNumber":
        ...

    def find_most_left_leaf(self) -> "SnailRegularNumber":
        ...

    def check_for_explosions(self) -> None:
        ...

    def check_for_split(self) -> None:
        ...


class SnailPair(Snail):
    def __init__(
        self,
        pair: Tuple[Snail, Snail],
        parent: Optional["SnailPair"],
        depth: int,
        position: Optional[str],
    ):
        self.parent = parent
        self.position = position
        self.depth = depth

        self.left, self.right = pair

    @classmethod
    def from_tuple(
        cls,
        pair: Tuple[SnailType, SnailType],
        parent: Optional["SnailPair"],
        depth: int,
        position: Optional[str],
    ) -> "SnailPair":
        left, right = pair

        if isinstance(left, int):
            left_obj: Snail = SnailRegularNumber(left, None, depth + 1, "left")
        else:
            left_obj = SnailPair.from_tuple(left, None, depth + 1, "left")
        if isinstance(right, int):
            right_obj: Snail = SnailRegularNumber(right, None, depth + 1, "right")
        else:
            right_obj = SnailPair.from_tuple(right, None, depth + 1, "right")

        snail_pair = cls((left_obj, right_obj), parent, depth, position)
        left_obj.parent = snail_pair
        right_obj.parent = snail_pair
        return snail_pair

    @property
    def value(self) -> int:  # type: ignore
        return self.left.value + self.right.value

    @property
    def magnitude(self) -> int:
        return self.left.magnitude * 3 + self.right.magnitude * 2

    def add(self, other: Snail) -> "SnailPair":
        new_pair = SnailPair((self, other), parent=None, depth=0, position=None)
        new_pair.left.parent = new_pair
        new_pair.left.position = "left"
        new_pair.left.update_depth(1)

        new_pair.right.parent = new_pair
        new_pair.right.position = "right"
        new_pair.right.update_depth(1)
        return new_pair

    def update_depth(self, modifier: int) -> None:
        self.depth += modifier
        self.left.update_depth(modifier)
        self.right.update_depth(modifier)

    def find_most_right_leaf(self) -> "SnailRegularNumber":
        return self.right.find_most_right_leaf()

    def find_most_left_leaf(self) -> "SnailRegularNumber":
        return self.left.find_most_left_leaf()

    def check_for_explosions(self) -> None:
        if self.depth >= 4:
            self.explode()
        else:
            self.left.check_for_explosions()
            self.right.check_for_explosions()

    def check_for_split(self) -> None:
        self.left.check_for_split()
        self.right.check_for_split()

    def explode(self) -> None:
        if self.parent is None:
            raise Exception("Why are we trying to explode the root node??")
        if not isinstance(self.left, SnailRegularNumber) or not isinstance(
            self.right, SnailRegularNumber
        ):
            raise Exception("We are trying to explode but not all leafs are integers.")

        if self.position == "right":
            closest_left = self.parent.left.find_most_right_leaf()
            closest_left.value += self.left.value

            parent = self.parent
            while True:
                if parent.parent is None:
                    break
                elif parent.position == "right":
                    parent = parent.parent
                else:
                    closest_right = parent.parent.right.find_most_left_leaf()  # type: ignore  # noqa:E501
                    closest_right.value += self.right.value
                    break
            self.parent.right = SnailRegularNumber(
                value=0, parent=self.parent, depth=self.depth, position="right"
            )

        if self.position == "left":
            closest_right = self.parent.right.find_most_left_leaf()
            closest_right.value += self.right.value

            parent = self.parent
            while True:
                if parent.parent is None:
                    break
                elif parent.position == "left":
                    parent = parent.parent
                else:
                    closest_left = parent.parent.left.find_most_right_leaf()  # type: ignore  # noqa:E501
                    closest_left.value += self.left.value
                    break
            self.parent.left = SnailRegularNumber(
                value=0, parent=self.parent, depth=self.depth, position="left"
            )

        raise Explosion(f"Exploded for {self}")


class SnailRegularNumber(Snail):
    def __init__(
        self,
        value: int,
        parent: Optional[SnailPair],
        depth: int,
        position: Optional[str],
    ):
        self.parent = parent
        self.position = position
        self.depth = depth

        self.value = value

    @property
    def magnitude(self) -> int:
        return self.value

    def find_most_right_leaf(self) -> "SnailRegularNumber":
        return self

    def find_most_left_leaf(self) -> "SnailRegularNumber":
        return self

    def update_depth(self, modifier: int) -> None:
        self.depth += modifier

    def check_for_explosions(self) -> None:
        pass

    def check_for_split(self) -> None:
        if self.value >= 10:
            self.split()

    def split(self) -> None:
        if self.parent is None:
            raise Exception("I can't split when parent is None")
        left, right = int(floor(self.value / 2)), int(ceil(self.value / 2))
        new_pair = SnailPair.from_tuple(
            (left, right), parent=self.parent, depth=self.depth, position=self.position
        )
        if self.position == "left":
            self.parent.left = new_pair
        else:
            self.parent.right = new_pair

        raise Split(f"Done a split for {self} into {new_pair}")


def add_and_reduce(n1: SnailPair, n2: SnailPair) -> SnailPair:
    new_number = n1.add(n2)
    while True:
        try:
            new_number.check_for_explosions()
        except Explosion:
            continue

        try:
            new_number.check_for_split()
        except Split:
            continue

        return new_number


def q1(data: List[str]) -> int:
    number = None
    for line in data:
        snail_number = json.loads(line)
        sp = SnailPair.from_tuple(snail_number, parent=None, depth=0, position=None)

        if number is None:
            number = sp
        else:
            number = add_and_reduce(number, sp)

    if number is None:
        raise Exception("No snail numbers have been processed at all!")

    return number.magnitude


def q2(data: List[str]) -> int:
    max_magnitude = 0
    for line in data:
        for line2 in data:
            if line == line2:
                continue
            sn1 = json.loads(line)
            sp1 = SnailPair.from_tuple(sn1, parent=None, depth=0, position=None)
            sn2 = json.loads(line2)
            sp2 = SnailPair.from_tuple(sn2, parent=None, depth=0, position=None)

            combined_number = add_and_reduce(sp1, sp2)
            magnitude = combined_number.magnitude

            if magnitude > max_magnitude:
                max_magnitude = magnitude
    return max_magnitude
