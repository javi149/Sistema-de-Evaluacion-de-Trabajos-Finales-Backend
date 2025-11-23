from database import db
from sqlalchemy.schema import ForeignKey

# Evaluaciones (PK: id, FKs: trabajo_id, evaluador_id, Columnas: nota_final, comentarios)
class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, ForeignKey('trabajos.id'), nullable=False) # FK
    evaluador_id = db.Column(db.Integer, ForeignKey('evaluadores.id')) # FK
    nota_final = db.Column(db.Numeric(4, 2))
    comentarios = db.Column(db.Text)