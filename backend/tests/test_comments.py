import pytest
from src.server import create_app
from src.database import db
from src.models import Comment, User, Post

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  
  with app.app_context():
    db.create_all()
    # Crea un usuario y un post de prueba
    user = User(name="John Doe", email="john@example.com")
    post = Post(title="Test Post", content="Test Content", user_id=1)
    db.session.add(user)
    db.session.add(post)
    db.session.commit()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

def test_create_comment(client):
  response = client.post('/comments/1', json={"content": "This is a test comment."})
  assert response.status_code == 201
  
  data = response.get_json()
  assert data['comment'] == "This is a test comment."
  assert data['post_id'] == 1

def test_create_comment_no_content(client):
  response = client.post('/comments/1', json={"content": ""})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Content is required"

def test_create_comment_exceeds_length(client):
  long_content = "x" * 501
  response = client.post('/comments/1', json={"content": long_content})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Content cannot exceed 500 characters"

def test_get_all_comments(client):
  client.post('/comments/1', json={"content": "First comment"})
  client.post('/comments/1', json={"content": "Second comment"})
  
  response = client.get('/comments/1')
  assert response.status_code == 200
  
  data = response.get_json()
  assert len(data) == 2
  assert data[0]['comment'] == "First comment"
  assert data[1]['comment'] == "Second comment"

def test_update_comment(client):
  client.post('/comments/1', json={"content": "Original comment"})
  
  response = client.put('/comments/1/1', json={"content": "Updated comment"})
  assert response.status_code == 200
  
  data = response.get_json()
  assert data['comment'] == "Updated comment"

def test_update_comment_not_found(client):
  response = client.put('/comments/1/99', json={"content": "Does not exist"})
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to update comment"

def test_delete_comment(client):
  client.post('/comments/1', json={"content": "Comment to delete"})
  response = client.delete('/comments/1/1')
  assert response.status_code == 200
  assert response.get_json()['message'] == "Comment deleted"

def test_delete_comment_not_found(client):
  response = client.delete('/comments/1/99')
  assert response.status_code == 400
  assert response.get_json()['error'] == "Failed to delete comment"
