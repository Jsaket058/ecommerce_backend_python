import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_db

# Set up module-level logger
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Extracts and validates the current user from a JWT token.

    Args:
        token (str): The JWT access token extracted from the request.
        db (Session): The database session for querying the user.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If token is invalid or user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token missing 'sub' claim.")
            raise credentials_exception
    except JWTError as e:
        logger.warning(f"JWT decoding failed: {str(e)}")
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        logger.warning(f"User not found for token subject: {user_id}")
        raise credentials_exception
    return user


def get_current_admin_user(user: User = Depends(get_current_user)) -> User:
    """
    Verifies that the authenticated user has admin privileges.

    Args:
        user (User): The currently authenticated user.

    Returns:
        User: The user object if admin.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if user.role != "admin":
        logger.warning(f"Access denied for user {user.email} — requires admin role.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user


def get_current_normal_user(user: User = Depends(get_current_user)) -> User:
    """
    Verifies that the authenticated user has a normal (non-admin) role.

    Args:
        user (User): The currently authenticated user.

    Returns:
        User: The user object if role is 'user'.

    Raises:
        HTTPException: If the user is not a normal user.
    """
    if user.role != "user":
        logger.warning(f"Access denied for user {user.email} — requires user role.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User privileges required",
        )
    return user
