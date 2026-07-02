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


def test_verify_password_returns_false_on_malformed_hash():
    # Corrupted or non-hash values in password_hash must fail closed
    # (return False), not crash the login path.
    assert not security.verify_password("anything", "")
    assert not security.verify_password("anything", "not-a-hash")
    assert not security.verify_password("anything", "$argon2id$v=19$truncated")


def test_verify_password_accepts_passlib_era_hash():
    # Frozen hash for "correct horse battery staple" using passlib 1.7.4's
    # argon2 cost parameters (m=102400,t=2,p=8) — verification must honor
    # the parameters embedded in the hash, not today's defaults, so hashes
    # written before the argon2-cffi migration keep working.
    legacy = (
        "$argon2id$v=19$m=102400,t=2,p=8"
        "$TTqinJeUIBao+/P65yMD+g$nsC7TIcv+5I/lT2pHT8dVDujYqlN0GbLrjU/GjM31wc"
    )
    assert security.verify_password("correct horse battery staple", legacy)
    assert not security.verify_password("wrong password", legacy)


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
