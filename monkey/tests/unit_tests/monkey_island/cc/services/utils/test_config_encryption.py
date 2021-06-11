import pytest
from tests.unit_tests.monkey_island.cc.services.utils.ciphertexts_for_encryption_test import (
    MALFORMED_CIPHER_TEXT_CORRUPTED,
)

from monkey_island.cc.services.utils.encryption import (
    InvalidCredentialsError,
    decrypt_ciphertext,
    encrypt_string,
)

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"
PASSWORD = "hello123"
INCORRECT_PASSWORD = "goodbye321"


def test_encrypt_decrypt_string(monkey_config_json):
    encrypted_config = encrypt_string(monkey_config_json, PASSWORD)
    assert decrypt_ciphertext(encrypted_config, PASSWORD) == monkey_config_json


def test_encrypt_decrypt_string__wrong_password(monkey_config_json):
    encrypted_config = encrypt_string(monkey_config_json, PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        decrypt_ciphertext(encrypted_config, INCORRECT_PASSWORD)


def test_encrypt_decrypt_string__malformed_corrupted():
    with pytest.raises(ValueError):
        decrypt_ciphertext(MALFORMED_CIPHER_TEXT_CORRUPTED, PASSWORD)


def test_encrypt_decrypt_string__decrypt_no_password(monkey_config_json):
    encrypted_config = encrypt_string(monkey_config_json, PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        decrypt_ciphertext(encrypted_config, "")
