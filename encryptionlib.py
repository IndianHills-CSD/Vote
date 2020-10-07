import hashlib, os

# Custom Python module/library for encrypting data


def create_hash(data, salt):
    """
    Encrypts the data
    """
    # Adds the salt (in hex) to the data that was entered
    salt_input = str(data) + str(salt.hex())
    hashed = hashlib.pbkdf2_hmac(
        "sha224", salt_input.encode("ascii"), salt, 10000
    ).hex()
    return hashed


def verify_hash(hashed, data, salt):
    """
    Checks to see if the hash matches the unencrypted data
    """
    # Adds the salt (in hex) to the data that was entered
    salt_input = str(data) + str(salt.hex())
    new_hash = hashlib.pbkdf2_hmac(
        "sha224", salt_input.encode("ascii"), salt, 10000
    ).hex()
    return hashed == new_hash