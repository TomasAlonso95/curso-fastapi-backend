from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId # Esto nos sirve para convertir un string en ObjectId y asi poder leer el id de la base de datos.

router = APIRouter(prefix="/userdb", 
                   tags= ["userdb"],
                   responses= {status.HTTP_404_NOT_FOUND: {"message": "No se ha encontrado."}}) # Definimos la ruta router de la API para que FastAPI la reconozca mediante el decorador @router.get("/users").

# Entidad user
#BaseModel nos da la capacidad de crear un objeto que represente un user con los parametros que necesitamos como name, surname, url y age.

users_list = [] # Quedará vacia solo para que no se rompa el codigo.

@router.get("/",response_model=list[User])
async def users(): 
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def user(id: str): 
    return search_user("_id",ObjectId(id))
    
# Path es una variable de la url que nos permite hacer busquedas personalizadas
# @router.get("/") 
# async def user(id: str): 
#     return search_user("_id",ObjectId(id))

# COMENTAMOS ESTA QUERY YA QUE ES REDUNTANTE REFERERNTE A LA GET DE ARRIBA, POR LO QUE AL UTILIZAR DOCS Y SWAGGER NO ES NECESARIO DECLARARLA YA QUE BUGGEA EL SISTEMA DE SWAGGER, LAS RUTAS SIEMPRE DEBEN SER CLARAS Y NO ESTAR DUPLICADAS.


@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user: User): #User es nuestro modelo de usuario, es la entidad que creamos en user.py mientras que user es el objeto que vamos a crear.
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
# Siempre que lanzamos un error debemos hacerlo con el raise debido a que es una excepcion 
# y no un return, ya que este nos sirve para devolver informacion.
    
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = db_client.users.find_one({"_id": id})
    return User(**user_schema(new_user)) # Aquí desempaquetamos el diccionario y lo pasamos a nuestro modelo de usuario.
# Acá le estamos diciendo al cliente: "Toma estos datos crudos que acabo de sacar de MongoDB, mételos en el molde User para crear un nuevo pastel (objeto), y entrégale ese pastel al cliente".

# ENDPOINTS O PUNTO DE ACCESO MEDIANTE UN DECORADOR CON: PUT
@router.put("/",response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
         db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
            
    except:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se ha actualizado el usuario"
        )
    return search_user("_id",ObjectId(user.id))


# ENDPOINTS O PUNTO DE ACCESO MEDIANTE UN DECORADOR CON: DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str): # Esto nos dice que todo a ido bien pero no devolvera nada.
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se ha eliminado el usuario"
        )

# Query en este caso es una variable de la url que nos permite hacer busquedas personalizadas    
def search_user(field: str, key): # Lo dejamos solo como key ya que podemos recibir tanto un str como un ObjectId sin problema.
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user)) # Primero obtenemos el diccionario y luego procedemos a realizar la transformacion con los datos  el usuario.
    except:
        return {"error": "No se ha encontrado el usuario"}

    
#BUSCAR MAS DOCUMENTACION SOBRE PATH Y QUERY PARA VER EJEMPLOS CLAROS EN LA DOCUMENTACION.

# Para prender el servidor fastapi usamos el comando uvicorn main:app --reload 

# CODIGOS DE STATUS: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
# Los codigos de status son para indicar el estado de la petición en HTTP y son los siguientes: 200, 201, 400, 404, 500.