from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    # Schema-owning role: used by Alembic migrations (DDL) only.
    postgres_user: str = "trading_app"
    postgres_password: str = "changeme"
    # Least-privilege runtime role (created by migration 0004): DML only,
    # no UPDATE/DELETE on the append-only ledger tables. The backend
    # runtime connects as this role, never as the schema owner.
    postgres_app_user: str = "trading_runtime"
    postgres_app_password: str = "changeme"
    postgres_db: str = "trading"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    # Symmetric key for reversible encryption of api_credentials.encrypted_value.
    # Must be a urlsafe base64-encoded 32-byte key (Fernet.generate_key()).
    credential_encryption_key: str = ""

    backend_port: int = 5000

    @property
    def database_url(self) -> str:
        """Schema-owner connection — migrations and test fixtures (DDL)."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def app_database_url(self) -> str:
        """Runtime connection — the DML-only role the backend runs as."""
        return (
            f"postgresql+psycopg://{self.postgres_app_user}:{self.postgres_app_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
