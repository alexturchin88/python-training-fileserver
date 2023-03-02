from configuration.config import Config
import random


def generate_file_name(charset: str) -> str:
    """
    Generate a random filename
    :param charset: string of characters to be used for generation
    :returns string filename
    """
    config = Config.get_instance()
    length = random.randint(config.file_name_len_min, config.file_name_len_max)
    return ''.join(random.choice(charset) for _ in range(length))

