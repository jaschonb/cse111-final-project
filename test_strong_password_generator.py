from strong_password_generator import *
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import os
import tempfile
import pytest


def test_generate_password():
    # Define the test parameters and expected results
    length = 10
    characters = {
        "lwr": list(ascii_lowercase),
        "upr": list(ascii_uppercase),
        "num": list(digits),
        "sym": list(punctuation)
    }
    
    # Generate a password
    password = generate_password(length, characters)

    # Assertions
    assert len(password) == length
    assert any(char in ascii_lowercase for char in password)
    assert any(char in ascii_uppercase for char in password)
    assert any(char in digits for char in password)
    assert any(char in punctuation for char in password)


@pytest.fixture
def temp_file(tmpdir):
    # Create a temporary file
    temp_file = tmpdir.join("temp_file.txt")
    yield temp_file
    # Remove the temporary file after the test finishes
    temp_file.remove()


def test_save_password_to_file(temp_file):
    # Call the function to save the password to the temporary file
    website = "example.com"
    username = "user123"
    password = "password123"
    save_password_to_file(website, username, password, temp_file)

    # Check if the file exists
    assert os.path.isfile(temp_file)

    # Read the content of the file
    with open(temp_file, "r") as file:
        content = file.read()

    # Assert that the file contains the expected information
    expected_content = f"Website: {website}\nUsername: {username}\nPassword: {password}\n\n"
    assert content == expected_content


def test_make_character_dict():
    # Call the function to get the dictionary of characters
    character_dict = make_character_dict()

    # Assert that the returned value is a dictionary
    assert isinstance(character_dict, dict)

    # Assert that the dictionary contains the expeced keys and values
    expected_dict = {
        "lwr": list(ascii_lowercase),
        "upr": list(ascii_uppercase),
        "num": list(digits),
        "sym": list(punctuation)
    }
    assert character_dict == expected_dict


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])