from database import db

class TipoTrabajo(db.Model):
    __tablename__ = 'tipos_trabajo'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

