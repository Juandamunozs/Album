from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
import json
from env.env import SECRET_KEY_SIGNATURE, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from env.env import DB_FILE
from fastapi import Depends, HTTPException
from jose.exceptions import ExpiredSignatureError, JWTError

# Configurar el esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cargar usuarios desde el archivo JSON
with open(DB_FILE, "r") as db_file:
    fake_users_db = json.load(db_file)

# Función para autenticar al usuario
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:  
        # servicio_correo()
        return user
    return None

# Función para crear el token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_SIGNATURE, algorithm=ALGORITHM)

# Función para verificar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY_SIGNATURE, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token sin usuario")
        return username
    except ExpiredSignatureError as e:
        print(f"Error la expiracion: {e}")
        raise HTTPException(status_code=401, detail="Token expirado.")
    except JWTError as e:
        print(f"Error en la autenticacion: {e}")
        raise HTTPException(status_code=401, detail="Token inválido.")
    
# Función para guardar el usuario en la base de datos
def save_user(username: str, password: str, rol: str):
    with open(DB_FILE, "r") as db_file:
        db = json.load(db_file)
    if username in db:
        return False
    db[username] = {"username": username, "password": password, "rol": rol}
    with open(DB_FILE, "w") as db_file:
        json.dump(db, db_file, indent=4)
    return True

# Función para eliminar el usuario de la base de datos
def delete_user_db(username: str):
    with open(DB_FILE, "r") as db_file:
        db = json.load(db_file)
    if username not in db:
        return False 
    db.pop(username)
    with open(DB_FILE, "w") as db_file:
        json.dump(db, db_file, indent=4)
    return True 

# Función para obtener el rol del usuario
def get_user_role(username: str):
    with open(DB_FILE, "r") as db_file:
        db = json.load(db_file)
    return db[username]["rol"]
