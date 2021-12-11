from typing import List, Tuple, Iterator


class Octopus:
    def __init__(self, energy: int, location: Tuple[int, int]):
        self.energy = energy
        self.location = location
        self.has_flashed = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(energy={self.energy}, @{self.location})"


class OctopusMap:
    def __init__(self, data: List[str]):
        self._data = data
        self._octopus_map = [
            [Octopus(int(energy), (y, x)) for x, energy in enumerate(line)]
            for y, line in enumerate(self._data)
        ]

    def __iter__(self) -> Iterator[Tuple[Tuple[int, int], Octopus]]:
        for y, line in enumerate(self._octopus_map):
            for x, octopus in enumerate(line):
                yield (y, x), octopus

    @property
    def size(self) -> int:
        return len(self._data) * len(self._data[0])

    def get_octopus(self, location: Tuple[int, int]) -> Octopus:
        return self._octopus_map[location[0]][location[1]]

    def find_neighbours(self, octopus: Octopus) -> List[Octopus]:
        neighbours = []
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if x == y == 0:
                    continue
                location = octopus.location[0] + y, octopus.location[1] + x
                if self.is_within_bounds(location):
                    neighbour = self.get_octopus(location)  # aka squidward
                    neighbours.append(neighbour)
        return neighbours

    def is_within_bounds(self, location: Tuple[int, int]) -> bool:
        y_within_bounds = 0 <= location[0] < len(self._data)
        x_within_bounds = 0 <= location[1] < len(self._data[0])
        return y_within_bounds and x_within_bounds

    def print_current_map(self) -> None:
        for line in self._octopus_map:
            print([o.energy for o in line])


class OctopusScientist:
    def __init__(self, octopus_map: OctopusMap):
        self.octopus_map = octopus_map
        self.flashed_octopi: List[Octopus] = []

    def increase_octopus_energy(self, octopus: Octopus) -> None:
        octopus.energy += 1
        if octopus.energy > 9 and not octopus.has_flashed:
            self.flash_octopus(octopus)

    def flash_octopus(self, octopus: Octopus) -> None:
        octopus.has_flashed = True
        self.flashed_octopi.append(octopus)

        neighbours = self.octopus_map.find_neighbours(octopus)
        for neighbour in neighbours:
            self.increase_octopus_energy(neighbour)

    def perform_step(self) -> int:
        for _, octopus in self.octopus_map:
            self.increase_octopus_energy(octopus)

        flashes = len(self.flashed_octopi)

        for octopus in self.flashed_octopi:
            octopus.energy = 0
            octopus.has_flashed = False

        self.flashed_octopi = []
        return flashes


def q1(data: List[str]) -> int:
    octopus_map = OctopusMap(data)
    scientist = OctopusScientist(octopus_map)
    return sum([scientist.perform_step() for _ in range(100)])


def q2(data: List[str]) -> int:
    octopus_map = OctopusMap(data)
    scientist = OctopusScientist(octopus_map)
    step = 0
    while True:
        step += 1
        flashes_in_step = scientist.perform_step()
        if flashes_in_step == octopus_map.size:
            return step
