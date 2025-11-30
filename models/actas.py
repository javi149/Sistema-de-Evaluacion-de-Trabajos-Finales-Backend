from database import db
from sqlalchemy.schema import ForeignKey
import enum

# Definimos los estados posibles como un Enum de Python
class EstadoActa(enum.Enum):
    APROBADO = 'APROBADO'
    REPROBADO = 'REPROBADO'
    PENDIENTE = 'PENDIENTE'

class Acta(db.Model):
    __tablename__ = 'actas'
    
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, ForeignKey('trabajos.id'), nullable=False)
    
    fecha = db.Column(db.DateTime)
    url_pdf = db.Column(db.String(255))
    
    # Estado usando Enum de SQLAlchemy
    # native_enum=False hace que funcione en SQLite (usa VARCHAR)
    # En MySQL/PostgreSQL usará ENUM nativo para mejor rendimiento
    estado = db.Column(db.Enum(EstadoActa, native_enum=False, length=20))