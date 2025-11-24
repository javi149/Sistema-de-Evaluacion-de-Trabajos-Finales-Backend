from database import db

class EvaluacionDetalle(db.Model):
    __tablename__ = 'evaluacion_detalles'

    id = db.Column(db.Integer, primary_key=True)
    
    # Claves foráneas
    evaluacion_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.id'), nullable=False)
    criterio_id = db.Column(db.Integer, db.ForeignKey('criterios.id'), nullable=False)

    # Datos de la calificación
    nota = db.Column(db.Float, nullable=False)
    comentarios = db.Column(db.Text, nullable=True)

    # Relaciones (Formato vertical para evitar errores)
    criterio = db.relationship(
        'Criterio', 
        backref=db.backref('detalles_evaluacion', lazy=True)
    )
    
    evaluacion = db.relationship(
        'Evaluacion', 
        backref=db.backref('detalles', lazy=True)
    )

    def __init__(self, evaluacion_id, criterio_id, nota, comentarios=None):
        self.evaluacion_id = evaluacion_id
        self.criterio_id = criterio_id
        self.nota = nota
        self.comentarios = comentarios