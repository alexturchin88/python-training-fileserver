import os
import pytest
import string
from file_operations.file_ops import create_file, delete_file, read_file, get_file_metadata
from utils.utils import generate_file_name


charset = string.ascii_letters + string.digits


@pytest.fixture
def temp_file():
    """Fixture that creates a temporary file and returns its name"""
    f_name = generate_file_name(charset)
    yield f_name
    os.remove(f_name)


def test_create_file(temp_file):
    """Test that create_file() creates a file with the correct content"""
    content = 'test'
    assert create_file(temp_file, content)
    with open(temp_file, 'r') as f:
        assert f.read() == content


def test_delete_file():
    """Test that delete_file() deletes a file"""
    f_name = generate_file_name(charset)
    assert create_file(f_name)
    assert delete_file(f_name)
    assert not os.path.exists(f_name)


def test_read_file(temp_file):
    """Test that read_file() reads the content of a file"""
    assert create_file(temp_file)
    assert read_file(temp_file) == 'foo'


def test_get_file_metadata(temp_file):
    """Test that get_file_metadata() returns the correct metadata"""
    assert create_file(temp_file)
    metadata = get_file_metadata(temp_file)
    assert metadata['size_b'] == 3
    assert metadata['created_on'] <= metadata['modified_on']
    assert metadata['modified_on'] <= metadata['accessed_on']
