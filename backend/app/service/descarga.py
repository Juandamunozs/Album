from fastapi import UploadFile
from env.router import UPLOAD_DIRECTORY

# Función para guardar el archivo en el sistema de archivos
async def guardar_archivo(file: UploadFile) -> str:
    # Ruta completa del archivo
    file_path = UPLOAD_DIRECTORY / file.filename 
    
    # Guardar el archivo en el sistema de archivos
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    return file.filename
