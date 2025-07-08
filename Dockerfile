FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos
COPY . /app

# Instala librerías del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala pip y dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando por defecto
CMD ["gunicorn", "Servidor.wsgi:application", "--bind", "0.0.0.0:8000"]
