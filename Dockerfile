# Usar una imagen de Python optimizada
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo los archivos necesarios para instalar dependencias
COPY requirements.txt .

# Instalar las dependencias necesarias (esto se cachea si requirements.txt no cambia)
RUN pip install --no-cache-dir -r requirements.txt

# Instalar curl y limpiar cache de apt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar el resto de los archivos al contenedor
COPY . .

# Exponer el puerto 8002 para API-Factura
EXPOSE 8002

# Variable de entorno para el puerto
ENV PORT=8002

# Iniciar la aplicación con uvicorn en el puerto correcto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]