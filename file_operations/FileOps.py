import os
from utils.logger import logger


def create_file(filename):
    try:
        with open(filename, 'w') as f:
            f.write('foo')
            logger.info(f"Successfully created a file {filename}")
            return True
    except OSError:
        logger.error("Failed to create a file")
        return False


def delete_file(filename):
    try:
        os.remove(filename)
        logger.info(f"Deleted file {filename} successfully")
        return True
    except FileNotFoundError:
        logger.error(f"Failed to remove a file {filename} as it doesn't exist")
        return False
    except OSError:
        logger.error(f"Failed to remove a file {filename}")
        return False


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Failed to read a file {filename} as it doesn't exist")
        return ''
    except OSError:
        logger.error(f"Failed to read a file {filename}")
        return ''


def get_file_metadata(filename):
    try:
        file_stat = os.stat(filename)
        metadata = {
            'size_b': file_stat.st_size,
            'created_on': file_stat.st_ctime,
            'modified_on': file_stat.st_mtime,
            'accessed_on': file_stat.st_atime
        }
        return metadata
    except FileNotFoundError:
        logger.error(f"Failed to get metadata of a file {filename} as it doesn't exist")
        return {}
    except OSError:
        logger.error(f"Failed to get metadata of a file {filename}")
        return {}

