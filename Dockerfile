# Imagen base
FROM python:3.13-slim

# Carpeta de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install  -r requirements.txt

# Copiar el código
COPY ./src /app/src

# Exponer puerto
EXPOSE 8000

# Ejecutar FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

