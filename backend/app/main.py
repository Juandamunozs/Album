from fastapi import FastAPI, HTTPException, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from service.descarga import guardar_archivo
from service.login import UserLogin, UserLoginCreate,authenticate_user, create_access_token, get_current_user, save_user, delete_user_db, get_user_role
from env.env import BASE_URL
from env.router import UPLOAD_DIRECTORY
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import StreamingResponse
import os
import mimetypes

# Crear la aplicación FastAPI
app = FastAPI()

# Middleware para proteger archivos estáticos
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/uploads"):
            try:
                # Verifica el usuario con el token en la cabecera
                token = request.headers.get("Authorization").replace("Bearer ", "")
                user: dict = get_current_user(token)
            except Exception:
                raise HTTPException(status_code=401, detail="No autorizado para acceder a archivos estáticos")
        return await call_next(request)

# Agregar el middleware a la aplicación
app.add_middleware(AuthMiddleware)

# Servir archivos estáticos protegidos
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

# Endpoint para guardar las imágenes
@app.post("/save/")
async def upload_image(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    try:
        resultado = await guardar_archivo(file)
        return JSONResponse(content={"message": f"Archivo cargado exitosamente por {user}", "filename": resultado}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al cargar el archivo", "error": str(e)}, status_code=500)

# Endpoint para listar las imágenes por los links
@app.get("/list/")
async def list_images(user: str = Depends(get_current_user)):
    try:
        # Obtener los archivos dentro del directorio de imágenes
        files = [f.name for f in UPLOAD_DIRECTORY.iterdir() if f.is_file()]
        
        if not files:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes")
        
        # Crear los enlaces a las imágenes
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
    role = get_user_role(user.username)
    access_token = create_access_token(data={"sub": valid_user["username"], "role": role})
    return {"token": access_token, "type": "bearer"}

# Endpoint para crear un usuario
@app.post("/create")
async def create_user(user: UserLoginCreate, userAuth: str = Depends(get_current_user)):
    if not save_user(user.username, user.password, user.rol):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return {"message": "Usuario creado exitosamente"}

# Endpoint para eliminar una imagen
@app.delete("/delete_image/{filename}")
async def delete_image(filename: str, user: str = Depends(get_current_user)):
    try:
        file_path = UPLOAD_DIRECTORY / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        file_path.unlink()
        return JSONResponse(content={"message": f"Archivo eliminado exitosamente por {user}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al eliminar el archivo", "error": str(e)}, status_code=500)
    
# Endpoint para eliminar un usuario
@app.delete("/delete_user/{username}")
async def delete_user(username: str, user: dict = Depends(get_current_user)):
    rol = get_user_role(user)
    print(rol)
    if rol != "ADMIN":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar usuarios")

    if not delete_user_db(username):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

@app.get("/uploads/{image_name}")
async def get_image(image_name: str, user: dict = Depends(get_current_user)):
    image_path = os.path.join(UPLOAD_DIRECTORY, image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    mime_type, _ = mimetypes.guess_type(image_path)
    
    if mime_type is None:
        raise HTTPException(status_code=415, detail="Tipo de archivo no soportado")
    
    file = open(image_path, "rb")
    return StreamingResponse(file, media_type=mime_type)

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# source venv/Scripts/activate