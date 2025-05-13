from .db import get_database
from bson import ObjectId
from bson.errors import InvalidId
import httpx
import logging

db = get_database()
facturas_collection = db["facturas_collection"]

API_USUARIOS_URL = "http://api-usuarios:8000/users/{user_id}"
API_PRODUCTOS_URL = "http://api-productos:8001/productos/{id}"

logger = logging.getLogger("factura_service")

def crear_factura(factura_data):
    try:
        nueva_factura = facturas_collection.insert_one(factura_data)
        logger.info(f"Factura insertada con _id: {nueva_factura.inserted_id}")
        return str(nueva_factura.inserted_id)
    except Exception as e:
        logger.exception("No se pudo crear la factura")
        return {"error": f"No se pudo crear la factura: {str(e)}"}


def obtener_datos_usuario(usuario_id: int):
    try:
        with httpx.Client() as client:
            response = client.get(API_USUARIOS_URL.format(user_id=usuario_id))
            logger.info(f"Respuesta API usuario: {response.status_code} {response.text}")
            if response.status_code != 200:
                return {"error": f"Error al obtener datos del usuario: {response.status_code}"}
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error de conexión a API usuarios: {str(e)}")
        return {"error": f"Error de conexión a la API de usuarios: {str(e)}"}
    except Exception as e:
        logger.exception("Error inesperado al consultar la API de usuarios")
        return {"error": f"Error inesperado al consultar la API de usuarios: {str(e)}"}

def obtener_datos_producto(producto_id: int):
    try:
        with httpx.Client() as client:
            response = client.get(API_PRODUCTOS_URL.format(id=producto_id))
            logger.info(f"Respuesta API producto: {response.status_code} {response.text}")
            if response.status_code != 200:
                return {"error": f"Error al obtener datos del producto con ID {producto_id}: {response.status_code}"}
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error de conexión a API productos: {str(e)}")
        return {"error": f"Error de conexión a la API de productos: {str(e)}"}
    except Exception as e:
        logger.exception("Error inesperado al consultar la API de productos")
        return {"error": f"Error inesperado al consultar la API de productos: {str(e)}"}

def obtener_facturas(skip=0, limit=10, usuario_id=None):
    try:
        filtro = {}
        if usuario_id is not None:
            filtro["usuario_id"] = usuario_id
        facturas = list(facturas_collection.find(filtro).skip(skip).limit(limit))
        logger.info(f"Facturas encontradas: {len(facturas)}")
        for factura in facturas:
            factura["_id"] = str(factura["_id"])
        return facturas
    except Exception as e:
        logger.exception("No se pudieron obtener las facturas")
        return {"error": f"No se pudieron obtener las facturas: {str(e)}"}

def obtener_factura_por_id(factura_id):
    try:
        try:
            obj_id = ObjectId(factura_id)
        except InvalidId:
            logger.warning(f"ID de factura no válido: {factura_id}")
            return {"error": "ID de factura no válido"}
        factura = facturas_collection.find_one({"_id": obj_id})
        if factura:
            factura["_id"] = str(factura["_id"])
            return factura
        else:
            logger.info(f"Factura no encontrada: {factura_id}")
            return {"error": "Factura no encontrada"}
    except Exception as e:
        logger.exception("Error al buscar la factura")
        return {"error": f"Error al buscar la factura: {str(e)}"}

def actualizar_factura(factura_id, factura_data):
    try:
        try:
            obj_id = ObjectId(factura_id)
        except InvalidId:
            logger.warning(f"ID de factura no válido para actualizar: {factura_id}")
            return {"error": "ID de factura no válido"}
        resultado = facturas_collection.update_one(
            {"_id": obj_id},
            {"$set": factura_data}
        )
        logger.info(f"Resultado update: matched={resultado.matched_count}, modified={resultado.modified_count}")
        return resultado.modified_count > 0
    except Exception as e:
        logger.exception("Error al actualizar la factura")
        return {"error": f"Error al actualizar la factura: {str(e)}"}

def eliminar_factura(factura_id):
    try:
        try:
            obj_id = ObjectId(factura_id)
        except InvalidId:
            logger.warning(f"ID de factura no válido para eliminar: {factura_id}")
            return {"error": "ID de factura no válido"}
        resultado = facturas_collection.delete_one({"_id": obj_id})
        logger.info(f"Resultado delete: deleted={resultado.deleted_count}")
        return resultado.deleted_count > 0
    except Exception as e:
        logger.exception("Error al eliminar la factura")
        return {"error": f"Error al eliminar la factura: {str(e)}"}