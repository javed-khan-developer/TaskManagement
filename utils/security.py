from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def _normalize_password(password: str) -> str:
    if password is None:
        return ""

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    return password_bytes.decode("utf-8", errors="ignore")


def hash_password(password: str):
    normalized_password = _normalize_password(password)
    return pwd_context.hash(normalized_password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    normalized_password = _normalize_password(plain_password)
    return pwd_context.verify(
        normalized_password,
        hashed_password
    )