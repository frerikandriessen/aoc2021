from typing import List, Tuple, Dict
from queue import PriorityQueue, Queue


NODE = Tuple[int, int]


class RiskMap:
    def __init__(self, data: List[str]):
        self._data = data

    def value_at_location(self, location: Tuple[int, int]) -> int:
        return int(self._data[location[0]][location[1]])

    def find_neighbours(self, location: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours = []
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if abs(x) == abs(y):
                    continue
                neighbour = location[0] + y, location[1] + x
                if self.is_within_bounds(neighbour):
                    neighbours.append(neighbour)
        return neighbours

    def is_within_bounds(self, location: Tuple[int, int]) -> bool:
        y_within_bounds = 0 <= location[0] < len(self._data)
        x_within_bounds = 0 <= location[1] < len(self._data[0])
        return y_within_bounds and x_within_bounds

    @property
    def end(self) -> Tuple[int, int]:
        y = len(self._data) - 1
        x = len(self._data[0]) - 1
        return y, x


class PathFinder:
    def __init__(self, risk_map: RiskMap) -> None:
        self.risk_map = risk_map

        self.visited_dict: Dict[NODE, bool] = {}
        self.nodes_to_visit: Queue[Tuple[int, NODE]] = PriorityQueue()

        self.node_risks: Dict[NODE, int] = {}

    def find_path(self) -> int:

        self.nodes_to_visit.put((0, (0, 0)))
        self.node_risks[(0, 0)] = 0

        while not self.nodes_to_visit.empty():
            risk, current_node = self.nodes_to_visit.get()
            if self.visited_dict.get(current_node):
                continue

            self.visited_dict[current_node] = True

            if current_node == self.risk_map.end:
                return risk

            for neighbour in self.risk_map.find_neighbours(current_node):
                if self.visited_dict.get(neighbour):
                    continue
                risk_at_neighbour = self.risk_map.value_at_location(neighbour)
                new_risk = risk + risk_at_neighbour
                previous_risk = self.node_risks.get(neighbour)
                if previous_risk is None or previous_risk > new_risk:
                    self.node_risks[neighbour] = new_risk
                    self.nodes_to_visit.put((new_risk, neighbour))
        raise Exception("Could never find a good route")


def q1(data: List[str]) -> int:
    risk_map = RiskMap(data)
    path_finder = PathFinder(risk_map)
    return path_finder.find_path()


def enlarge_map(risk_map: List[str], enlargement_factor: int) -> List[str]:
    total_map = []
    for Y in range(enlargement_factor):
        for y, line in enumerate(risk_map):
            new_line = []
            for X in range(enlargement_factor):
                for x, value in enumerate(line):
                    new_value = int(value) + X + Y
                    if new_value > 9:
                        new_value = new_value % 9
                    new_line.append(str(new_value))
            total_map.append("".join(new_line))
    return total_map


def q2(data: List[str]) -> int:
    enlarged_map = enlarge_map(data, enlargement_factor=5)
    risk_map = RiskMap(enlarged_map)
    path_finder = PathFinder(risk_map)
    return path_finder.find_path()
