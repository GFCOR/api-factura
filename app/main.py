from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.controller import router
from .routes.models.services.db import get_database

app = FastAPI()

# Configuración CORS abierta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar MongoDB
db = get_database()

# Incluir rutas
app.include_router(router, prefix="/factura", tags=["factura"])

@app.get("/")
def home():
    return {"message": "API Factura operativa 🚀"}