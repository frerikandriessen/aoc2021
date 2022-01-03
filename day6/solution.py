from typing import List


def preprocess_data(data: str) -> List[int]:
    return list(map(int, data.strip().split(",")))


def naive_solution(days: int, fish_timers: List[int]) -> int:
    for _ in range(days):
        for index, timer in list(enumerate(fish_timers)):
            if timer == 0:
                fish_timers[index] = 6
                fish_timers.append(8)
            else:
                fish_timers[index] = timer - 1
    return len(fish_timers)


def optimized_solution(days: int, fish_timers: List[int]) -> int:
    FISH_SPAWN_TIME = 7
    FISH_FIRST_SPAWN_TIME = 9
    planned_spawnings = [0] * (days + FISH_FIRST_SPAWN_TIME)

    total_fish = len(fish_timers)

    for days_till_spawning in fish_timers:
        planned_spawnings[days_till_spawning] += 1

    for day in range(days):
        spawn_count = planned_spawnings[day]
        planned_spawnings[day + FISH_SPAWN_TIME] += spawn_count
        planned_spawnings[day + FISH_FIRST_SPAWN_TIME] += spawn_count
        total_fish += spawn_count

    return total_fish


def q1(fish_timers: List[int]) -> int:
    return naive_solution(80, fish_timers)


def q2(fish_timers: List[int]) -> int:
    return optimized_solution(256, fish_timers)
