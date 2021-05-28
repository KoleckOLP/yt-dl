import secrets
from cryptography import fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

backend = default_backend()
iterations = 100_000


def _derive_key(password: bytes, salt: bytes, itera: int = iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=itera, backend=backend)
    return b64e(kdf.derive(password))


def _encrypt(message: bytes, password: str, itera: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, itera)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(fernet.Fernet(key).encrypt(message)),
        )
    )


def _decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, itera, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterat = int.from_bytes(itera, 'big')
    key = _derive_key(password.encode(), salt, iterat)
    return fernet.Fernet(key).decrypt(token)


def encrypt(data: str, pin: str) -> bytes:
    output = _encrypt(data.encode(), pin)
    return output


def decrypt(data: bytes, pin: str) -> str:
    try:  # this tests if pin correct
        output = _decrypt(data, pin).decode()  # this decrypts the
    except fernet.InvalidToken:  # executed if pin wrong
        output = "wrong pin"
    return output
