import os
import pytest
from io import BytesIO
from werkzeug.security import generate_password_hash

from src.server import create_app
from src.database import db
from src.models import User, Post, Image

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  app.config['UPLOAD_FOLDER'] = './test_uploads'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

  with app.app_context():
    db.create_all()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    user = User(
      name="Cesar",
      lastName="Villalobos Olmos",
      email="cesarvillalobosolmos.01@gmail.com",
      password=generate_password_hash("Password123", method="pbkdf2:sha256"),
      image="http://example.com/image.jpg"
    )
    post = Post(content="This is a test post.", user_id=1)
    
    db.session.add_all([user, post])
    db.session.commit()
    
    yield app.test_client()
    
    db.session.remove()
    db.drop_all()

    if os.path.exists(app.config['UPLOAD_FOLDER']):
      for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
      os.rmdir(app.config['UPLOAD_FOLDER'])

def test_upload_image(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)

  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  response = client.post('/api/images/1', data=data, content_type='multipart/form-data')
  assert response.status_code == 201
  json_data = response.get_json()
  assert json_data['message'] == "Image uploaded successfully"
  assert 'image' in json_data
  assert 'test_image.jpg' in json_data['image']['image']

def test_upload_image_no_file(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  response = client.post('/api/images/1', data={}, content_type='multipart/form-data')
  assert response.status_code == 400
  assert response.get_json()['error'] == "No file part in the request"

def test_get_all_images(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  
  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  client.post('/api/images/1', data=data, content_type='multipart/form-data')
  response = client.get('/api/images/1')

  assert response.status_code == 200
  json_data = response.get_json()
  assert len(json_data) == 1
  assert 'test_image.jpg' in json_data[0]['image']

def test_delete_image(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  
  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  upload_response = client.post('/api/images/1', data=data, content_type='multipart/form-data')
  image_id = upload_response.get_json()['image']['id']
  
  response = client.delete(f'/api/images/1/{image_id}')
  assert response.status_code == 200
  assert response.get_json()['message'] == "Image deleted successfully"

def test_delete_image_not_found(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('src.views.require_auth', mock_auth)
  response = client.delete('/api/images/1/999')
  assert response.status_code == 404
  assert response.get_json()['error'] == "Failed to delete image"
