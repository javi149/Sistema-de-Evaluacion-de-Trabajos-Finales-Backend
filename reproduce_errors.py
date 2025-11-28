import unittest
import json
from app import app, db
from models import Trabajo

class TestTrabajoErrors(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # Create tables if not exist (though they should exist in dev)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_create_trabajo_no_tipo(self):
        """Test creating a work without 'tipo' field (simulating frontend)"""
        payload = {
            "titulo": "Tesis de Prueba",
            "resumen": "Resumen de prueba",
            "estudiante_id": 1, # Assuming student 1 exists or validation is loose
            "fecha_entrega": "2025-12-01",
            "duracion_meses": 10,
            "nota_aprobacion": 5.0,
            "requisito": "si"
        }
        response = self.app.post('/trabajos/', json=payload)
        print(f"\nCreate Response Status: {response.status_code}")
        print(f"Create Response Body: {response.get_json()}")
        # Currently expecting 400 because 'tipo' is missing
        if response.status_code == 400:
            print("Confirmed: 400 Error reproduced (Missing 'tipo')")
        else:
            print(f"Unexpected status: {response.status_code}")

    def test_get_trabajos_500(self):
        """Test fetching works to see if 500 occurs"""
        response = self.app.get('/trabajos/')
        print(f"\nGet Response Status: {response.status_code}")
        # Currently expecting 500 if there's bad data or 200 if empty/fine
        if response.status_code == 500:
            print("Confirmed: 500 Error reproduced")
        elif response.status_code == 200:
            print("Get works: Success (No 500 error found yet)")
        else:
            print(f"Unexpected status: {response.status_code}")

if __name__ == '__main__':
    unittest.main()
