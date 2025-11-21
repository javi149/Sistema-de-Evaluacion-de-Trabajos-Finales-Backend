from database import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    
    # Columnas basadas en tu imagen:
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(255))
    rut = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    carrera = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rut': self.rut,
            'email': self.email,
            'carrera': self.carrera
        }