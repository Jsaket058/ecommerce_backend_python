import re
from enum import Enum
from pydantic import BaseModel, EmailStr, constr, field_validator

# Password must include: 1 uppercase, 1 lowercase, 1 digit, 1 special char, min 6 characters
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$"
)


class Role(str, Enum):
    """
    Enum for defining user roles.
    
    Attributes:
        admin (str): Admin role.
        user (str): Normal user role.
    """
    admin = "admin"
    user = "user"


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Fields:
        name (str): Full name of the user.
        email (EmailStr): Valid email address.
        password (str): Password (must pass complexity regex).
        role (Role): User role (admin or user).
    """
    name: str
    email: EmailStr
    password: constr(min_length=6) 
    role: Role

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_REGEX.match(value):
            raise ValueError(
                "Password must be at least 6 characters long and include "
                "one uppercase letter, one lowercase letter, one number, and one special character."
            )
        return value


class UserOut(BaseModel):
    """
    Schema for returning user data in responses.

    Fields:
        id (int): User ID.
        name (str): Full name.
        email (EmailStr): Email address.
        role (Role): User's assigned role.
    """
    id: int
    name: str
    email: EmailStr
    role: Role

    model_config = {
        "from_attributes": True
    }


class UserSignin(BaseModel):
    """
    Schema for user login requests.

    Fields:
        email (EmailStr): Registered user email.
        password (str): Plaintext password.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Schema for the token response after successful login.

    Fields:
        access_token (str): Short-lived access token.
        refresh_token (str): Long-lived refresh token.
        token_type (str): Usually 'bearer'.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    """
    Schema for requesting a password reset.

    Fields:
        email (EmailStr): Registered email to reset password for.
    """
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """
    Schema for performing password reset.

    Fields:
        token (str): Reset token received via email.
        new_password (str): New password (must pass regex validation).
    """
    token: str
    new_password: constr(min_length=6)

    @field_validator("new_password")
    def validate_new_password(cls, value: str) -> str:
        if not PASSWORD_REGEX.match(value):
            raise ValueError(
                "New password must be at least 6 characters long and include "
                "one uppercase letter, one lowercase letter, one number, and one special character."
            )
        return value


class RefreshTokenRequest(BaseModel):
    """
    Schema for requesting a new access token using a refresh token.

    Fields:
        refresh_token (str): Valid refresh token.
    """
    refresh_token: str
