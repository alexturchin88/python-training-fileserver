import os
from utils.logger import logger


def create_file(filename: str) -> bool:
    """
    Create a file by provided name
    :param filename: string representation of a filename
    :returns boolean
    """
    try:
        with open(filename, 'w') as f:
            f.write('foo')
            logger.info(f"Successfully created a file {filename}")
            return True
    except OSError:
        logger.error("Failed to create a file")
        return False


def delete_file(filename: str) -> bool:
    """
    Delete a file by provided filename
    :param filename: string representation of a filename
    :returns boolean
    """
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


def read_file(filename: str) -> str:
    """
    Read a file by provided filename
    :param filename: string representation of a filename
    :returns text file content
    """
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Failed to read a file {filename} as it doesn't exist")
        return ''
    except OSError:
        logger.error(f"Failed to read a file {filename}")
        return ''


def get_file_metadata(filename: str) -> dict:
    """
    Get a map with metadata details of a file by provided filename
    :param filename: string representation of a filename
    :returns dictionary
    """
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


def print_metadata(filename: str) -> str:
    """
    Get a human-readable batch of metadata details of a file by its provided name
    :param filename: string representation of a filename
    :returns string
    """
    metadata = get_file_metadata(filename)
    if not metadata:
        return f"No metadata found for file '{filename}'"
    output = f"Metadata of a file '{filename}':\n"
    for k, v in metadata.items():
        output += f"{k}: '{v}'\n"
    return output

