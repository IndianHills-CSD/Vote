from hashlib import sha256

# Custom Python module/library for verifying Bitcoins


def decode_base58(bc, length):
    """
    Find the total bytes of a Bitcoin
    """
    n = 0
    digits58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, "big")


def check_bc(bc):
    """
    Verifies a Bitcoin
    """
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False