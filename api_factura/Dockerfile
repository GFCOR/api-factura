# Usar una imagen de Python optimizada
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos al contenedor
COPY . .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8002 para API-Factura
EXPOSE 8002

# Variable de entorno para el puerto
ENV PORT=8002

# Iniciar la aplicación con uvicorn en el puerto correcto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]