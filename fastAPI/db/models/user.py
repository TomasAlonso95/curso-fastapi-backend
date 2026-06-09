from pydantic import BaseModel # Pydantic nos permite gestionar modelos de datos por la API REST.


class User(BaseModel): # Acá definimos una entidad la cual nos sirve para crear un user dandole los parametros que necesitamos.
    id: str | None = None # De esta forma el campo id puede ser opcional, puede que no nos llegue 
    username: str
    email: str