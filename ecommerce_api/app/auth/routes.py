import logging
from datetime import datetime, timedelta , timezone

from app.core.database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.auth import models, utils
from app.auth.schemas import (
    UserCreate,
    UserOut,
    UserSignin,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshTokenRequest
)
from app.auth.utils import (
    verify_password,
    create_access_token,
    create_refresh_token
)

from app.auth.models import PasswordResetToken
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


logger = logging.getLogger(__name__)


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user with hashed password and role.

    Args:
        user (UserCreate): Incoming user data.
        db (Session): SQLAlchemy database session.

    Returns:
        UserOut: The created user record.

    Raises:
        HTTPException: If email already exists.
    """
    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"New user registered: {new_user.email} ({new_user.role})")
        return new_user
    except IntegrityError:
        db.rollback()
        logger.warning(f"Signup failed: Email already exists - {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/signin", response_model=TokenResponse)
def signin(credentials: UserSignin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns access + refresh tokens.

    Args:
        credentials (UserSignin): Email and password.
        db (Session): Database session.

    Returns:
        TokenResponse: JWT access and refresh tokens.

    Raises:
        HTTPException: Invalid credentials.
    """
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Failed login attempt for {credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"User signed in: {user.email}")
    payload = {"sub": str(user.id), "role": user.role}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Generates a password reset token for the given email.

    Args:
        req (ForgotPasswordRequest): Email to reset password for.
        db (Session): Database session.

    Returns:
        dict: Reset token message and token (for testing).
    """
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        logger.warning(f"Password reset requested for unknown email: {req.email}")
        raise HTTPException(status_code=404, detail="User not found")

    token = utils.generate_reset_token()
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)

    reset_entry = PasswordResetToken(
        user_id=user.id,
        token=token,
        expiration_time=expiry,
        used=False
    )
    db.add(reset_entry)
    db.commit()

    logger.info(f"Password reset token generated for {user.email}")
    return {"message": "Reset token generated", "reset_token": token}


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Resets a user's password using a valid reset token.

    Args:
        req (ResetPasswordRequest): Token and new password.
        db (Session): Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: Invalid/expired token or user not found.
    """
    token_entry = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == req.token,
        PasswordResetToken.used == False,
        PasswordResetToken.expiration_time > datetime.now(timezone.utc) 
    ).first()

    if not token_entry:
        logger.warning("Invalid or expired reset token used.")
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == token_entry.user_id).first()
    if not user:
        logger.error("User not found during password reset.")
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = utils.hash_password(req.new_password)
    token_entry.used = True
    db.commit()

    logger.info(f"Password reset successful for user ID {user.id}")
    return {"message": "Password has been reset successfully"}


@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    """
    Refreshes the user's access token using a valid refresh token.

    Args:
        request (RefreshTokenRequest): The refresh token.

    Returns:
        dict: New access token and token type.

    Raises:
        HTTPException: Invalid or tampered refresh token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")

        if user_id is None or role is None:
            logger.warning("Malformed refresh token payload.")
            raise credentials_exception

    except JWTError as e:
        logger.warning(f"JWT decode failed in refresh: {str(e)}")
        raise credentials_exception

    logger.info(f"Issued new access token for user ID {user_id}")
    new_access_token = create_access_token(data={"sub": user_id, "role": role})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
