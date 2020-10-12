import firebase_admin
import pytest
from firebase_admin import auth, credentials, firestore
from pydantic import BaseSettings


@pytest.fixture
def settings():
    class Settings(BaseSettings):
        GOOGLE_APPLICATION_CREDENTIALS: str

        class Config:
            env_file = ".test.env"

    return Settings()


@pytest.fixture
def db(settings):
    cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(cred)
    return firestore.client()
