import pytest
from backend.app import create_app
from backend.database import db

@pytest.fixture
def app():
    # Use an in-memory database for testing
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield
