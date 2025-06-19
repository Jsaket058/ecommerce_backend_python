from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    """
    Enum defining roles for system users.
    
    Attributes:
        admin (str): Admin role with elevated privileges.
        user (str): Regular user role with restricted access.
    """
    admin = "admin"
    user = "user"


class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    
    Attributes:
        id (int): Primary key, unique user ID.
        name (str): Full name of the user.
        email (str): Unique email address used for login.
        hashed_password (str): Securely hashed user password.
        role (UserRole): Role assigned to the user (admin or user).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)


class PasswordResetToken(Base):
    """
    SQLAlchemy model for tracking password reset tokens.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key referencing the user who requested a reset.
        token (str): Unique token string sent to user's email.
        expiration_time (datetime): Token expiration datetime.
        used (bool): Whether the token has already been used.
        user (User): Relationship to the User model.
    """
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, nullable=False)
    expiration_time = Column(DateTime)
    used = Column(Boolean, default=False)

    user = relationship("User")
