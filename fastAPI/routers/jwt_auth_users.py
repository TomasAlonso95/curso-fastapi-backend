from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
# La autentifacion con JWT se diferencia de la autentificacion con Basic Auth en que en la autenticacion basic se envian credenciales en el header y en la autenticacion JWT se envian en el body, por lo que el token se envia en el body y no en el header que seria la cabecera de la peticion, lo que lo hace mas seguro.

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # Esto equivale a un minuto.
SECRET = "7e3e811d8b514ccac06dc44afa1812ab8bcc128cb625a22f6456336c3e2ac13f" # Esto es la clave secreta que se usa para encriptar y desencriptar el token.

router = APIRouter(prefix= "/jwtauth", 
                   tags=["jwtauth"], 
                   responses= {404: {"message": "No se ha encontrado el usuario."}}) # Acá definimos la ruta router de la API para que FastAPI la reconozca mediante el decorador @router.get("/users").

oauth2 = OAuth2PasswordBearer(tokenUrl="login") # Definimos el tokenUrl para que FastAPI lo reconozca mediante el decorador @router.post("/login").
crypt = CryptContext(schemes=["bcrypt"])
class User(BaseModel): # BaselModel se usa para crear un objeto que represente un user con los parametros que necesitamos como name, surname, url y age.
    username: str
    email: str
    surname: str
    disable: bool

class UserDB(User): # Aca creamos la clase UserDB que hereda de la clase User y que se usa para la autenticacion.
    password: str

users_db = {
    "tomyydev": {
    "username": "tomyydev",
    "surname": "Tomas Contreras",
    "email": "tomy@dev.com",
    "disable": False,
    "password": "$2b$12$UVGn82lHjiBpLBnJ0bNkB.EA6AMzxIBqQnKkULLul43.ZRKyM6QJO"
    },
    "tomyydev2": {
    "username": "tomyydev2",
    "surname": "Tomas Contreras 2",
    "email": "tomy2@dev.com",
    "disable": True,
    "password": "$2a$12$n5ROj3S.g6DDlEVw68DyrO153XfxNuscXKqPcl7IyENctnZdsATw2"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Los ** son para desempaquetar el diccionario

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # Los ** son para desempaquetar el diccionario

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas.", 
            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)      

async def current_user(user: User= Depends(auth_user)):
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
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta.")  
    
    access_token = {"sub": user.username, # sub es el subject del token, es decir el username del user.
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)} # exp es el expiration time del token, es decir el tiempo en el que expira el token.
                    
    return {"access_token": jwt.encode(access_token, SECRET, ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user