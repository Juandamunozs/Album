from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from pydantic import BaseModel
import json

# Clave secreta y algoritmo
SECRET_KEY_SIGNATURE = "0b22b437c9a645aeb4f6e2a5b1ac528540778c5c0467554d26d643069bd4cfb4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# Cargar base de datos desde un archivo JSON
DB_FILE = "db.json"

# Cargar usuarios desde el archivo JSON
with open(DB_FILE, "r") as db_file:
    fake_users_db = json.load(db_file)

# Modelo para recibir las credenciales
class UserLogin(BaseModel):
    username: str
    password: str

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