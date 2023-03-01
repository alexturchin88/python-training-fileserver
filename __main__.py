import argparse
import string
import yaml
from file_operations.file_ops import read_file, create_file, print_metadata, delete_file
from utils.utils import generate_file_name, read_config
from utils.logger import logger


parser = argparse.ArgumentParser(description='Input parameters')
parser.add_argument('port', type=str, help='Port number')
parser.add_argument('workdir', type=str, help='Working directory with files')
charset = string.ascii_letters + string.digits

config = read_config()
settings = config['settings']
date_format = settings['date_format']


def main():
    args = parser.parse_args()
    port = args.port
    workdir = args.workdir
    logger.info(f"Starting service on port {port}, working in directory '{workdir}'")

    test_file = generate_file_name(charset)

    create_file(test_file)
    logger.info(read_file(test_file))
    logger.info(print_metadata(test_file, date_format))
    delete_file(test_file)


if __name__ == '__main__':
    main()
