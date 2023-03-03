import os
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from utils.logger import logger


class FileService:
    """Class to work with files - create/read/delete/get metadata"""

    def __init__(self):
        self.logger = logger

    def create_file(self, filename: str, content: str = '') -> bool:
        """
        Create a file by provided name
        :param filename: string representation of a filename
        :param content: string content of a future file
        :returns boolean
        """
        try:
            with open(filename, 'w') as f:
                if not content:
                    f.write('foo')
                else:
                    f.write(content)
                self.logger.info(f"Successfully created a file {filename}")
                return True
        except OSError as e:
            self.logger.error(f"Failed to create a file:\n{e.strerror}")
            return False

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file by provided filename
        :param filename: string representation of a filename
        :returns boolean
        """
        try:
            os.remove(filename)
            self.logger.info(f"Deleted file {filename} successfully")
            return True
        except FileNotFoundError:
            self.logger.error(f"Failed to remove a file {filename} as it doesn't exist")
            return False
        except OSError:
            self.logger.error(f"Failed to remove a file {filename}")
            return False

    def read_file(self, filename: str) -> str:
        """
        Read a file by provided filename
        :param filename: string representation of a filename
        :returns text file content
        """
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Failed to read a file {filename} as it doesn't exist")
            return ''
        except OSError:
            self.logger.error(f"Failed to read a file {filename}")
            return ''
        except UnicodeDecodeError:
            self.logger.error(f"Failed to read an encrypted file {filename}")

    def get_file_metadata(self, filename: str) -> dict:
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
            self.logger.error(f"Failed to get metadata of a file {filename} as it doesn't exist")
            return {}
        except OSError:
            self.logger.error(f"Failed to get metadata of a file {filename}")
            return {}

    def print_metadata(self, filename: str, date_format: str) -> str:
        """
        Get a human-readable batch of metadata details of a file by its provided name
        :param filename: string representation of a filename
        :param date_format: format of the date to be displayed
        :returns string
        """
        metadata = self.get_file_metadata(filename)
        if not metadata:
            return f"No metadata found for file '{filename}'"
        output = f"Metadata of a file '{filename}':\n"
        for k, v in metadata.items():
            value = datetime.fromtimestamp(v).strftime(date_format) if '.' in str(v) else v
            output += f"{k}: '{value}'\n"
        return output


class FileServiceEncrypted(FileService):
    """Class to work with files using cryptography"""

    def __init__(self):
        super().__init__()
        self.private_key = None
        self.public_key = None
        self.generate_keys_pair()
        self.store_public_key()

    def generate_keys_pair(self):
        """Generate a pair of public and private keys"""
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def store_public_key(self):
        """Save a public key into a file"""
        with open('public_key.pem', 'wb') as file:
            file.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def create_file(self, filename: str, content: str = '') -> bool:
        """
        Create an encrypted file by provided name
        :param filename: string representation of a filename
        :param content: string content of a future file
        :returns boolean
        """
        if not super().create_file(filename, content):
            return False
        with open(filename, 'rb') as file:
            original = file.read()
        try:
            encrypted = self.public_key.encrypt(
                original,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            with open(filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            return True
        except Exception as exc:
            self.logger.error(f"Failed to create an encrypted file:\n {exc}")
            return False

    def read_file(self, filename: str) -> str:
        """
        Read an encrypted file by provided filename
        :param filename: string representation of a filename
        :returns text file content
        """
        with open(filename, 'rb') as file:
            encrypted = file.read()
        if not encrypted:
            self.logger.error(f"Failed to get encrypted file data")
            return ''
        try:
            decrypted = self.private_key.decrypt(
                encrypted,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted
        except Exception as exc:
            self.logger.error(f"Failed to decrypt a file {filename}:\n{exc}")
            return ''

