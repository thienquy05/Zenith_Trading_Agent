import pytest
from cryptography.fernet import Fernet

from app import security


def test_hash_password_roundtrip():
    hashed = security.hash_password("correct horse battery staple")
    assert hashed != "correct horse battery staple"
    assert security.verify_password("correct horse battery staple", hashed)


def test_verify_password_rejects_wrong_password():
    hashed = security.hash_password("correct horse battery staple")
    assert not security.verify_password("wrong password", hashed)


def test_encrypt_decrypt_roundtrip(monkeypatch, clear_settings_cache):
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode())

    ciphertext = security.encrypt_secret("sk-live-my-api-key")
    assert b"sk-live-my-api-key" not in ciphertext
    assert security.decrypt_secret(ciphertext) == "sk-live-my-api-key"


def test_decrypt_rejects_tampered_ciphertext(monkeypatch, clear_settings_cache):
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode())

    ciphertext = security.encrypt_secret("sk-live-my-api-key")
    tampered = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])

    with pytest.raises(Exception):
        security.decrypt_secret(tampered)


def test_encrypt_secret_requires_key(monkeypatch, clear_settings_cache):
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", "")

    with pytest.raises(RuntimeError):
        security.encrypt_secret("sk-live-my-api-key")
