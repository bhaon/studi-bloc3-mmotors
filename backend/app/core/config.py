"""Configuration applicative : secrets et URL issus uniquement des variables d'environnement."""

from __future__ import annotations

import json
from typing import Annotated, Any, List

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_allowed_origins() -> List[str]:
    """Valeurs CORS par défaut (non sensibles) si la configuration est absente ou vide."""
    return [
        "https://localhost:8443",
        "https://127.0.0.1:8443",
    ]


def _strip_nonempty_string_list(items: list[Any]) -> List[str]:
    """Normalise une liste d'origines : chaînes non vides après strip."""
    return [str(x).strip() for x in items if str(x).strip()]


def _try_parse_origins_json_array(s: str) -> List[str] | None:
    """
    Si ``s`` est un tableau JSON valide, renvoie la liste d'origines nettoyées.
    Renvoie ``None`` pour repasser par le parseur CSV (JSON invalide ou type inattendu).
    """
    if not s.startswith("["):
        return None
    try:
        parsed = json.loads(s)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list):
        return None
    return _strip_nonempty_string_list(parsed)


def _parse_allowed_origins(v: Any) -> List[str]:
    """
    Construit la liste CORS depuis une liste Python, du JSON (tableau) ou une chaîne CSV.
    Valeurs par défaut non sensibles si la variable est absente ou vide.
    """
    default = _default_allowed_origins()
    if v is None:
        return default
    if isinstance(v, list):
        out = _strip_nonempty_string_list(v)
        return out or default
    if not isinstance(v, str):
        return default
    s = v.strip()
    if not s:
        return default
    json_origins = _try_parse_origins_json_array(s)
    if json_origins is not None:
        return json_origins or default
    parts = [x.strip() for x in s.split(",") if x.strip()]
    return parts or default


class Settings(BaseSettings):
    """Paramètres chargés depuis l'environnement (fichier `.env` optionnel en local)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "M-Motors API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    DATABASE_URL: str = Field(
        ...,
        description="URL SQLAlchemy synchrone (ex. postgresql://user:pass@host:5432/db).",
    )
    SECRET_KEY: str = Field(
        ...,
        description="Secret pour signer les JWT — obligatoire (variable d'environnement uniquement).",
    )

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    ALLOWED_ORIGINS: Annotated[List[str], BeforeValidator(_parse_allowed_origins)] = Field(
        default_factory=lambda: [
            "https://localhost:8443",
            "https://127.0.0.1:8443",
        ],
    )


# Les champs requis sont fournis par l’environnement ; mypy ne le déduit pas.
settings = Settings()  # type: ignore[call-arg]
