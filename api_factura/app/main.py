from fastapi import FastAPI
from app.routes import factura
from .routes.models.services.db import get_database

app = FastAPI()

# Conectar MongoDB
db = get_database()

# Incluir rutas
app.include_router(factura.router, prefix="/factura", tags=["factura"])

@app.get("/")
def home():
    return {"message": "API Factura operativa 🚀"}