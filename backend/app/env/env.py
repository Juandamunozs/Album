import os
from pathlib import Path

# Ruta del directorio actual - donde se encuentra el archivo
dir_proyect = os.path.abspath(os.path.dirname(__file__))

# Ruta de los directorios principales
dir_assets = os.path.abspath(os.path.join(dir_proyect, '..', 'assets'))
dir_controller = os.path.abspath(os.path.join(dir_proyect, '..', 'controller'))
dir_database = os.path.abspath(os.path.join(dir_proyect, '..', 'db'))
dir_model = os.path.abspath(os.path.join(dir_proyect, '..', 'model'))
dir_schemas = os.path.abspath(os.path.join(dir_proyect, '..', 'schemas'))
dir_service = os.path.abspath(os.path.join(dir_proyect, '..', 'service'))
dir_uploads = os.path.abspath(os.path.join(dir_proyect, '..', 'uploads'))

# Verificar que la carpeta 'uploads' exista, si no, crearla
if not os.path.exists(dir_uploads):
    os.makedirs(dir_uploads)

# Archivos y URLs
IMAGE_PATH  = os.path.join(dir_assets, 'logo.pmg')
BASE_URL = "http://localhost:8000/uploads/"

# Convertir la ruta a un objeto Path
UPLOAD_DIRECTORY = Path(os.path.join(dir_proyect, '..', 'uploads'))
DB_FILE = os.path.join(dir_database, 'db.json')

# Configuración del token
SECRET_KEY_SIGNATURE = "9955ea8e1c6ce8cb33cc9e1dddba65c729078dd4ff9ff04936ee6af14bfc1cbb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuración de correo
FROM_EMAIL = "lifesnapco@gmail.com"
FROM_PASSWORD = "bhcf jhfk jvkw ibro" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587