import itertools



def rotate(x: list, shift: int) -> list:
    """Rotate a list by `shift` places"""
    return x[-shift:] + x[:-shift]

def make_cups(labels: str) -> list:
    """Make the cups as a list from the string of cup labels"""
    return [int(label) for label in labels]

def pick_up(cups: list, current: int) -> list:
    """Grab the three cups to be moved from the cup circle. They should be taken
    from the positions immediately clockwise of the current cup specified by
    index.

    Note that this call will wrap to the start of the list if the current index
    is near to the end of the list."""
    result = []
    circle = itertools.cycle(cups)
    i = 0
    while len(result) < 3:
        cup = next(circle)
        i += 1
        if i > (current + 1):
            result.append(cup)
    return result

def move_cups(current, cups):
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

    Note that the current cup is specified by its index in the list.
    """
    # 1a. store the current cup label...
    cur_label = cups[current]
    # 1b. pick up the cups...
    picked_up = pick_up(cups, current)
    # 1c. remove them from the circle
    insert_into = [cup for cup in cups if cup not in picked_up]
    # 2. select the destination cup...
    dst_label = cups[current] - 1
    while True:
        if dst_label not in picked_up:
            try:
                dst_idx = insert_into.index(dst_label)
                break
            except ValueError:
                pass
        dst_label -= 1
        if dst_label < 0:
            dst_label = max(cups)
    # 3. insert the cups back at the target idx
    result = insert_into[:dst_idx + 1] + picked_up + insert_into[dst_idx + 1:]
    # now normalise the indices so that the current cup is at the same index as
    # before...
    result = rotate(
        x=result,
        shift=(cups.index(cur_label) - result.index(cur_label)))
    return result

# Tests based on example input part1...
cups = make_cups("389125467")
expected_cups = [
    # [3, 8, 9, 1, 2, 5, 4, 6, 7], # initial state
    [3, 2, 8, 9, 1, 5, 4, 6, 7],
    [3, 2, 5, 4, 6, 7, 8, 9, 1],
    [7, 2, 5, 8, 9, 1, 3, 4, 6],
    [3, 2, 5, 8, 4, 6, 7, 9, 1],
    [9, 2, 5, 8, 4, 1, 3, 6, 7],
    [7, 2, 5, 8, 4, 1, 9, 3, 6],
    [8, 3, 6, 7, 4, 1, 9, 2, 5],
    [7, 4, 1, 5, 8, 3, 9, 2, 6],
    [5, 7, 4, 1, 8, 3, 9, 2, 6],
    [5, 8, 3, 7, 4, 1, 9, 2, 6],
]
for i, expect in enumerate(expected_cups):
    cups = move_cups(i % len(cups), cups)
    assert expect == cups, f"FAILED...move {i + 1}: {expect} != {cups}"
