from typing import List, Tuple, Dict


class HeightMap:
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

    def find_local_minima(self) -> Dict[Tuple[int, int], int]:
        low_points = {}
        for y, line in enumerate(self._data):
            for x, value in enumerate(line):
                if self.is_local_minimum((y, x)):
                    low_points[(y, x)] = int(value)
        return low_points

    def is_local_minimum(self, location: Tuple[int, int]) -> bool:
        y, x = location
        neighbours = self.find_neighbours(location)
        for yc, xc in neighbours:
            if int(self._data[y][x]) >= int(self._data[yc][xc]):
                return False
        return True


def q1(data: List[str]) -> int:
    hm = HeightMap(data)
    low_points = hm.find_local_minima()

    risk_level = 0
    for value in low_points.values():
        risk_level += value + 1
    return risk_level


class BasinVisitor:
    def __init__(self, start_location: Tuple[int, int], height_map: HeightMap):
        self.height_map = height_map

        self.locations_to_visit: List[Tuple[int, int]] = [start_location]
        self.already_visited: List[Tuple[int, int]] = []
        self.locations_in_basin: List[Tuple[int, int]] = []

    def calculate_basin_size(self) -> int:
        while len(self.locations_to_visit) != 0:
            new_location = self.locations_to_visit.pop()
            self.already_visited.append(new_location)
            if self.height_map.value_at_location(new_location) != 9:
                self.locations_in_basin.append(new_location)
                self.locations_to_visit += self.find_unvisited_neighbours(new_location)
        return len(self.locations_in_basin)

    def find_unvisited_neighbours(
        self, location: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        unvisited_neighbours = []
        neighbours = self.height_map.find_neighbours(location)
        for neighbour in neighbours:
            if (
                neighbour not in self.already_visited
                and neighbour not in self.locations_to_visit
            ):
                unvisited_neighbours.append(neighbour)
        return unvisited_neighbours


def q2(data: List[str]) -> int:
    hm = HeightMap(data)
    low_points = hm.find_local_minima()
    basin_sizes = [BasinVisitor(lp, hm).calculate_basin_size() for lp in low_points]

    total = 1
    for b in sorted(basin_sizes)[-3:]:
        total *= b
    return total
