from database import db

# Evaluadores (PK: id, Columnas: nombre, email)
class Evaluador(db.Model):
    __tablename__ = 'evaluadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True)