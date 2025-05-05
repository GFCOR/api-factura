from pydantic import BaseModel, Field
from typing import List, Dict
import re
class Compra(BaseModel):
    usuario_id: int = Field(..., example=12345)
    productos: List[Dict[str, int]]  # Cada producto tiene un ID y una cantidad
    fecha: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}$")

def validar_email(email: str):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None