import pytest
from werkzeug.security import generate_password_hash

from src.server import create_app
from src.database import db
from src.models import User


@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  
  with app.app_context():
    db.create_all()
    
    user1 = User(
      name="Cesar",
      lastName="Villalobos Olmos",
      email="cesarvillalobosolmos.01@gmail.com",
      password=generate_password_hash("Password123", method="pbkdf2:sha256"),
      image="http://example.com/image.jpg"
    )
    user2 = User(
      name="Araza",
      lastName="Messa Sanchez",
      email="aranzazu.messa@gmail.com",
      password=generate_password_hash("Password123", method="pbkdf2:sha256"),
      image="http://example.com/image.jpg"
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    yield app.test_client()
    
    db.session.remove()
    db.drop_all()


def test_follow_user(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  
  response = client.post('/api/follows/2')
  assert response.status_code == 201
  data = response.get_json()
  assert data['user_following'] == 1
  assert data['user_followed'] == 2


def test_follow_user_unauthorized(client):
  response = client.post('/api/follows/2')
  assert response.status_code == 401
  assert response.get_json()['error'] == "Unauthorized"


def test_unfollow_user(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  
  client.post('/api/follows/2')
  response = client.delete('/api/follows/2')

  assert response.status_code == 200
  data = response.get_json()
  assert data['user_following'] == 1
  assert data['user_followed'] == 2


def test_unfollow_user_not_found(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  response = client.delete('/api/follows/2')
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to unfollow user"


def test_get_followers(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)

  client.post('/api/follows/2')
  response = client.get('/api/follows/followers/2')

  assert response.status_code == 200
  data = response.get_json()
  assert len(data) == 1
  assert data[0]['user_following'] == 1
  assert data[0]['user_followed'] == 2


def test_get_following(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)

  client.post('/api/follows/2')
  response = client.get('/api/follows/following/1')
  
  assert response.status_code == 200
  data = response.get_json()
  assert len(data) == 1
  assert data[0]['user_following'] == 1
  assert data[0]['user_followed'] == 2
