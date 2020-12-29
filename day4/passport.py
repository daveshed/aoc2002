import re

_BIRTH_YEAR = re.compile("byr:\d{4}")
_ISSUE_YEAR = re.compile("iyr:\d{4}")
_EXPIRY_YEAR = re.compile("eyr:\d{4}")
_HEIGHT = re.compile("hgt:\d+(in|cm)")
_HAIR_COLOUR = re.compile("hcl:#()")

def is_valid(entry):
    """Validate a passport entry"""
    birthyear = _BIRTH_YEAR.search(entry).group()
    issueyear = _ISSUE_YEAR.search(entry).group()
    height = _HEIGHT.search(entry).group()
    print(locals())
    return True

