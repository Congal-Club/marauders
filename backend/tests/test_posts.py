import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from src.database import db
from src.models import Post, User


@pytest.fixture
def client():
  app = create_app()

  with app.test_client() as client:
    with app.app_context():
      db.create_all()

      user = User(
        name="Cesar",
        lastName="Villalobos Olmos",
        email="cesarvillalobosolmos.01@gmail.com",
        password=generate_password_hash("Password123", method="pbkdf2:sha256"),
        image="http://example.com/image.jpg"
      )

      db.session.add(user)
      db.session.commit()

    yield client

    with app.app_context():
      db.session.remove()
      db.drop_all()


def test_create_post(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  data = {
    "content": "This is a test post content."
  }

  response = client.post("/api/posts", json=data, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 201
  
  response_data = response.get_json()
  assert response_data["content"] == "This is a test post content."
  assert response_data["user_id"] == 1


def test_get_all_posts(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']
  
  with client.application.app_context():
    post1 = Post(content="Post 1", user_id=1)
    post2 = Post(content="Post 2", user_id=1)

    db.session.add(post1)
    db.session.add(post2)

    db.session.commit()

  response = client.get("/api/posts", headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert len(response_data) == 2


def test_get_single_post(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  with client.application.app_context():
    post = Post(content="Single Post", user_id=1)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  response = client.get(f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["content"] == "Single Post"


def test_update_post(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  with client.application.app_context():
    post = Post(content="Old Content", user_id=1)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  data = {"content": "Updated Content"}
  
  response = client.put(f"/api/posts/{post_id}", json=data, headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["content"] == "Updated Content"


def test_delete_post(client):
  response_signin = client.post('/api/auth/sign-in', json={
    "email": "cesarvillalobosolmos.01@gmail.com",
    "password": "Password123"
  })

  assert response_signin.status_code == 200
  token = response_signin.get_json()['token']

  with client.application.app_context():
    post = Post(content="Delete Me", user_id=1)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  response = client.delete(f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["message"] == "Post deleted"

  response = client.get(f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {token}"})
  assert response.status_code == 404
