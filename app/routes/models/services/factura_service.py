from .db import get_database
from bson import ObjectId
import httpx

db = get_database()
facturas_collection = db["collection"]

API_USUARIOS_URL = "http://api-usuarios:8000/users/{user_id}"
API_PRODUCTOS_URL = "http://api-productos:8001/productos/{id}"

def obtener_datos_usuario(usuario_id: int):
    try:
        with httpx.Client() as client:
            response = client.get(API_USUARIOS_URL.format(user_id=usuario_id))
            if response.status_code != 200:
                return {"error": f"Error al obtener datos del usuario: {response.status_code}"}
            return response.json()
    except Exception as e:
        return {"error": f"Error al consultar la API de usuarios: {str(e)}"}

def obtener_datos_producto(producto_id: int):
    try:
        with httpx.Client() as client:
            response = client.get(API_PRODUCTOS_URL.format(id=producto_id))
            if response.status_code != 200:
                return {"error": f"Error al obtener datos del producto con ID {producto_id}: {response.status_code}"}
            return response.json()
    except Exception as e:
        return {"error": f"Error al consultar la API de productos: {str(e)}"}
    
def crear_factura(factura_data):
    try:
        nueva_factura = facturas_collection.insert_one(factura_data)
        return str(nueva_factura.inserted_id)
    except Exception as e:
        return {"error": f"No se pudo crear la factura: {str(e)}"}

def obtener_facturas():
    try:
        facturas = list(facturas_collection.find())
        for factura in facturas:
            factura["_id"] = str(factura["_id"])
        return facturas
    except Exception as e:
        return {"error": f"No se pudieron obtener las facturas: {str(e)}"}

def obtener_factura_por_id(factura_id):
    try:
        factura = facturas_collection.find_one({"_id": ObjectId(factura_id)})
        if factura:
            factura["_id"] = str(factura["_id"])
        return factura or {"error": "Factura no encontrada"}
    except Exception as e:
        return {"error": f"Error al buscar la factura: {str(e)}"}

def actualizar_factura(factura_id, factura_data):
    try:
        resultado = facturas_collection.update_one(
            {"_id": ObjectId(factura_id)},
            {"$set": factura_data}
        )
        return resultado.modified_count > 0
    except Exception as e:
        return {"error": f"Error al actualizar la factura: {str(e)}"}

def eliminar_factura(factura_id):
    try:
        resultado = facturas_collection.delete_one({"_id": ObjectId(factura_id)})
        return resultado.deleted_count > 0
    except Exception as e:
        return {"error": f"Error al eliminar la factura: {str(e)}"}