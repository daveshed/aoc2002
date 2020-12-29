from os import path

from toboggan import (
    count_trees,
    get_route,
    get_solution,
    load_forest,
    Slope,
)

HERE, _ = path.split(path.realpath(__file__))
EXAMPLE_INPUT = path.join(HERE, "input-example.txt")
REAL_INPUT = path.join(HERE, "input-day3.txt")
PART1_SLOPE = Slope(1, 3)
PART2_SLOPES = [
    Slope(1, 1),
    PART1_SLOPE,
    Slope(1, 5),
    Slope(1, 7),
    Slope(2, 1),
]

#### PART1
assert ''.join(get_route(load_forest(EXAMPLE_INPUT), PART1_SLOPE)) \
    == "..#.##.####"
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), PART1_SLOPE)) == 7

#### PART2
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), Slope(1, 1))) == 2
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), Slope(1, 3))) == 7
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), Slope(1, 5))) == 3
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), Slope(1, 7))) == 4
assert count_trees(get_route(load_forest(EXAMPLE_INPUT), Slope(2, 1))) == 2
assert get_solution(EXAMPLE_INPUT, PART2_SLOPES) == 336

print(
    "PART1 result -> "
    f"{count_trees(get_route(load_forest(REAL_INPUT), PART1_SLOPE))}"
)
print(f"PART2 result -> {get_solution(REAL_INPUT, PART2_SLOPES)}")
