import os
import pytest
import string
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from file_operations.file_ops import FileService, FileServiceEncrypted
from utils.utils import generate_file_name


charset = string.ascii_letters + string.digits
file_ops_simple = FileService()
file_ops_crypto = FileServiceEncrypted()


@pytest.fixture
def temp_file():
    """Fixture that creates a temporary file and returns its name"""
    f_name = generate_file_name(charset)
    yield f_name
    os.remove(f_name)


def test_create_file(temp_file):
    """Test that create_file() creates a file with the correct content"""
    content = 'test'
    assert file_ops_simple.create_file(temp_file, content)
    with open(temp_file, 'r') as f:
        assert f.read() == content


def test_delete_file():
    """Test that delete_file() deletes a file"""
    f_name = generate_file_name(charset)
    assert file_ops_simple.create_file(f_name)
    assert file_ops_simple.delete_file(f_name)
    assert not os.path.exists(f_name)


def test_read_file(temp_file):
    """Test that read_file() reads the content of a file"""
    assert file_ops_simple.create_file(temp_file)
    assert file_ops_simple.read_file(temp_file) == 'foo'


def test_get_file_metadata(temp_file):
    """Test that get_file_metadata() returns the correct metadata"""
    assert file_ops_simple.create_file(temp_file)
    metadata = file_ops_simple.get_file_metadata(temp_file)
    assert metadata['size_b'] == 3
    assert metadata['created_on'] <= metadata['modified_on']
    assert metadata['modified_on'] <= metadata['accessed_on']


def test_create_file_crypto():
    filename = 'test_file.txt'
    content = 'this is a test file'
    assert file_ops_crypto.create_file(filename, content)
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    assert content.encode() != encrypted_data


def test_read_file_crypto():
    filename = 'test_file.txt'
    content = 'this is a test file'
    with open(filename, 'wb') as f:
        encrypted_data = file_ops_crypto.public_key.encrypt(
            content.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        f.write(encrypted_data)
    assert file_ops_crypto.read_file(filename) == content.encode()

