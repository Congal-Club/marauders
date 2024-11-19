import os
import pytest
from io import BytesIO
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
    # Crear usuario y post de prueba
    user = User(name="John Doe", email="john@example.com")
    post = Post(title="Test Post", content="This is a test post.")
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
    return 1  # Usuario autenticado con ID 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)

  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  response = client.post('/images/1', data=data, content_type='multipart/form-data')
  assert response.status_code == 201
  json_data = response.get_json()
  assert json_data['message'] == "Image uploaded successfully"
  assert 'image' in json_data
  assert 'test_image.jpg' in json_data['image']['image']

def test_upload_image_no_file(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  response = client.post('/images/1', data={}, content_type='multipart/form-data')
  assert response.status_code == 400
  assert response.get_json()['error'] == "No file part in the request"

def test_get_all_images(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  # Subir imagen de prueba
  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  client.post('/images/1', data=data, content_type='multipart/form-data')
  # Obtener todas las imágenes del post
  response = client.get('/images/1')
  assert response.status_code == 200
  json_data = response.get_json()
  assert len(json_data) == 1
  assert 'test_image.jpg' in json_data[0]['image']

def test_delete_image(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  # Subir imagen de prueba
  data = {
    'file': (BytesIO(b'this is a test image'), 'test_image.jpg')
  }

  upload_response = client.post('/images/1', data=data, content_type='multipart/form-data')
  image_id = upload_response.get_json()['image']['id']
  # Eliminar imagen
  response = client.delete(f'/images/1/{image_id}')
  assert response.status_code == 200
  assert response.get_json()['message'] == "Image deleted successfully"

def test_delete_image_not_found(client, monkeypatch):
  def mock_auth():
    return 1

  monkeypatch.setattr('app.views.require_auth', mock_auth)
  response = client.delete('/images/1/999')  # Intentar eliminar imagen inexistente
  assert response.status_code == 404
  assert response.get_json()['error'] == "Failed to delete image"
