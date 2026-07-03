import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

_ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode()

if not _ENCRYPTION_KEY:
    raise ValueError(
        "ENCRYPTION_KEY no configurada en .env. "
        "Genera una con: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
    )

_fernet = Fernet(_ENCRYPTION_KEY)


def encrypt(value: str) -> str:
    if not value:
        return ""
    return _fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    if not value:
        return ""
    try:
        return _fernet.decrypt(value.encode()).decode()
    except Exception:
        return ""