from database import db
from sqlalchemy.schema import ForeignKey

# Detalle Evaluación (PK: id, FKs: evaluacion_id, criterio_id, Columnas: nota, subtotal)
class EvaluacionDetalle(db.Model):
    __tablename__ = 'evaluacion_detalle'
    id = db.Column(db.Integer, primary_key=True)
    evaluacion_id = db.Column(db.Integer, ForeignKey('evaluaciones.id'), nullable=False) # FK
    criterio_id = db.Column(db.Integer, ForeignKey('criterios.id'), nullable=False) # FK
    nota = db.Column(db.Numeric(5, 2))
    subtotal = db.Column(db.Numeric(5, 2))