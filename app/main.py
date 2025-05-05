from fastapi import FastAPI
from .routes.controller import router
from .routes.models.services.db import get_database

app = FastAPI()

# Conectar MongoDB
db = get_database()

# Incluir rutas
app.include_router(router, prefix="/factura", tags=["factura"])

@app.get("/")
def home():
    return {"message": "API Factura operativa 🚀"}