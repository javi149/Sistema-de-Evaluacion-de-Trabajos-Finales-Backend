from database import db

class Evaluador(db.Model):
    __tablename__ = 'evaluadores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True)

    # --- RELACIÓN AGREGADA ---
    # Permite ver todas las notas que ha puesto este profe
    evaluaciones_realizadas = db.relationship('Evaluacion', backref='evaluador', lazy=True)