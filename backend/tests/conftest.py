"""Fixtures communes : base SQLite, tables et client FastAPI."""

from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-minimum-32bytes!")
os.environ.setdefault("ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite:///./pytest_unit.db")

from app.db.session import Base, SessionLocal, engine  # noqa: E402
from app.main import application  # noqa: E402
from app.models.vehicle import MoteurEnum, Vehicle  # noqa: E402


@pytest.fixture(autouse=True)
def reset_db() -> None:
    """Réinitialise le schéma entre chaque test pour des données isolées."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> TestClient:
    """Client HTTP avec lifespan (création des tables si besoin)."""
    with TestClient(application) as c:
        yield c


@pytest.fixture
def db() -> Session:
    """Session SQLAlchemy directe pour préparer des données."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_vehicle(db: Session, **kwargs: object) -> Vehicle:
    """Crée un véhicule catalogue minimal."""
    defaults: dict = {
        "make": "Peugeot",
        "model": "208",
        "year": 2023,
        "km": 10000,
        "moteur": MoteurEnum.essence,
        "prix": 18990.0,
        "lld": False,
        "mensualite": None,
        "img": "https://example.com/v.jpg",
        "spec_carburant": "Essence",
        "spec_boite": "Manuelle",
        "spec_couleur": "Gris",
        "spec_places": 5,
        "spec_puissance": "100 ch",
        "visible_catalogue": True,
        "archived": False,
    }
    defaults.update(kwargs)
    v = Vehicle(**defaults)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v
