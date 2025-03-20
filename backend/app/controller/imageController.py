from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from service.imageService import guardar_archivo, listar_imagenes, eliminar_imagen, obtener_imagen
from service.userService import get_current_user

router = APIRouter(prefix="/imagenes", tags=["Imagenes"])

# Endpoint para guardar imágenes
@router.post("/save/")
async def upload_image(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    try:
        resultado = await guardar_archivo(file)
        return JSONResponse(content={"message": "Archivo cargado exitosamente", "filename": resultado}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al cargar el archivo", "error": str(e)}, status_code=500)

# Endpoint para listar imágenes
@router.get("/list/")
async def list_images(user: str = Depends(get_current_user)):
    return listar_imagenes()

# Endpoint para eliminar una imagen
@router.delete("/delete_image/{filename}")
async def delete_image(filename: str, user: str = Depends(get_current_user)):
    return eliminar_imagen(filename, user)

# Endpoint para obtener una imagen específica
@router.get("/uploads/{image_name}")
async def get_image(image_name: str, user: str = Depends(get_current_user)):
    return obtener_imagen(image_name)
