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
  """Test para un registro exitoso"""

  response = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "SecurePass123",
    "image": "http://example.com/image.jpg"
  })

  assert response.status_code == 201
  data = response.get_json()
  assert data['name'] == "Cesar"
  assert data['email'] == "cesarvillalobosolmos.01@gmail.com"


def test_signup_missing_fields(client):
  """Test para un registro con campos faltantes"""

  response = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "Email and password are required"


def test_signup_invalid_email(client):
  """Test para un registro con un formato de correo electrónico inválido"""

  response = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "invalid-email",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "Invalid email format"


def test_signup_weak_password(client):
  """Test para un registro con una contraseña débil"""

  response = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "123"
  })

  assert response.status_code == 400
  assert "Password must be at least 8 characters" in response.get_json()['error']


def test_signup_duplicate_email(client):
  """Test para un registro con un correo electrónico ya registrado"""

  client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "SecurePass123"
  })

  response = client.post('/api/auth/sign-up', json={
    "name": "Jane",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 400
  assert response.get_json()['error'] == "User already exists"


def test_signin_valid(client):
  """Test para un inicio de sesión exitoso"""

  hashed_password = generate_password_hash("SecurePass123", method='pbkdf2:sha256')
  user = User(name="Cesar", lastName="Villalobos Olmos", email="cesarvillalobosolmos.01@gmail.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  response = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 200
  assert "token" in response.get_json()


def test_signin_invalid_email(client):
  """Test para un inicio de sesión con un correo electrónico no registrado"""

  response = client.post('/api/auth/sign-in', json={
    "email": "unknown@example.com",
    "password": "SecurePass123"
  })

  assert response.status_code == 401
  assert response.get_json()['error'] == "Invalid email or password"


def test_signin_invalid_password(client):
  """Test para un inicio de sesión con una contraseña incorrecta"""

  hashed_password = generate_password_hash("SecurePass123", method='pbkdf2:sha256')
  user = User(name="Cesar", lastName="Villalobos Olmos", email="cesarvillalobosolmos.01@gmail.com", password=hashed_password)
  db.session.add(user)
  db.session.commit()

  response = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "WrongPass456"
  })

  assert response.status_code == 401
  assert response.get_json()['error'] == "Invalid email or password"


def test_change_password_valid(client):
  """Test para un cambio de contraseña exitoso"""
  
  response_signup = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "OldPass123",
    "image": "http://example.com/image.jpg"
  })

  assert response_signup.status_code == 201

  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "OldPass123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response_change_password = client.put(
    '/api/auth/change-password',
    json={
      "old_password": "OldPass123",
      "new_password": "NewPass456"
    },
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response_change_password.status_code == 200
  assert response_change_password.get_json()['message'] == "Password updated successfully"


def test_change_password_invalid_old_password(client):
  """Test para un cambio de contraseña con una contraseña actual incorrecta"""
  
  response_signup = client.post('/api/auth/sign-up', json={
    "name": "Cesar",
    "lastName": "Villalobos Olmos",
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "OldPass123",
    "image": "http://example.com/image.jpg"
  })

  assert response_signup.status_code == 201

  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "OldPass123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response_change_password = client.put(
    '/api/auth/change-password',
    json={
      "old_password": "WrongPass123",
      "new_password": "NewPass456"
    },
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response_change_password.status_code == 400
  assert response_change_password.get_json()['error'] == "Invalid user or password"
