import collections
from os import path

Slope = collections.namedtuple("Slope", ["down", "right"])

def load_forest(filename):
    """Get the forest row-by-row as a strings. # = tree, . = space"""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

def get_route(forest, slope):
    """Get the route of the toboggan through the forest as an iterable"""
    location = 0
    for row_idx, row in enumerate(forest):
        if row_idx % slope.down:
            # only report from rows that are multiples of the down component
            continue
        yield row[location % len(row)] # the patterns on each row repeat
        # each time we traverse a row, the location must increment by 3
        location += slope.right

def count_trees(route):
    return sum(1 for location in route if location == '#')

def get_solution(filename, slopes):
    # get all the trees encountered...
    results = (
        count_trees(get_route(load_forest(filename), slope))
        for slope in slopes
    )
    # multiply up...
    solution = 1
    for result in results:
        solution *= result
    return solution
