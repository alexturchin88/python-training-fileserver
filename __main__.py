import argparse
import string
from file_operations.FileOps import read_file, create_file, get_file_metadata, delete_file
from utils.Utils import generate_file_name
from utils.logger import logger

parser = argparse.ArgumentParser(description='Input parameters')
parser.add_argument('port', type=str, help='Port number')
parser.add_argument('workdir', type=str, help='Working directory with files')
charset = string.ascii_letters + string.digits


def main():
    args = parser.parse_args()
    port = args.port
    workdir = args.workdir
    logger.info(f"Starting service on port {port}, working in directory '{workdir}'")

    test_file = generate_file_name(charset)

    create_file(test_file)
    logger.info(read_file(test_file))
    for k, v in get_file_metadata(test_file).items():
        logger.info(f"{k}: '{v}'")
    delete_file(test_file)


if __name__ == '__main__':
    main()
