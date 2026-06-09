from fastapi import APIRouter

# Esto es la definición de la instancia de la API para FastAPI.
router = APIRouter(prefix="/products",
                tags=["products"],
                responses= {404: {"message": "No se ha encontrado el producto."}}) 

products_list = ["Producto 1", "Producto 2", 
                "Producto 3", "Producto 4", "Producto 5"]
@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    
    return products_list[id]