from fastapi import APIRouter, HTTPException
from .models.services.utils.validation import Compra
from .models.services.factura_service import (
    crear_factura,
    obtener_facturas,
    obtener_factura_por_id,
    actualizar_factura,
    eliminar_factura,
    obtener_datos_usuario,
    obtener_datos_producto,
)

router = APIRouter(tags=["factura"])

@router.post("/")
def crear_nueva_factura(compra: Compra):
    # Obtener datos del usuario
    datos_usuario = obtener_datos_usuario(compra.usuario_id)
    if "error" in datos_usuario:
        raise HTTPException(status_code=500, detail=datos_usuario["error"])

    # Obtener datos de los productos y calcular subtotales
    productos_detalles = []
    for producto in compra.productos:
        producto_detalle = obtener_datos_producto(producto["id"])
        if "error" in producto_detalle:
            raise HTTPException(status_code=500, detail=producto_detalle["error"])

        # Calcular subtotal para el producto
        subtotal = producto_detalle["precio"] * producto["cantidad"]
        productos_detalles.append({
            "id_producto": producto_detalle["id_producto"],
            "nombre": producto_detalle["nombre"],
            "descripcion": producto_detalle["descripcion"],
            "precio_unitario": producto_detalle["precio"],
            "cantidad": producto["cantidad"],
            "subtotal": subtotal
        })

    # Calcular el total general de la factura
    total = sum(item["subtotal"] for item in productos_detalles)

    # Crear la factura final
    factura_dict = {
        "usuario_id": compra.usuario_id,
        "datos_usuario": datos_usuario,
        "productos": productos_detalles,
        "total": total,
        "fecha": compra.fecha
    }

    # Guardar la factura en la base de datos
    factura_id = crear_factura(factura_dict)
    if "error" in factura_id:
        raise HTTPException(status_code=500, detail=factura_id["error"])

    return {"message": "Factura creada exitosamente", "id": factura_id}

@router.get("/")
def listar_facturas(skip: int = 0, limit: int = 10):
    facturas = obtener_facturas(skip=skip, limit=limit)
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
def modificar_factura(factura_id: str, compraModificada: Compra):
    factura_dict = compraModificada.dict()
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