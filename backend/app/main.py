from fastapi import HTTPException, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controller import userController, imageController
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from env.env import UPLOAD_DIRECTORY
from service.userService import get_current_user

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

# Incluir el router
app.include_router(userController.router, prefix="/apiV1", tags=[""])
app.include_router(imageController.router, prefix="/apiV1", tags=[""])

"""

Para ejecutar la aplicación, puedes utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

python -m venv venv
source venv/Scripts/activate

"""