import pytest
from app import create_app
from src.database import db
from src.models import Post, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
  app = create_app("testing")

  with app.test_client() as client:
    with app.app_context():
      db.create_all()
      # Crear un usuario para pruebas
      user = User(
        name="Test",
        lastName="User",
        email="testuser@example.com",
        password=generate_password_hash("Password123", method="pbkdf2:sha256")
      )

      db.session.add(user)
      db.session.commit()

    yield client

    with app.app_context():
      db.session.remove()
      db.drop_all()

def test_create_post(client):
  # Autenticación simulada
  user_id = 1
  data = {
    "title": "Test Post",
    "content": "This is a test post content."
  }

  response = client.post("/posts", json=data, headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 201
  
  response_data = response.get_json()
  assert response_data["content"] == "This is a test post content."
  assert response_data["user_id"] == user_id

def test_get_all_posts(client):
  user_id = 1
  # Crear posts para pruebas
  with client.application.app_context():
    post1 = Post(content="Post 1", user_id=user_id)
    post2 = Post(content="Post 2", user_id=user_id)

    db.session.add(post1)
    db.session.add(post2)

    db.session.commit()

  response = client.get("/posts", headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert len(response_data) == 2

def test_get_single_post(client):
  user_id = 1
  with client.application.app_context():
    post = Post(content="Single Post", user_id=user_id)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  response = client.get(f"/posts/{post_id}", headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["content"] == "Single Post"

def test_update_post(client):
  user_id = 1
  with client.application.app_context():
    post = Post(content="Old Content", user_id=user_id)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  data = {"content": "Updated Content"}
  
  response = client.put(f"/posts/{post_id}", json=data, headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["content"] == "Updated Content"

def test_delete_post(client):
  user_id = 1
  with client.application.app_context():
    post = Post(content="Delete Me", user_id=user_id)
    db.session.add(post)
    db.session.commit()
    post_id = post.id

  response = client.delete(f"/posts/{post_id}", headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 200
  
  response_data = response.get_json()
  assert response_data["message"] == "Post deleted"

  # Verificar que ya no existe
  response = client.get(f"/posts/{post_id}", headers={"Authorization": f"Bearer {user_id}"})
  assert response.status_code == 404
