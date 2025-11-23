from database import db
from sqlalchemy.schema import ForeignKey
# Importamos Enum si tu base de datos soporta ENUM, si no, usa String
from sqlalchemy.dialects.mysql import ENUM 

class Acta(db.Model):
    __tablename__ = 'actas'
    
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, ForeignKey('trabajos.id'), nullable=False)
    
    fecha = db.Column(db.DateTime)
    url_pdf = db.Column(db.String(255))
    
    # Estado como ENUM (Aprobado/Reprobado/Pendiente)
    estado = db.Column(ENUM('APROBADO', 'REPROBADO', 'PENDIENTE'))
