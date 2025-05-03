from app.services.db import get_database
from bson import ObjectId

db = get_database()
facturas_collection = db["facturas"]

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