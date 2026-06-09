from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", 
                   tags= ["users"],
                   responses= {404: {"message": "No se ha encontrado el usuario."}}) # Definimos la ruta router de la API para que FastAPI la reconozca mediante el decorador @router.get("/users").

# Entidad user
class User(BaseModel): # Acá definimos una entidad la cual nos sirve para crear un user dandole los parametros que necesitamos.
    id: int
    name: str
    surname: str
    url: str
    age: int
#BaseModel nos da la capacidad de crear un objeto que represente un user con los parametros que necesitamos como name, surname, url y age.

users_list = [
    User(id=1, name="Tomas", surname="Contreras", url="https://tomyy.dev", age=30),
    User(id=2, name="Samantha", surname="Urrutia", url="https://sammy.com", age=25),
    User(id=3, name="Felipe", surname="claro", url="https://felipe.com", age=50)
]

@router.get("/usersjson")
async def usersjson(): 
    return [{ "name": "Tomas", "surname": "Contreras", "url": "https://tomyy.dev", "age": 30},
            { "name": "Samantha", "surname": "Urrutia", "url": "https://sammy.com","age": 25}, 
            { "name": "Felipe", "surname": "Claro", "url": "https://felipe.com", "age": 50}]

@router.get("/")
async def users(): 
    return users_list

@router.get("/user/{id}")
async def users(id: int): 
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
# Path es una variable de la url que nos permite hacer busquedas personalizadas
@router.get("/user/")
async def users(id: int): 
    return search_user(id)

@router.get("/")
async def get_all_users():
    return users_list

@router.post("/user/",response_model=User,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
# Siempre que lanzamos un error debemos hacerlo con el raise debido a que es una excepcion 
# y no un return, ya que este nos sirve para devolver informacion.

    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):

    found = False
    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
            return {"error": "No se ha actualizado el usuario"}
    return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            found = True
    if not found:
            return {"error": "No se ha eliminado el usuario"}

# Query en este caso es una variable de la url que nos permite hacer busquedas personalizadas    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
#BUSCAR MAS DOCUMENTACION SOBRE PATH Y QUERY PARA VER EJEMPLOS CLAROS EN LA DOCUMENTACION.

# Para prender el servidor fastapi usamos el comando uvicorn main:app --reload 

# CODIGOS DE STATUS: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
# Los codigos de status son para indicar el estado de la petición en HTTP y son los siguientes: 200, 201, 400, 404, 500.