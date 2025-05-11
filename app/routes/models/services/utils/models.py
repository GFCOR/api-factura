from pydantic import BaseModel, Field
from typing import List

class ProductoCompra(BaseModel):
    id: int = Field(..., example=1, description="ID del producto")
    cantidad: int = Field(..., example=2, description="Cantidad del producto a comprar")

class Compra(BaseModel):
    usuario_id: int = Field(..., example=12345, description="ID del usuario que realiza la compra")
    productos: List[ProductoCompra] = Field(..., description="Lista de productos a comprar")
    fecha: str = Field(
        ...,
        example="2025-05-11T12:00:00",
        pattern="^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}$",
        description="Fecha de la compra en formato ISO")
    
class ProductoFactura(BaseModel):
    id_prod: int = Field(..., example=2293, description="ID del producto")
    precio_unitario: float = Field(..., example=1335.48, description="Precio unitario del producto")
    cantidad: int = Field(..., example=1, description="Cantidad del producto")
    subtotal: float = Field(..., example=1335, description="Subtotal del producto")

class UsuarioInfo(BaseModel):
    nombre: str = Field(..., example="Yago")
    apellido: str = Field(..., example="Tejera Ferrán")
    correo: str = Field(..., example="florencia22@example.net")

class FacturaIn(BaseModel):
    usuario_id: int = Field(..., example=23)
    producto: ProductoFactura
    total: float = Field(..., example=1335)
    fecha: str = Field(..., example="2024-08-04T11:16:19")
    usuario_info: UsuarioInfo


