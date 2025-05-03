from pydantic import BaseModel, Field
from typing import List, Dict
import re

class Factura(BaseModel):
    usuario_id: str = Field(..., example="65a8c3f2e89b4b001f2e6a7b")
    productos: List[Dict[str, str]]
    total: float = Field(..., gt=0, example=1272.48)
    fecha: str = Field(..., regex="^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}$")
    datos_usuario: Dict[str, str]

def validar_email(email: str):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None