from pydantic import BaseModel

# Modelo para recibir las credenciales
class UserLoginCreate(BaseModel):
    username: str
    password: str
    rol: str

class UserLogin(BaseModel):
    username: str
    password: str
