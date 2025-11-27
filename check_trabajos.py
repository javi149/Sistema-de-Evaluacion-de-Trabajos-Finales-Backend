from app import create_app
from database import db
from models.trabajos import Trabajo

app = create_app()

with app.app_context():
    trabajos = Trabajo.query.all()
    print(f"Total trabajos: {len(trabajos)}")
    for t in trabajos:
        print(f"ID: {t.id}, Titulo: {t.titulo}, Estudiante ID: {t.estudiante_id}")
