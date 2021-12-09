from typing import List, Tuple

def find_neighbours(start_coordinate, data):
    coordinates = []
    for y in (-1, 0, 1):
        for x in (-1, 0, 1):
            if (y,x) == (0, 0):
                continue
            if y != 0 and x != 0:
                continue
            coordinate = start_coordinate[0] + y, start_coordinate[1] + x
            if 0 <= coordinate[0] < len(data) and 0 <= coordinate[x] < len(data[0]):
                coordinates.append(coordinate)
    return coordinates

def find_low_points(data: List[str]):
    low_points = {}

    for y, line in enumerate(data):
        for x, value in enumerate(line):
            coordinates_to_check = find_neighbours((y, x), data)
            for yc, xc in coordinates_to_check:
                #if 0 <= yc < len(data) and 0 <= xc < len(line):
                    # print(f"{y},{x}: {value}")
                    # print(f"{yc},{xc}: {int(data[yc][xc])}")
                if int(value) >= int(data[yc][xc]):
                    break
            else:
                low_points[(y,x)] = int(value)
    return low_points

def q1(data: List[str]) -> int:
    risk_level = 0
    low_points = find_low_points(data)
    for lp, value in low_points.items():
        risk_level += value + 1

    # for y, line in enumerate(data):
    #     for x, value in enumerate(line):
    #         coordinates_to_check = find_neighbours((y, x))
    #         for yc, xc in coordinates_to_check:
    #             if 0 <= yc < len(data) and 0 <= xc < len(line):
    #                 # print(f"{y},{x}: {value}")
    #                 # print(f"{yc},{xc}: {int(data[yc][xc])}")
    #                 if int(value) >= int(data[yc][xc]):
    #                     break
    #         else:
    #             risk_level += int(value) + 1
    #         # value = int(value)

    #         # if y != 0:
    #         #     if value 
                

    return risk_level


def get_neighbours_to_check(coordinate: Tuple[str], data: List[str], already_visited: List[Tuple[int]], already_going_to_check):
    neighbours_to_check = []
    coordinates = find_neighbours(coordinate, data)
    for c in coordinates:
        if c not in already_visited and c not in already_going_to_check:
            # print(f"Already visited: {already_visited}")
            # print(f"This coordinate: {c}")
            neighbours_to_check.append(c)
        # else:
        #     print(f"I'm skipping {c}")
    return neighbours_to_check

def calculate_basin_size(low_point, data):
    locations_to_check = []
    already_visited = []
    locations_in_basin = []
    locations_to_check = [low_point]


    while len(locations_to_check) != 0:
        new_location = locations_to_check.pop()
        # print(f"Currently checking {new_location}. Already visited: {already_visited}")
        already_visited.append(new_location)
        y, x = new_location
        if int(data[y][x]) != 9:
            locations_in_basin.append(new_location)
            neighbours_to_check = get_neighbours_to_check(new_location, data, already_visited, locations_to_check)
            locations_to_check += neighbours_to_check
        # print(f"Locations to check: {locations_to_check}")
    
    
    # print(f"Locations in basin: {locations_in_basin}")
    return len(locations_in_basin)
    

def q2(data) -> int:
    low_points = find_low_points(data)
    print(f"Low points: {low_points}")
    basin_sizes = []
    for lp in low_points:
        size = calculate_basin_size(lp, data)
        print(size)
        basin_sizes.append(size)

    largest_three = sorted(basin_sizes)[-3:]
    total = 1
    for b in largest_three:
        total *= b
    return total