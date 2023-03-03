import argparse
import os
import string
from configuration.config import Config
from file_operations.file_ops import FileService, FileServiceEncrypted
from utils.utils import generate_file_name
from utils.logger import logger


parser = argparse.ArgumentParser(description='Input parameters')
parser.add_argument('port', type=str, help='Port number')
parser.add_argument('workdir', type=str, help='Working directory with files')
charset = string.ascii_letters + string.digits

config = Config.get_instance()
date_format = config.date_format


def main():
    args = parser.parse_args()
    port = args.port
    workdir = args.workdir
    logger.info(f"Starting service on port {port}, working in directory '{workdir}'")

    create_file_dir(workdir)
    test_file = os.path.join(workdir, generate_file_name(charset))

    file_ops_simple = FileService()
    file_ops_crypto = FileServiceEncrypted()

    file_ops_simple.create_file(test_file, 'test content')
    logger.info(file_ops_simple.read_file(test_file))
    logger.info(file_ops_simple.print_metadata(test_file, date_format))
    file_ops_simple.delete_file(test_file)

    logger.info("=========Encrypted operations:=========")

    file_ops_crypto.create_file(test_file, 'test content')
    logger.info(file_ops_crypto.read_file(test_file))
    logger.info(file_ops_simple.read_file(test_file))  # should fail due to encrypted data
    file_ops_crypto.delete_file(test_file)


def create_file_dir(dirname: str):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


if __name__ == '__main__':
    main()
