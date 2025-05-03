from fastapi import APIRouter, HTTPException
from app.models.factura import Factura
from app.services.factura_service import (

)

from api_factura.app.routes.models.services.factura_service import crear_factura, obtener_facturas, \
    obtener_factura_por_id, actualizar_factura, eliminar_factura

router = APIRouter(tags=["factura"])

@router.post("/")
def crear_nueva_factura(factura: Factura):
    factura_dict = factura.dict()
    factura_id = crear_factura(factura_dict)
    if "error" in factura_id:
        raise HTTPException(status_code=500, detail=factura_id["error"])
    return {"message": "Factura creada exitosamente", "id": factura_id}

@router.get("/")
def listar_facturas():
    facturas = obtener_facturas()
    if "error" in facturas:
        raise HTTPException(status_code=500, detail=facturas["error"])
    return facturas

@router.get("/{factura_id}")
def obtener_factura(factura_id: str):
    factura = obtener_factura_por_id(factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.put("/{factura_id}")
def modificar_factura(factura_id: str, factura: Factura):
    factura_dict = factura.dict()
    resultado = actualizar_factura(factura_id, factura_dict)
    if not resultado:
        raise HTTPException(status_code=404, detail="Factura no encontrada para actualización")
    return {"message": "Factura actualizada correctamente"}

@router.delete("/{factura_id}")
def borrar_factura(factura_id: str):
    resultado = eliminar_factura(factura_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Factura no encontrada para eliminación")
    return {"message": "Factura eliminada correctamente"}