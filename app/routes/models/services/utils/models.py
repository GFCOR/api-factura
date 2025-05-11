from pydantic import BaseModel, Field

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