# This code is used to obfuscate shellcode
# Usage:
# shellcode_obfuscator.py [your normal shellcode].

import sys

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports
from Crypto.Cipher import AES  # noqa: DUO133  # nosec: B413

# We only encrypt payloads to hide them from static analysis
# it's OK to have these keys plaintext
KEY = b"1234567890123456"
NONCE = b"\x93n2\xbc\xf5\x8d:\xc2fP\xabn\x02\xb3\x17f"


# Use this manually to get obfuscated bytes of shellcode
def obfuscate(shellcode: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=NONCE)
    ciphertext, _ = cipher.encrypt_and_digest(shellcode)
    return ciphertext


def clarify(shellcode: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=NONCE)
    return cipher.decrypt(shellcode)


if __name__ == "__main__":
    print(obfuscate(sys.argv[1].encode()))
