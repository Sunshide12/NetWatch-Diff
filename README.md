# NetWatch-Diff

NetWatch-Diff es una herramienta ligera y rápida desarrollada en Python que monitoriza continuamente los puertos abiertos de una dirección IP objetivo. Funciona estableciendo una "línea base" en su primer escaneo y, posteriormente, te alerta de cualquier anomalía (puertos que se han abierto o cerrado de forma inesperada).

Está diseñada para ser ejecutada fácilmente mediante Docker.

## Características
- **Escaneo concurrente ultrarrápido:** Utiliza un `ThreadPoolExecutor` para escanear simultáneamente los 1024 puertos principales + puertos comunes de desarrollo (3000, 8080, 5432, etc.).
- **Alertas Diff:** Solo te notifica cuando hay un cambio de estado real en la red, evitando el spam en los logs.
- **Dockerizado:** Basado en `python:3.11-alpine` para un consumo mínimo de recursos.
- **Configurable:** Todo se controla mediante un sencillo archivo `.env`.

## Requisitos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Uso

1. **Clona el repositorio** o descarga los archivos.
2. **Configura las variables** en el archivo `.env`. Por defecto incluye:
   ```env
   TARGET_IP=192.168.1.142
   SCAN_INTERVAL_MINS=1
   ```
   *Nota: Puedes usar decimales en `SCAN_INTERVAL_MINS` (ej. `0.1` para escanear cada 6 segundos).*

3. **Inicia el contenedor** en segundo plano con Docker Compose:
   ```bash
   docker compose up -d --build
   ```

4. **Ver los logs** en tiempo real para monitorizar la actividad:
   ```bash
   docker logs -f netwatch-diff
   ```

## Archivos Principales
* `main.py`: El script principal que contiene la lógica de escaneo y comparación.
* `Dockerfile`: Instrucciones de construcción de la imagen Alpine.
* `docker-compose.yml`: Orquestador para levantar el servicio leyendo la configuración de `.env`.
* `.env`: Tus variables de entorno.

## Licencia
Distribuido libremente para uso personal y educativo.
