import unittest
import json
from app import app, db


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

    def test_create_and_delete_trabajo(self):
        """Test creating a work and then deleting it"""
        # 1. Create
        payload = {
            "titulo": "Tesis de Prueba Exitosa",
            "resumen": "Resumen de prueba exitosa",
            "estudiante_id": 1, 
            "tipo_id": 1, # Assuming type 1 exists
            "fecha_entrega": "2025-12-01"
        }
        response = self.app.post('/trabajos/', json=payload)
        print(f"\nCreate Response Status: {response.status_code}")
        print(f"Create Response Body: {response.get_json()}")
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        trabajo_id = data['id']
        print(f"Created Trabajo ID: {trabajo_id}")

        # 2. Delete
        response_delete = self.app.delete(f'/trabajos/{trabajo_id}')
        print(f"Delete Response Status: {response_delete.status_code}")
        print(f"Delete Response Body: {response_delete.get_json()}")
        
        self.assertEqual(response_delete.status_code, 200)
        print("Delete successful (No 500 error)")

if __name__ == '__main__':
    unittest.main()
