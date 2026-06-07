FROM python:3.11-alpine

# Evita que Python escriba archivos .pyc en el disco y asegura salida directa de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY main.py .
CMD ["python", "main.py"]
