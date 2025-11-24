from database import db

class Criterio(db.Model):
    __tablename__ = 'criterios'

    id = db.Column(db.Integer, primary_key=True)
    # Si antes usabas ForeignKey('instituciones.id'), cámbialo a un entero simple o bórralo si ya no sirve.
    # Para que no falle, lo dejamos como Integer simple (sin conectar a nada).
    institucion_id = db.Column(db.Integer, nullable=True) 
    
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    ponderacion = db.Column(db.Float)