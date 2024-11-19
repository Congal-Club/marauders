import json
import pytest
from werkzeug.security import generate_password_hash

from src.database import db
from src.models import User
from src.server import create_app

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  app.config['SECRET_KEY'] = 'test_secret_key'

  with app.app_context():
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

def test_signup_valid(client):
  """Test for a successful signup."""
  response = client.post('/auth/sign-up', json={
    "name": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123",
    "image": "http://example.com/image.jpg"
  })

  assert response.status_code == 201
  data = response.get_json()
  assert data['name'] == "John"
  assert data['email'] == "john.doe@example.com"

def test_signup_missing_fields(client):
  """Test signup with missing required fields."""
  response = client.post('/auth/sign-up', json={
    "name": "John",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "Email and password are required"

def test_signup_invalid_email(client):
  """Test signup with an invalid email format."""
  response = client.post('/auth/sign-up', json={
    "name": "John",
    "lastName": "Doe",
    "email": "invalid-email",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "Invalid email format"

def test_signup_weak_password(client):
  """Test signup with a weak password."""
  response = client.post('/auth/sign-up', json={
    "name": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "123"
  })

  assert response.status_code == 400
  assert "Password must be at least 8 characters" in response.get_json()['error']

def test_signup_duplicate_email(client):
  """Test signup with an email already registered."""
  client.post('/auth/sign-up', json={
    "name": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  })

  response = client.post('/auth/sign-up', json={
    "name": "Jane",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "User already exists"

def test_signin_valid(client):
  """Test successful sign in."""
  hashed_password = generate_password_hash("SecurePass123", method='pbkdf2:sha256')
  user = User(name="John", lastName="Doe", email="john.doe@example.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  response = client.post('/auth/sign-in', json={
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 200
  assert "token" in response.get_json()

def test_signin_invalid_email(client):
  """Test sign in with an unregistered email."""
  response = client.post('/auth/sign-in', json={
    "email": "unknown@example.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 401
  assert response.get_json()['error'] == "Invalid email or password"

def test_signin_invalid_password(client):
  """Test sign in with an incorrect password."""
  hashed_password = generate_password_hash("SecurePass123", method='pbkdf2:sha256')
  user = User(name="John", lastName="Doe", email="john.doe@example.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  response = client.post('/auth/sign-in', json={
    "email": "john.doe@example.com",
    "password": "WrongPass456"
  })

  assert response.status_code == 401
  assert response.get_json()['error'] == "Invalid email or password"

def test_change_password_valid(client):
  """Test successful password change."""
  hashed_password = generate_password_hash("OldPass123", method='pbkdf2:sha256')
  user = User(name="John", lastName="Doe", email="john.doe@example.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  # Authenticate the user (mock token)
  client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer mocktoken'

  response = client.put('/auth/change-password', json={
    "old_password": "OldPass123",
    "new_password": "NewPass456"
  })

  assert response.status_code == 200
  assert response.get_json()['message'] == "Password updated successfully"

def test_change_password_invalid_old_password(client):
  """Test password change with an incorrect current password."""
  hashed_password = generate_password_hash("OldPass123", method='pbkdf2:sha256')
  user = User(name="John", lastName="Doe", email="john.doe@example.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  # Authenticate the user (mock token)
  client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer mocktoken'

  response = client.put('/auth/change-password', json={
    "old_password": "WrongPass123",
    "new_password": "NewPass456"
  })
  
  assert response.status_code == 400
  assert response.get_json()['error'] == "Invalid user or password"
