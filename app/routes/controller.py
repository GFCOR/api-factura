from fastapi import APIRouter, HTTPException, Request
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
import logging

router = APIRouter()
logger = logging.getLogger("factura_controller")

@router.post("/")
def crear_nueva_factura(compra: Compra, request: Request):
    logger.info(f"Solicitud recibida en {request.url.path}: {compra}")
    try:
        datos_usuario = obtener_datos_usuario(compra.usuario_id)
        logger.info(f"Datos usuario: {datos_usuario}")
        if "error" in datos_usuario:
            logger.error(f"Error usuario: {datos_usuario['error']}")
            raise HTTPException(status_code=400, detail=datos_usuario["error"])

        productos_detalles = []
        for producto in compra.productos:
            producto_detalle = obtener_datos_producto(producto.id)
            logger.info(f"Producto detalle: {producto_detalle}")
            if "error" in producto_detalle:
                logger.error(f"Error producto: {producto_detalle['error']}")
                raise HTTPException(status_code=400, detail=producto_detalle["error"])
            if "precio" not in producto_detalle:
                logger.error(f"Producto sin precio: {producto_detalle}")
                raise HTTPException(status_code=422, detail="El producto no tiene precio")
            subtotal = producto_detalle["precio"] * producto.cantidad
            productos_detalles.append({
                "id_producto": producto_detalle.get("id_producto"),
                "nombre": producto_detalle.get("nombre"),
                "descripcion": producto_detalle.get("descripcion", ""),
                "precio_unitario": producto_detalle.get("precio"),
                "cantidad": producto.cantidad,
                "subtotal": subtotal
            })

        total = sum(item["subtotal"] for item in productos_detalles)
        factura_dict = {
            "usuario_id": compra.usuario_id,
            "datos_usuario": datos_usuario,
            "productos": productos_detalles,
            "total": total,
            "fecha": compra.fecha
        }
        logger.info(f"Factura dict: {factura_dict}")
        factura_id = crear_factura(factura_dict)
        logger.info(f"Factura id: {factura_id}")
        if isinstance(factura_id, dict) and "error" in factura_id:
            logger.error(f"Error al crear factura: {factura_id['error']}")
            raise HTTPException(status_code=500, detail=factura_id["error"])

        return {"message": "Factura creada exitosamente", "id": factura_id}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Error inesperado al crear factura")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/")
def listar_facturas(skip: int = 0, limit: int = 10, request: Request = None):
    logger.info(f"Solicitud GET {request.url.path} skip={skip} limit={limit}")
    try:
        facturas = obtener_facturas(skip=skip, limit=limit)
        if isinstance(facturas, dict) and "error" in facturas:
            logger.error(f"Error al obtener facturas: {facturas['error']}")
            raise HTTPException(status_code=500, detail=facturas["error"])
        return facturas
    except Exception as e:
        logger.exception("Error inesperado al listar facturas")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/{factura_id}")
def obtener_factura(factura_id: str, request: Request):
    logger.info(f"Solicitud GET {request.url.path} factura_id={factura_id}")
    try:
        factura = obtener_factura_por_id(factura_id)
        if isinstance(factura, dict) and "error" in factura:
            logger.error(f"Error al obtener factura: {factura['error']}")
            if factura["error"] == "ID de factura no válido":
                raise HTTPException(status_code=400, detail=factura["error"])
            elif factura["error"] == "Factura no encontrada":
                raise HTTPException(status_code=404, detail=factura["error"])
            else:
                raise HTTPException(status_code=500, detail=factura["error"])
        return factura
    except Exception as e:
        logger.exception("Error inesperado al obtener factura")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.put("/{factura_id}")
def modificar_factura(factura_id: str, compraModificada: Compra, request: Request):
    logger.info(f"Solicitud PUT {request.url.path} factura_id={factura_id} data={compraModificada}")
    try:
        factura_dict = compraModificada.dict()
        resultado = actualizar_factura(factura_id, factura_dict)
        if isinstance(resultado, dict) and "error" in resultado:
            logger.error(f"Error al actualizar factura: {resultado['error']}")
            raise HTTPException(status_code=500, detail=resultado["error"])
        if not resultado:
            logger.warning("Factura no encontrada para actualización")
            raise HTTPException(status_code=404, detail="Factura no encontrada para actualización")
        return {"message": "Factura actualizada correctamente"}
    except Exception as e:
        logger.exception("Error inesperado al actualizar factura")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{factura_id}")
def borrar_factura(factura_id: str, request: Request):
    logger.info(f"Solicitud DELETE {request.url.path} factura_id={factura_id}")
    try:
        resultado = eliminar_factura(factura_id)
        if isinstance(resultado, dict) and "error" in resultado:
            logger.error(f"Error al eliminar factura: {resultado['error']}")
            raise HTTPException(status_code=500, detail=resultado["error"])
        if not resultado:
            logger.warning("Factura no encontrada para eliminación")
            raise HTTPException(status_code=404, detail="Factura no encontrada para eliminación")
        return {"message": "Factura eliminada correctamente"}
    except Exception as e:
        logger.exception("Error inesperado al eliminar factura")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")