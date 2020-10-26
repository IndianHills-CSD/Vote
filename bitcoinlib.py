from hashlib import sha256

# Custom Python module/library for verifying Bitcoins


def check_bc(bc):
    """
    Verifies a Bitcoin address
    """
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


def decode_base58(bc, length):
    """
    Finds the total bytes of a Bitcoin address
    """
    n = 0
    # Contains all of the acceptable characters
    digits58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, "big")