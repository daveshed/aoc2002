from os import path

HERE, _ = path.split(path.realpath(__file__))
EXAMPLE_INPUT = path.join(HERE, "input-example.txt")
# REAL_INPUT = path.join(HERE, "input-day1.txt")

def get_entries(filename):
    """Get the entries from the file and return a set"""
    with open(filename, 'r') as file:
        for line in
        return int(line.strip()) for line in file

