from database import db
from sqlalchemy.schema import ForeignKey

class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text)
    fecha_entrega = db.Column(db.Date)
    
    # Claves Foráneas (Conexiones ID)
    tipo_id = db.Column(db.Integer, ForeignKey('tipos_trabajo.id'))
    estudiante_id = db.Column(db.Integer, ForeignKey('estudiantes.id'))

    # --- RELACIÓN AGREGADA ---
    # Esto permite hacer "trabajo.evaluaciones" en tu ActaHTML
    evaluaciones = db.relationship('Evaluacion', backref='trabajo', lazy=True)