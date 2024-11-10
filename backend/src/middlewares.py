import jwt
from flask import request

SECRET_KEY = "my_secret_key"

def require_auth():
  token = request.headers.get("Authorization")

  if not token:
    return None
  
  try:
    token = token.replace("Bearer ", "")
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    current_user_id = data.get("user_id")

    if not current_user_id:
      return None
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None

  return current_user_id
