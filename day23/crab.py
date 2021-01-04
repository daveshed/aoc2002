import itertools
import sys

from linkedlist import CircularLinkedList

N_CUPS = int(1E6)
N_MOVES = int(1E7)

def make_cups(labels: str) -> list:
    """Make the cups as a list from the string of cup labels"""
    return CircularLinkedList(int(label) for label in labels)

def make_cups_part_2(labels: str, total: int=N_CUPS) -> list:
    """Make the cups from the string of cup labels as described in part 1.
    Additional cups are then added until the total is reached"""
    part1 = [int(label) for label in labels]
    max_label = max(part1) + (total - len(part1))
    # FIXME: Very inefficient to create two lists. We should just have one long
    #        generator.
    padding = list(range(max(part1) + 1, max_label + 1))
    part2 = part1 + padding
    assert len(part2) == total
    return CircularLinkedList(part2)

def move_cups(current: int, cups: CircularLinkedList) -> int: # return the new current cup
    """
    1. The crab picks up the three cups that are immediately clockwise of the
       current cup. They are removed from the circle; cup spacing is adjusted
       as necessary to maintain the circle.
    2. The crab selects a destination cup: the cup with a label equal to the
       current cup's label minus one. If this would select one of the cups that
       was just picked up, the crab will keep subtracting one until it finds a
       cup that wasn't just picked up. If at any point in this process the value
       goes below the lowest value on any cup's label, it wraps around to the
       highest value on any cup's label instead.
    3. The crab places the cups it just picked up so that they are immediately
       clockwise of the destination cup. They keep the same order as when they
       were picked up.
    4. The crab selects a new current cup: the cup which is immediately
       clockwise of the current cup.

    Note that the current cup is specified by its label.
    """
    # Pick up some cups from the next available location...
    adjacent = cups.next(current)
    picked_up = cups.to_list(location=adjacent, length=3)
    # find the destination cup...
    target = current - 1
    counter = 0
    while (target in picked_up) or (target not in cups):
        target -= 1
        counter += 1
        if target < 0:
            target = max(cups)
        if counter > len(cups):
            raise AssertionError("Stuck!")
    # move the cups...
    cups.move(dst=target, src=adjacent, length=3)
    # return the new current cup...
    return cups.next(current)

def get_order(cups: CircularLinkedList) -> str:
    """The order of labels from cup `1`"""
    rotated = cups.to_list(location=1)
    return ''.join(str(label) for label in rotated[1:])

def solution_part_1(labels: str, moves: int) -> str:
    cups = make_cups(labels)
    current_cup = int(labels[0])
    for _ in range(moves):
        current_cup = move_cups(current_cup, cups)
    return get_order(cups)

def solution_part_2(labels: str, moves: int=N_MOVES) -> int:
    cups = make_cups_part_2(labels)
    current_cup = int(labels[0])
    for i in range(moves):
        if not i % (moves / 100):
            print(f"{(i / moves * 100):3.0f}% complete...")
        current_cup = move_cups(current_cup, cups)
    next_cup = cups.next(location=1)
    next_next_cup = cups.next(location=next_cup)
    return str(next_cup * next_next_cup)

# The actual solutions...
if __name__ == '__main__':
    problem_input = sys.argv[1]
    print(solution_part_1(labels=problem_input, moves=100))
    print(solution_part_2(labels=problem_input, moves=int(1E7)))
