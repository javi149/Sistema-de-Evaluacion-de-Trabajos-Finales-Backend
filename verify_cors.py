import urllib.request
import urllib.error
from flask import Flask
from flask_cors import CORS
import threading
import time
import sys
import os

# Agregar la raíz del proyecto al path para importar app
sys.path.append(os.getcwd())

try:
    from app import crear_app
except ImportError:
    print("No se pudo importar app. Asegúrate de estar en la raíz del proyecto.")
    sys.exit(1)

def ejecutar_servidor(app):
    # Suprimir banner de flask
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(port=5001, use_reloader=False)

def verificar_cors():
    # Iniciar servidor en un hilo
    app = crear_app()
    hilo_servidor = threading.Thread(target=ejecutar_servidor, args=(app,))
    hilo_servidor.daemon = True
    hilo_servidor.start()
    
    # Esperar a que el servidor inicie
    time.sleep(2)
    
    url_base = "http://localhost:5001"
    
    print("--- Verificando CORS ---")
    
    # Probar petición OPTIONS (Preflight)
    print("\nProbando petición OPTIONS...")
    try:
        req = urllib.request.Request(f"{url_base}/estudiantes/", method="OPTIONS")
        req.add_header("Origin", "http://localhost:3000")
        req.add_header("Access-Control-Request-Method", "GET")
        req.add_header("Access-Control-Request-Headers", "Content-Type")
        
        with urllib.request.urlopen(req) as response:
            print(f"Código de Estado: {response.status}")
            print("Encabezados:")
            headers = response.info()
            for k, v in headers.items():
                if "Access-Control" in k:
                    print(f"  {k}: {v}")
            
            if response.status == 200 and "Access-Control-Allow-Origin" in headers:
                print("Petición exitosa")
            else:
                print("Petición fallida")
            
    except urllib.error.HTTPError as e:
        print(f"Error probando : {e}")
    except Exception as e:
        print(f"Error probando : {e}")

    # Probar petición GET
    print("\nProbando petición GET...")
    try:
        req = urllib.request.Request(f"{url_base}/estudiantes/", method="GET")
        req.add_header("Origin", "http://localhost:3000")
        
        with urllib.request.urlopen(req) as response:
            print(f"Código de Estado: {response.status}")
            print("Encabezados:")
            headers = response.info()
            for k, v in headers.items():
                if "Access-Control" in k:
                    print(f"  {k}: {v}")
                
            if "Access-Control-Allow-Origin" in headers:
                print("Petición GET tiene encabezados CORS")
            else:
                print("Petición GET le faltan encabezados CORS")

    except urllib.error.HTTPError as e:
        print(f"Error probando GET: {e}")
    except Exception as e:
        print(f"Error probando GET: {e}")

if __name__ == "__main__":
    verificar_cors()
