"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.utils.auth import hash_password

# Test database URL (use SQLite for testing)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Create a test client with test database
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """
    Create a test user
    """
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        full_name="Test User",
        phone="1234567890",
        role=UserRole.STUDENT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin(db):
    """
    Create a test admin user
    """
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        full_name="Admin User",
        phone="0987654321",
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def test_instructor(db):
    """
    Create a test instructor user
    """
    instructor = User(
        email="instructor@example.com",
        password_hash=hash_password("instructor123"),
        full_name="Instructor User",
        phone="1112223333",
        role=UserRole.INSTRUCTOR
    )
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor


@pytest.fixture
def auth_headers(client, test_user):
    """
    Get authentication headers for test user
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, test_admin):
    """
    Get authentication headers for admin user
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def instructor_headers(client, test_instructor):
    """
    Get authentication headers for instructor user
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "instructor@example.com",
            "password": "instructor123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
