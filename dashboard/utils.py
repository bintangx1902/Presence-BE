import string, random


def generate_agency_code():
    letter = string.ascii_letters
    num = '0123456789'
    raw = letter + num
    return ''.join(random.sample(raw, 32))
