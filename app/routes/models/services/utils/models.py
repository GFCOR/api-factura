from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

class ProductoCompra(BaseModel):
    id: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., description="Cantidad del producto a comprar")

class Compra(BaseModel):
    usuario_id: int = Field(..., example=20007)
    productos: List[ProductoCompra]
    fecha: datetime
class ProductoFactura(BaseModel):
    id_prod: int = Field(..., description="ID del producto")
    precio_unitario: float = Field(..., description="Precio unitario del producto")
    cantidad: int = Field(..., description="Cantidad del producto")
    subtotal: float = Field(..., description="Subtotal del producto")

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


