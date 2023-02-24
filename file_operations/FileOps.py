import os


def create_file(filename):
    try:
        with open(filename, 'w') as f:
            f.write('foo')
            print(f"Successfully created a file {filename}")
    except OSError:
        print("Failed to create a file")


def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted file {filename} successfully")
        return True
    except FileNotFoundError:
        print(f"Failed to remove a file {filename} as it doesn't exist")
        return False
    except OSError:
        print(f"Failed to remove a file {filename}")
        return False


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Failed to read a file {filename} as it doesn't exist")
        return None
    except OSError:
        print(f"Failed to read a file {filename}")
        return None


def get_file_metadata(filename):
    try:
        file_stat = os.stat(filename)
        data_map = {
            'size_b': file_stat.st_size,
            'created_on': file_stat.st_ctime,
            'modified_on': file_stat.st_mtime,
            'accessed_on': file_stat.st_atime
        }
        return data_map
    except FileNotFoundError:
        print(f"Failed to get metadata of a file {filename} as it doesn't exist")
        return None
    except OSError:
        print(f"Failed to get metadata of a file {filename}")
        return None

