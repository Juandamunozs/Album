import os
import mimetypes
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from env.env import UPLOAD_DIRECTORY, BASE_URL, dir_uploads

async def guardar_archivo(file):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file.filename

def listar_imagenes():
    try:
        files = [f.name for f in UPLOAD_DIRECTORY.iterdir() if f.is_file()]
        if not files:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes")
        image_urls = [f"{BASE_URL}{filename}" for filename in files]
        return {"images": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_imagen(filename, user):
    filename = filename.replace("{filename}", "")
    try:
        file_path = os.path.join(dir_uploads, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        os.remove(file_path)
        return JSONResponse(content={"message": f"Archivo eliminado exitosamente por {user}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error al eliminar el archivo", "error": str(e)}, status_code=500)

def obtener_imagen(image_name):
    image_path = os.path.join(UPLOAD_DIRECTORY, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise HTTPException(status_code=415, detail="Tipo de archivo no soportado")

    file = open(image_path, "rb")
    return StreamingResponse(file, media_type=mime_type)
