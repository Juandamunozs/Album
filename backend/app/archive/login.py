from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from pydantic import BaseModel
import json
from env.env import SECRET_KEY_SIGNATURE, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, DB_FILE

# Cargar usuarios desde el archivo JSON
with open(DB_FILE, "r") as db_file:
    fake_users_db = json.load(db_file)

# Modelo para recibir las credenciales
class UserLogin(BaseModel):
    username: str
    password: str

# Función para autenticar al usuario
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:  
        return user
    return None

# Función para crear el token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_SIGNATURE, algorithm=ALGORITHM)



















# Si el archivo no existe, se crea con datos predeterminados
# if not os.path.exists(DB_FILE):
#     with open(DB_FILE, "w") as db_file:
#         json.dump(
#             {
#                 "testuser": {
#                     "username": "testuser",
#                     "hashed_password": "hashedpassword123",
#                 },
#                 "admin": {
#                     "username": "admin",
#                     "hashed_password": "adminpassword123",
#                 },
#             },
#             db_file,
#             indent=4,
#         )