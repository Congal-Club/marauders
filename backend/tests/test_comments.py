import pytest
from werkzeug.security import generate_password_hash

from src.server import create_app
from src.database import db
from src.models import User, Post


@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  
  with app.app_context():
    db.create_all()
    
    user = User(
      name="Cesar",
      lastName="Villalobos Olmos",
      email="cesarvillalobosolmos.01@gmail.com",
      password=generate_password_hash("Password123", method="pbkdf2:sha256"),
      image="http://example.com/image.jpg"
    )
    post = Post(content="Test Content", user_id=1)

    db.session.add(user)
    db.session.add(post)

    db.session.commit()
    
    yield app.test_client()
    
    db.session.remove()
    db.drop_all()


def test_create_comment(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response = client.post(
    '/api/comments/1',
    json={"comment": "This is a test comment."},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 201
  data = response.get_json()
  assert data['comment'] == "This is a test comment."
  assert data['post_id'] == 1


def test_create_comment_no_content(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response = client.post('/api/comments/1', json={"comment": ""}, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Comment is required"


def test_create_comment_exceeds_length(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  long_content = "x" * 501
  response = client.post('/api/comments/1', json={"comment": long_content}, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Comment cannot exceed 500 characters"


def test_get_all_comments(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  client.post('/api/comments/1', json={"comment": "First comment"}, headers={"Authorization": f"Bearer {token}"})
  client.post('/api/comments/1', json={"comment": "Second comment"}, headers={"Authorization": f"Bearer {token}"})
  
  response = client.get('/api/comments/1', headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  data = response.get_json()
  assert len(data) == 2
  assert data[0]['comment'] == "First comment"
  assert data[1]['comment'] == "Second comment"


def test_update_comment(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  client.post('/api/comments/1', json={"comment": "Original comment"}, headers={"Authorization": f"Bearer {token}"})
  
  response = client.put('/api/comments/1/1', json={"comment": "Updated comment"}, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  data = response.get_json()
  assert data['comment'] == "Updated comment"


def test_update_comment_not_found(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response = client.put('/api/comments/1/99', json={"comment": "Does not exist"}, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to update comment"


def test_delete_comment(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  client.post('/api/comments/1', json={"comment": "Comment to delete"}, headers={"Authorization": f"Bearer {token}"})
  response = client.delete('/api/comments/1/1', headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  assert response.get_json()['message'] == "Comment deleted"


def test_delete_comment_not_found(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  response = client.delete('/api/comments/1/99', headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to delete comment"
