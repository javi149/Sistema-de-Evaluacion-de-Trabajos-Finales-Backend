from database import db
from sqlalchemy.schema import ForeignKey

class Trabajo(db.Model):
    __tablename__ = 'trabajos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    duracion_meses = db.Column(db.Integer)
    nota_aprobacion = db.Column(db.Float)
    requisito_aprobacion = db.Column(db.String(255))
    
    resumen = db.Column(db.Text)
    fecha_entrega = db.Column(db.Date)
    
    # Nuevo campo estado
    estado = db.Column(db.String(50), default='pendiente') # pendiente, aprobado, rechazado, etc.

    # Claves Foráneas
    tipo_id = db.Column(db.Integer, ForeignKey('tipos_trabajo.id'))
    estudiante_id = db.Column(db.Integer, ForeignKey('estudiantes.id'))

    # --- RELACIÓN PARA LAS ACTAS ---
    evaluaciones = db.relationship('Evaluacion', backref='trabajo', lazy=True, cascade="all, delete-orphan")