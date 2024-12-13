from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from archive.descarga import guardar_archivo
from archive.login import UserLogin, authenticate_user, create_access_token, SECRET_KEY_SIGNATURE

SECRET_KEY = SECRET_KEY_SIGNATURE
ALGORITHM = "HS256"

# Configurar el esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Función para obtener el usuario actual a partir del token
def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Token recibido: {token}") 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    try:
        # Llamar a la función para guardar el archivo
        resultado = await guardar_archivo(file)
        return JSONResponse(content={"message": f"Archivo cargado exitosamente por {user}", "filename": resultado}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al cargar el archivo", "error": str(e)}, status_code=500)

# Endpoint para generar el token
@app.post("/login")
async def login(user: UserLogin):
    valid_user = authenticate_user(user.username, user.password)
    if not valid_user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": valid_user["username"]})
    return {"token": access_token, "type": "bearer"}

#uvicorn main:app --host 172.31.150.16 --port 8000 --reload