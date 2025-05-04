from fastapi import APIRouter, HTTPException
from .models.services.utils.validation import Compra
import httpx
from api_factura.app.routes.models.services.factura_service import (
    crear_factura,
    obtener_facturas,
    obtener_factura_por_id,
    actualizar_factura,
    eliminar_factura,
)

router = APIRouter(tags=["factura"])

# URLs de las APIs externas
API_USUARIOS_URL = "http://api-usuarios.com/users/users/{user_id}"
API_PRODUCTOS_URL = "http://api-productos.com/productos/{id}"

@router.post("/")
def crear_nueva_factura(compra: Compra):
    # Obtener datos del usuario
    try:
        with httpx.Client() as client:
            usuario_response = client.get(API_USUARIOS_URL.format(user_id=compra.usuario_id))
            if usuario_response.status_code != 200:
                raise HTTPException(status_code=usuario_response.status_code, detail="Error al obtener datos del usuario")
            datos_usuario = usuario_response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la API de usuarios: {str(e)}")

    # Obtener datos de los productos
    productos_detalles = []
    for producto in compra.productos:
        try:
            with httpx.Client() as client:
                producto_response = client.get(API_PRODUCTOS_URL.format(id=producto["id"]))
                if producto_response.status_code != 200:
                    raise HTTPException(status_code=producto_response.status_code, detail=f"Error al obtener datos del producto con ID {producto['id']}")
                producto_detalle = producto_response.json()
                productos_detalles.append({
                    "id_producto": producto_detalle["id_producto"],
                    "descripcion": producto_detalle["descripcion"],
                    "precio": producto_detalle["precio"],
                    "cantidad": producto["cantidad"],  # Cantidad enviada por el cliente
                    "subtotal": producto_detalle["precio"] * producto["cantidad"]
                })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar la API de productos: {str(e)}")

    # Calcular el total de la factura
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