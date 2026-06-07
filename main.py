import os
import sys
import time
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configuración mediante variables de entorno
TARGET_IP = os.environ.get("TARGET_IP")
SCAN_INTERVAL_MINS = float(os.environ.get("SCAN_INTERVAL_MINS", 1))

# Lista de puertos a escanear (Rango estándar de 1 a 1024 + puertos comunes de desarrollo)
PORTS_TO_SCAN = list(range(1, 1025)) + [
    3000, 3306, 5000, 5432, 6379, 8000, 8080, 8081, 8443, 9000, 27017
]

def log(message, level="INFO"):
    """Imprime logs con timestamp forzando el vaciado de buffer para Render/Docker."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}", flush=True)

def check_port(ip, port):
    """Intenta conectar a un puerto específico. Retorna el puerto si está abierto."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)  # Timeout rápido para evitar bloqueos prolongados
            result = s.connect_ex((ip, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def scan_ip(ip):
    """Escanea la IP objetivo de forma concurrente usando hilos."""
    open_ports = []
    # Usamos 50 hilos en paralelo para que el escaneo tarde menos de 30 segundos
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: check_port(ip, p), PORTS_TO_SCAN)
        for port in results:
            if port is not None:
                open_ports.append(port)
    return sorted(open_ports)

def main():
    if not TARGET_IP:
        log("ERROR: La variable de entorno TARGET_IP no está configurada.", "CRITICAL")
        sys.exit(1)

    log(f"Iniciando NetWatch-Diff para la IP: {TARGET_IP}")
    log(f"Frecuencia de escaneo: cada {SCAN_INTERVAL_MINS} minutos.")
    
    previous_state = None

    while True:
        log(f"Analizando IP objetivo: {TARGET_IP}...")
        try:
            current_state = scan_ip(TARGET_IP)
        except Exception as e:
            log(f"Error durante el escaneo: {e}", "ERROR")
            time.sleep(60)
            continue

        # Evaluación de estados (El "Diff")
        if previous_state is None:
            # Primer escaneo de la aplicación (Línea base)
            previous_state = current_state
            log(f"[Todo BIEN] - Línea base establecida. Puertos abiertos detectados: {current_state}")
        
        elif current_state == previous_state:
            # El estado actual es idéntico al anterior
            if current_state:
                log(f"[Todo BIEN] - Sin cambios detectados. Puertos abiertos ({len(current_state)}): {current_state}")
            else:
                log(f"[Todo BIEN] - Sin cambios detectados. 0 puertos abiertos.")
        
        else:
            # Hubo una discrepancia entre los últimos dos registros
            new_ports = set(current_state) - set(previous_state)
            closed_ports = set(previous_state) - set(current_state)
            
            log("¡ALERTA DE CAMBIO DETECTADA! [Todo MAL] ⚠️", "WARNING")
            if new_ports:
                log(f"NUEVOS puertos abiertos detectados: {list(new_ports)}", "WARNING")
            if closed_ports:
                log(f"Puertos que se han cerrado: {list(closed_ports)}", "INFO")
            
            # Guardamos el estado actual como el nuevo registro de comparación
            previous_state = current_state

        # Esperar hasta el próximo intervalo
        time.sleep(SCAN_INTERVAL_MINS * 60)

if __name__ == "__main__":
    main()
