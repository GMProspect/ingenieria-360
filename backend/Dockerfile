# Usar Python ligero
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y netcat-openbsd

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Exponer el puerto
EXPOSE 8000

# Comando para producción (usando Gunicorn)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
