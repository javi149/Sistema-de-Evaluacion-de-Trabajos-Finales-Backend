from database import db
from sqlalchemy.schema import ForeignKey
from datetime import datetime

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nota_final = db.Column(db.Numeric(4, 2))
    comentarios = db.Column(db.Text)
    
    # Agregué esto porque salía en tu imagen de la BD y sirve para el Acta
    fecha_evaluacion = db.Column(db.Date, default=datetime.utcnow)

    # Claves Foráneas
    trabajo_id = db.Column(db.Integer, ForeignKey('trabajos.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, ForeignKey('evaluadores.id'))

    # NOTA: Gracias a los 'relationship' en los otros archivos,
    # aquí ya puedes usar "self.trabajo" o "self.evaluador" automáticamente.
