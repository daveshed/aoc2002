"""
1. Subtract each entry off the target value (2020) -> remainders
2. Look through the entries for each remainder
"""
from os import path

HERE, _ = path.split(path.realpath(__file__))
EXAMPLE_INPUT = path.join(HERE, "input-example.txt")
DAY1_INPUT = path.join(HERE, "input-day1.txt")
TARGET = 2020

def get_entries(filename):
    """Get the entries from the file and return a set"""
    with open(filename, 'r') as file:
        return {int(line.strip()) for line in file}

def subtract(value, entries):
    """Subtract the entry off the value and return another set of remainders"""
    return {(value - entry) for entry in entries}

def get_common(a, b):
    """Retrieve elements in common between sets a and b"""
    return a & b

def get_summands(target, entries):
    remainders = subtract(target, entries)
    summands = get_common(entries, remainders)
    assert len(summands) % 2 == 0, "Should be an even number of summands"
    return summands

def get_solution_part1(entries):
    summand1, summand2 = get_summands(TARGET, entries)
    return summand1 * summand2

def get_solution_part2(entries):
    remainders = subtract(TARGET, entries)
    for remainder in remainders:
        # Can the remainder be made from any of the entries?
        summands = get_summands(target=remainder, entries=entries)
        if summands:
            summand1, summand2 = summands
            summand3 = (TARGET - remainder)
            return summand1 * summand2 * summand3
    return None


assert(get_solution_part1(get_entries(EXAMPLE_INPUT)) == 514579)
assert(get_solution_part2(get_entries(EXAMPLE_INPUT)) == 241861950)
print(get_solution_part1(get_entries(DAY1_INPUT)))
print(get_solution_part2(get_entries(DAY1_INPUT)))
