from pathlib import Path
from fastapi import UploadFile

# Directorio donde se guardarán las imágenes
UPLOAD_DIRECTORY = Path("image")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

async def guardar_archivo(file: UploadFile) -> str:
    # Ruta completa del archivo
    file_path = UPLOAD_DIRECTORY / file.filename
    
    # Guardar el archivo en el sistema de archivos
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    return file.filename
