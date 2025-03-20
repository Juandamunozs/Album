from fastapi import APIRouter, Depends, HTTPException
from schemas.userSchema import UserLoginCreate, UserLogin
from service.userService import authenticate_user, create_access_token, save_user, delete_user_db, get_user_role, get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Endpoint para iniciar sesión y obtener token
@router.post("/login")
async def login(form_data: UserLogin):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["rol"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para crear un usuario
@router.post("/create")
async def create_user(user: UserLoginCreate, current_user: str = Depends(get_current_user)):
    if get_user_role(current_user) != "ADMIN":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear usuarios")
    
    if not save_user(user.username, user.password, user.rol):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return {"message": "Usuario creado exitosamente"}

# Endpoint para eliminar un usuario
@router.delete("/delete/{username}")
async def delete_user(username: str, current_user: str = Depends(get_current_user)):
    if get_user_role(current_user) != "ADMIN":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar usuarios")
    
    if not delete_user_db(username):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}