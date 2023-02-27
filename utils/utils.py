import random


def generate_file_name(charset: str) -> str:
    """
    Generate a random filename
    :param charset: string of characters to be used for generation
    :returns string filename
    """
    length = random.randint(5, 10)
    return ''.join(random.choice(charset) for _ in range(length))
