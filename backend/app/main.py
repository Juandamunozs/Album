from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from archive.descarga import guardar_archivo
from archive.login import UserLogin, authenticate_user, create_access_token
from env.env import SECRET_KEY_SIGNATURE, ALGORITHM, UPLOAD_DIRECTORY, BASE_URL
from fastapi.staticfiles import StaticFiles

# Configurar el esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear la aplicación FastAPI
app = FastAPI()

# Sirve las imágenes desde la carpeta "image"
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Función para verificar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Token recibido: {token}") 
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

# Endpoint para guardar archivos
@app.post("/save/")
async def upload_image(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    try:
        resultado = await guardar_archivo(file)
        return JSONResponse(content={"message": f"Archivo cargado exitosamente por {user}", "filename": resultado}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al cargar el archivo", "error": str(e)}, status_code=500)

# Endpoint para los enlaces de los archivos
@app.get("/list/")
async def list_images():
    try:
        files = [f.name for f in UPLOAD_DIRECTORY.iterdir() if f.is_file()]
        if not files:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes")
        
        image_urls = [f"{BASE_URL}{filename}" for filename in files]
        return {"images": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
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

# Endpoint para eliminar una imagen
@app.delete("/delete/{filename}")
async def delete_image(filename: str, user: str = Depends(get_current_user)):
    try:
        file_path = UPLOAD_DIRECTORY / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        file_path.unlink()
        return JSONResponse(content={"message": f"Archivo eliminado exitosamente por {user}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al eliminar el archivo", "error": str(e)}, status_code=500)

#uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# source venv/Scripts/activate