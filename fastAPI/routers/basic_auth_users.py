from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/basic_auth_users",
                   tags= ["basic_auth_users"],
                   responses= {404: {"message": "No se ha encontrado el usuario."}}) # Acá definimos la ruta router de la API para que FastAPI la reconozca mediante el decorador @router.
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    email: str
    surname: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "tomyydev": {
    "username": "tomyydev",
    "surname": "Tomas Contreras",
    "email": "tomy@dev.com",
    "disable": False,
    "password": "123456"
    },
    "tomyydev2": {
    "username": "tomyydev2",
    "surname": "Tomas Contreras 2",
    "email": "tomy2@dev.com",
    "disable": True,
    "password": "654321"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Los ** son para desempaquetar el diccionario
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # Los ** son para desempaquetar el diccionario

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token) # Esto es asi por que el token es el username de la base de datos.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas.", 
            headers={"WWW-Authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo.")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto.")  

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta.")  
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
