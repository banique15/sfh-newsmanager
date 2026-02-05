"""Application settings loaded from environment variables."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load environment variables into os.environ for libraries that read them directly (e.g. litellm)
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Newsletter Manager"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str
    db_pool_min: int = 2
    db_pool_max: int = 10

    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_bucket: str = "uploads"

    # LLM Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None

    # Default LLM
    default_llm: str = "openai"
    default_model: str = "gpt-4"

    # Slack
    slack_bot_token: str | None = None
    slack_app_token: str | None = None
    slack_signing_secret: str | None = None

    # Email
    email_host: str | None = None
    email_port: int = 587
    email_username: str | None = None
    email_password: str | None = None
    email_from: str = "newsletter@singforhope.org"

    # Agent Configuration
    agent_name: str = "Newsletter Manager"
    confirmation_required: bool = True
    confirmation_timeout: int = 300  # 5 minutes

    # Content Generation
    content_default_tone: str = "inspiring"
    content_default_length: str = "medium"
    content_max_tokens: int = 2000

    # Image Generation
    image_default_style: str = "vibrant"
    image_default_size: str = "1792x1024"

    # Rate Limits
    content_gen_rate_limit: int = 10  # per minute
    image_gen_rate_limit: int = 5  # per minute
    max_bulk_size: int = 50

    # Redis (for memory/cache)
    redis_url: str = "redis://localhost:6379/0"

    # Logging
    log_level: str = "INFO"


# Global settings instance
settings = Settings()
