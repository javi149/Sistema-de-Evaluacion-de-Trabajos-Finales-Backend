from database import db

class Criterio(db.Model):
    __tablename__ = 'criterios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    ponderacion = db.Column(db.Float)