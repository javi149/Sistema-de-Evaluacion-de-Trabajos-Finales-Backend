from database import db
from sqlalchemy.schema import ForeignKey

# Columna: titulo, tipo_id (FK), estudiante_id (FK), resumen, fecha_entrega
class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    duracion_meses = db.Column(db.Integer)
    nota_aprobacion = db.Column(db.Float)
    requisito_aprobacion = db.Column(db.String(255))
    
    # Relaciones (Foreign Keys)
    tipo_id = db.Column(db.Integer, ForeignKey('tipos_trabajo.id'))
    estudiante_id = db.Column(db.Integer, ForeignKey('estudiantes.id'))

    resumen = db.Column(db.Text)
    fecha_entrega = db.Column(db.Date)