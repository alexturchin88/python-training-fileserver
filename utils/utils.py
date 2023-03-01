import random
import yaml
from .logger import logger
from vars import config_file


def generate_file_name(charset: str) -> str:
    """
    Generate a random filename
    :param charset: string of characters to be used for generation
    :returns string filename
    """
    length = random.randint(5, 10)
    return ''.join(random.choice(charset) for _ in range(length))


def read_config():
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.critical(f"Failed to read config file '{config_file}'")
        raise e
