from dataclasses import dataclass
from typing import List, Literal, LiteralString

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict



LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]



class Settings(BaseSettings):
    # logging settings
    log_level : LogLevel = Field(default="INFO")
    # redis settings
    redis_port : int = Field(default=6379)
    redis_host : str = Field(default="localhost")
    redis_max_connections : int = Field(default=10)

    # Database settings
    database_url: PostgresDsn = Field(
        default=PostgresDsn("postgres://postgres:pass123@localhost:5432/split_smart"),
        description="PostgreSQL connection string"
    )
    
    # Security settings
    secret_key: str = Field(default="Aabracadabra", description="Secret key for JWT or session signing")
    access_token_expire_minutes : int = int(Field(default= 15 , description="Maximum validity duration of a given access token"))
    algorithm : str = Field(default="HS256" , description="Hashing Algorithm")
    allowed_hosts: List[str] = Field(default=["localhost"], description="Allowed hostnames")

    # Debug mode
    debug: bool = Field(default=False, description="Enable debug mode")

    # Pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",        # Load from .env file if present
        env_file_encoding="utf-8",
    )


settings = Settings()