import argparse
import string
from file_operations.FileOps import read_file, create_file, get_file_metadata, delete_file
from utils.Utils import generate_file_name


# parser = argparse.ArgumentParser(description='Input parameters')
# parser.add_argument('port', type=str, help='Port number')
# parser.add_argument('workdir', type=str, help='Working directory with files')


def main():
    # args = parser.parse_args()

    charset = string.ascii_letters + string.digits

    test_file = generate_file_name(charset)

    create_file(test_file)
    print(read_file(test_file))
    for k, v in get_file_metadata(test_file).items():
        print(f"{k}: '{v}'")
    delete_file(test_file)


if __name__ == '__main__':
    main()
