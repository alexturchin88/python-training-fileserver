import random


def generate_file_name(charset):
    length = random.randint(5, 10)
    return ''.join(random.choice(charset) for _ in range(length))
