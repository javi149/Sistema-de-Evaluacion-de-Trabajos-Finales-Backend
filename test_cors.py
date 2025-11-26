"""
Script para probar CORS con peticiones POST/PUT/DELETE
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"
# BASE_URL = "https://sistema-de-evaluacion-de-trabajos-finales-production.up.railway.app"

def test_cors_get():
    """Prueba petición GET"""
    print("\n" + "="*60)
    print("TEST 1: GET /estudiantes/")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/estudiantes/")
    print(f"Status Code: {response.status_code}")
    print(f"CORS Headers:")
    print(f"  - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    print(f"  - Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods')}")
    print(f"  - Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers')}")
    print(f"Response: {response.json()[:2] if response.json() else 'Empty'}")  # Primeros 2 elementos

def test_cors_options():
    """Prueba petición OPTIONS (preflight)"""
    print("\n" + "="*60)
    print("TEST 2: OPTIONS /estudiantes/ (Preflight)")
    print("="*60)
    
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    response = requests.options(f"{BASE_URL}/estudiantes/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"CORS Headers:")
    print(f"  - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    print(f"  - Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods')}")
    print(f"  - Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers')}")
    print(f"  - Access-Control-Max-Age: {response.headers.get('Access-Control-Max-Age')}")

def test_cors_post():
    """Prueba petición POST"""
    print("\n" + "="*60)
    print("TEST 3: POST /estudiantes/")
    print("="*60)
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
    }
    
    data = {
        "nombre": "Test CORS",
        "apellido": "Usuario",
        "rut": "11111111-1",
        "email": "test@cors.com",
        "carrera": "Ingeniería de Pruebas"
    }
    
    response = requests.post(f"{BASE_URL}/estudiantes/", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"CORS Headers:")
    print(f"  - Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("\n🔍 PRUEBAS DE CORS")
    print("="*60)
    
    try:
        test_cors_get()
        test_cors_options()
        test_cors_post()
        
        print("\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60)
        print("\nSi todas las pruebas muestran 'Access-Control-Allow-Origin: *',")
        print("entonces CORS está configurado correctamente.")
        print("\nPara probar en Railway, cambia BASE_URL en el script.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nAsegúrate de que el servidor esté corriendo en", BASE_URL)
