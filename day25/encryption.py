import math

TRANSFORM_INTEGER = 20201227
SUBJECT_INTEGER = 7
CARD_PUBLIC_KEY = 5764801
CARD_LOOP_SIZE = 8
DOOR_PUBLIC_KEY = 17807724
DOOR_LOOP_SIZE = 11
ENCRYPTION_KEY = 14897079


def read_keys(filename):
    with open(filename, 'r') as file:
        card_key = int(file.readline().strip())
        door_key = int(file.readline().strip())
        return card_key, door_key


def transform(loop_size: int, subject: int=SUBJECT_INTEGER) -> int:
    """Transform (exponentiation) operation described in the problem"""
    result = 1
    for _ in range(loop_size):
        result = (result * subject) % TRANSFORM_INTEGER
    return result


def discrete_logarithm(a, b, m):
    """
    Find k such that a^k cong b (mod m)
    via the baby step giant step algorithm

    Taken from geeksforgeeks
    """
    n = int(math.sqrt (m) + 1)

    # Calculate a ^ n
    an = 1;
    for i in range(n):
        an = (an * a) % m

    value = [0] * m

    # Store all values of a^(n*i) of LHS
    cur = an;
    for i in range(1, n + 1):
        if (value[ cur ] == 0):
            value[ cur ] = i
        cur = (cur * an) % m

    cur = b
    for i in range(n + 1):

        # Calculate (a ^ j) * b and check for collision
        if (value[cur] > 0):
            ans = value[cur] * n - i;
            if (ans < m):
                return ans
        cur = (cur * a) % m

    raise ValueError("No solution")


def inverse_transform(value: int):
    """Get the loop size from the result of a transform"""
    return discrete_logarithm(SUBJECT_INTEGER, value, TRANSFORM_INTEGER)


def inverse_transform_brute_force(value: int):
    """Get the loop size from the result of a transform"""
    # brute force method is very slow...
    i = 1
    while transform(i) != value:
        i += 1
    return i


def get_solution(filename):
    # 1. get the keys from the input...
    card_key, door_key = read_keys(filename)
    # 2. get the loop size for each of them...
    card_loops = inverse_transform(card_key)
    door_loops = inverse_transform(door_key)
    # 3. get the encryption key from each...
    encryption_key1 = transform(card_loops, door_key)
    encryption_key2 = transform(door_loops, card_key)
    # 4. they should match...
    assert encryption_key1 == encryption_key2
    # 5. Now we're done...
    return encryption_key1


# Tests against example input in the description...
assert CARD_PUBLIC_KEY == transform(CARD_LOOP_SIZE)
assert CARD_LOOP_SIZE == inverse_transform(CARD_PUBLIC_KEY)
assert DOOR_PUBLIC_KEY == transform(DOOR_LOOP_SIZE)
assert DOOR_LOOP_SIZE == inverse_transform(DOOR_PUBLIC_KEY)
assert ENCRYPTION_KEY == transform(DOOR_LOOP_SIZE, CARD_PUBLIC_KEY)
assert ENCRYPTION_KEY == transform(CARD_LOOP_SIZE, DOOR_PUBLIC_KEY)

# print the solution to the problem...
print(get_solution("puzzle-input.txt"))