from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SmartLiftRentals")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "IoT platform for monitoring and managing construction lift rentals.",
    )
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "smartliftrentals")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "smartlift")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "smartlift")

    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "backend")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "backend123")
    MQTT_TOPIC: str = os.getenv("MQTT_TOPIC", "lifts/+/telemetry")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-dev")
    CORS_ORIGINS_RAW: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )

    @property
    def DATABASE_URL(self) -> str:
        return os.getenv(
            "DATABASE_URL",
            (
                f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            ),
        )

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS_RAW.split(",") if origin.strip()]


settings = Settings()
