from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI() # Definimos la instancia de la API para FastAPI.

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="statics"), name="static")
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router) 
@app.get("/")
async def root():
    return "!Hola FastAPI!"
# ==========================================
# RECORDATORIO: ERROR 404 EN /favicon.ico
# ==========================================
# Al hacer una petición GET a la raíz ("/") desde un navegador web, este buscará 
# automáticamente un archivo llamado 'favicon.ico' para mostrar en la pestaña.
# Como no hemos definido una ruta @app.get("/favicon.ico") ni configurado 
# la entrega de archivos estáticos, FastAPI no lo encuentra y lanza un 404.
# Conclusión: La API funciona perfectamente, el navegador solo está siendo insistente.

@app.get("/url")
async def url():
    return { "url": "https://tomyydev.com/python" }