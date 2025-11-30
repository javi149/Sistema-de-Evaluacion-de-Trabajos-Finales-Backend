import urllib.request
import urllib.error
import sys

def verificar_servidor():
    url = "http://localhost:5000/ping"
    print(f"Verificando conexión a {url}...")
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status == 200:
                print("[OK] ¡El servidor está FUNCIONANDO y es accesible!")
                print(f"Respuesta: {response.read().decode('utf-8')}")
                return True
            else:
                print(f"[AVISO] El servidor respondió con código de estado: {response.status}")
                return False
    except urllib.error.URLError as e:
        print(f"[ERROR] No se pudo conectar al servidor: {e}")
        print("-> ¡Asegúrate de estar ejecutando 'python app.py' en una terminal separada!")
        return False
    except Exception as e:
        print(f"[ERROR] Ocurrió un error: {e}")
        return False

if __name__ == "__main__":
    exito = verificar_servidor()
    if not exito:
        sys.exit(1)
