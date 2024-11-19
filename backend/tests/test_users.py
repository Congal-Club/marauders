import pytest
from app import create_app

from src.database import db
from src.models import User

@pytest.fixture
def test_client():
  app = create_app()
  app.config["TESTING"] = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  with app.test_client() as client:
    with app.app_context():
      db.create_all()
      
    yield client

    with app.app_context():
      db.drop_all()

def test_create_user_success(test_client):
  response = test_client.post("/api/users", json={
    "name": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  })

  assert response.status_code == 201
  data = response.get_json()
  assert data["name"] == "John"
  assert data["email"] == "john.doe@example.com"

def test_create_user_missing_fields(test_client):
  response = test_client.post("/api/users", json={"email": "missing@example.com"})
  assert response.status_code == 400
  assert "Missing fields" in response.get_json()["error"]

def test_create_user_invalid_email(test_client):
  response = test_client.post("/api/users", json={
    "name": "John",
    "lastName": "Doe",
    "email": "invalid-email",
    "password": "password123"
  })

  assert response.status_code == 400
  assert "Invalid email format" in response.get_json()["error"]

def test_create_user_duplicate_email(test_client):
  test_client.post("/api/users", json={
    "name": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  })

  response = test_client.post("/api/users", json={
    "name": "Jane",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "password1234"
  })

  assert response.status_code == 400

def test_get_all_users(test_client):
  test_client.post("/api/users", json={"name": "John", "lastName": "Doe", "email": "john.doe@example.com", "password": "password123"})
  response = test_client.get("/api/users")
  assert response.status_code == 200
  assert len(response.get_json()) == 1

def test_delete_user_success(test_client):
  response = test_client.post("/api/users", json={"name": "John", "lastName": "Doe", "email": "john.doe@example.com", "password": "password123"})
  user_id = response.get_json()["id"]
  response = test_client.delete(f"/api/users/{user_id}")
  
  assert response.status_code == 200
  assert "User deleted" in response.get_json()["message"]
