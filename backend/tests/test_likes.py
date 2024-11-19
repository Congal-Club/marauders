import pytest
from src.server import create_app
from src.database import db
from src.models import User, Post, Like

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  
  with app.app_context():
    db.create_all()
    # Crear usuarios y posts de prueba
    user = User(name="John Doe", email="john@example.com")
    post = Post(title="Test Post", content="This is a test post.")
    db.session.add_all([user, post])
    db.session.commit()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

def test_like_post(client, monkeypatch):
  def mock_auth():
    return 1  # Usuario autenticado con ID 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  
  response = client.post('/likes/1')  # Dar like al post con ID 1
  assert response.status_code == 201
  data = response.get_json()
  assert data['user_id'] == 1
  assert data['post_id'] == 1

def test_like_post_unauthorized(client):
  response = client.post('/likes/1')  # Sin autenticación
  assert response.status_code == 401
  assert response.get_json()['error'] == "Unauthorized"

def test_unlike_post(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  # Dar like primero
  client.post('/likes/1')
  # Ahora quitar el like
  response = client.delete('/likes/1')
  assert response.status_code == 200
  data = response.get_json()
  assert data['user_id'] == 1
  assert data['post_id'] == 1

def test_unlike_post_not_found(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  response = client.delete('/likes/1')  # Intentar quitar un like inexistente
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to unlike post"

def test_get_all_likes(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  # Dar like al post
  client.post('/likes/1')

  response = client.get('/likes/1')  # Obtener todos los likes del post con ID 1
  assert response.status_code == 200
  data = response.get_json()
  assert len(data) == 1
  assert data[0]['user_id'] == 1
  assert data[0]['post_id'] == 1
