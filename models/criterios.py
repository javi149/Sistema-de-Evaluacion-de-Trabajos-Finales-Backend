from database import db
from sqlalchemy.schema import ForeignKey

# Criterios (PK: id, FK: institucion_id, Columnas: nombre, descripcion, ponderacion)
class Criterio(db.Model):
    __tablename__ = 'criterios'

    id = db.Column(db.Integer, primary_key=True)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id'))
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    ponderacion = db.Column(db.Numeric(5, 2))

    institucion = db.relationship("Institucion", back_populates="criterios")
    detalles = db.relationship("EvaluacionDetalle", back_populates="criterio")