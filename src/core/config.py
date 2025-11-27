"""
Configuración de la aplicación usando pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ecommerce"
    
    # Application
    app_name: str = "E-commerce Core"
    debug: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Singleton de configuración
settings = Settings()
