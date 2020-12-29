import collections
from os import path
import re

HERE, _ = path.split(path.realpath(__file__))
EXAMPLE_INPUT = path.join(HERE, "input-example.txt")
EXAMPLE_INPUT2 = path.join(HERE, "input-day2-first-20.txt")
REAL_INPUT = path.join(HERE, "input-day2.txt")
REGEX = re.compile("(\d+)-(\d+) (\w): (\w+)")

ParsedPasswordEntry = collections.namedtuple(
    "ParsedEntry",
    [
        "param1",
        "param2",
        "token",
        "password",
    ]
)

def get_lines(filename):
    """Get the entries from the file line by line"""
    with open(filename, 'r') as file:
        for line in file:
            yield line

def parse_line(line):
    """Take the input line and return a tuple of everything"""
    try:
        (param1, param2, token, password) = \
            REGEX.match(line).groups()
        param1 = int(param1)
        param2 = int(param2)
        token = str(token)
        password = str(password)
        return ParsedPasswordEntry(
            param1,
            param2,
            token,
            password
        )
    except AttributeError as error:
        raise AssertionError(f"Could not parse '{line}'")

def is_valid_part1(entry):
    """
    Validate the password against the rule (part 1)

    The token must appear at the correct frequency.
    """
    actual_frequency = entry.password.count(entry.token)
    min_frequency = entry.param1
    max_frequency = entry.param2
    return min_frequency <= actual_frequency <= max_frequency

def is_valid_part2(entry):
    """
    Validate the password against the rule (part 2)

    Position 1 must contain the token and position 2 must not.
    """
    # note that positions are 1 indexed
    pos1 = entry.param1 - 1
    pos2 = entry.param2 - 1

    result = (entry.password[pos1] == entry.token) \
        and (entry.password[pos2] != entry.token)
    print(f"{entry} -> {result}")
    return result

def count_valid_passwords(filename, validator):
    valid_entries = filter(validator, map(parse_line, get_lines(filename)))
    return sum(1 for entry in valid_entries)

assert (count_valid_passwords(EXAMPLE_INPUT2, is_valid_part2) == 7), count_valid_passwords(EXAMPLE_INPUT2, is_valid_part2)


# # check the parser/validators...
# # PART1
# assert (is_valid_part1(parse_line("1-8 n: dpwpmhknmnlglhjtrbpx")))
# assert (not is_valid_part1(parse_line("2-6 b: ab")))
# assert (count_valid_passwords(EXAMPLE_INPUT, is_valid_part1) == 2)
# # PART2
# assert (is_valid_part2(parse_line("1-3 a: abcde")))
# assert (not is_valid_part2(parse_line("1-3 b: cdefg")))
# assert (not is_valid_part2(parse_line("2-9 c: ccccccccc")))
# assert (not is_valid_part2(parse_line("2-9 c: cbccccccc")))
# assert (count_valid_passwords(EXAMPLE_INPUT, is_valid_part2) == 1)
# assert (count_valid_passwords(EXAMPLE_INPUT2, is_valid_part2) == 7), count_valid_passwords(EXAMPLE_INPUT2, is_valid_part2)
# # show the solution...
# print(
#     "PART1: valid passwords -> "
#     f"{count_valid_passwords(REAL_INPUT, is_valid_part1)}"
# )
print(
    "PART2: valid passwords -> "
    f"{count_valid_passwords(REAL_INPUT, is_valid_part2)}"
)
