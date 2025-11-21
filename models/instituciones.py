from database import db
from sqlalchemy.schema import ForeignKey

class Institucion(db.Model):
    __tablename__ = 'instituciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))

    criterios = db.relationship("Criterio", back_populates="institucion")
