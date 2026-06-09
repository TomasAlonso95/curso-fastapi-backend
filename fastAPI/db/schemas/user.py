def user_schema(user) -> dict:
    return {"id": str(user["_id"]), # A nuestro id le colocamos str debido a que la base de datos nos devolvera un objeto y nosotros lo que queremos es un string...
            "username": user["username"],
            "email": user["email"]
            }

# Mediante esta operacion podremos transformar lo que viene en la base de datos, el JSON en sí a formato diccionario, para poder leer los datos de mejor manera, osea, podremos leer lo que tiene nuestro objeto de modelo que es user sin problemas.

def users_schema(users) -> list:
    return [user_schema(user) for user in users]