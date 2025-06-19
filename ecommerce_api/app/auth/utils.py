from datetime import datetime, timedelta , timezone
from passlib.context import CryptContext 
from jose import jwt
from app.core.config import settings
import uuid

# Set up password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The user's plain-text password.

    Returns:
        str: The securely hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    """
    Verifies a plain-text password against a hashed one.

    Args:
        plain_pw (str): The user's input password.
        hashed_pw (str): The stored hashed password.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return pwd_context.verify(plain_pw, hashed_pw)


def create_token(data: dict, expires_delta: timedelta, secret_key: str) -> str:
    """
    Creates a JWT token with expiration time.

    Args:
        data (dict): Data to encode inside the token.
        expires_delta (timedelta): Token validity duration.
        secret_key (str): Secret key used for signing.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")


def create_access_token(data: dict) -> str:
    """
    Generates a short-lived access token using configured expiry.

    Args:
        data (dict): Data to encode (e.g., user ID and role).

    Returns:
        str: Encoded JWT access token.
    """
    return create_token(
        data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.SECRET_KEY
    )


def create_refresh_token(data: dict) -> str:
    """
    Generates a long-lived refresh token.

    Args:
        data (dict): Data to encode (e.g., user ID and role).

    Returns:
        str: Encoded JWT refresh token valid for 7 days.
    """
    return create_token(
        data,
        expires_delta=timedelta(days=7),
        secret_key=settings.SECRET_KEY 
    )


def generate_reset_token() -> str:
    """
    Generates a unique token for password reset requests.

    Returns:
        str: A UUID4 string used as a reset token.
    """
    return str(uuid.uuid4())
