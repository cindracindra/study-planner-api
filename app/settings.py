import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_url: str = os.getenv("SERVER_URL", "/")
    environment: str = os.getenv("ENVIRONMENT", "development")
    testing: bool = bool(os.getenv("TESTING", 0))
    super_users: str = os.getenv("SUPER_USERS", "")

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"
