import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application configuration settings loaded from environment variables.

    Attributes:
        SECRET_KEY (str): Secret key used for signing JWTs and tokens.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Duration in minutes before access tokens expire.
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Global settings instance for import across the project
settings = Settings()
