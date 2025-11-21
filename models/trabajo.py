from database import db

class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    tipo = db.Column(db.String(100)) # Tesis, Proyecto, Seminario
    
    # --- CORREGIDO: Ahora los nombres coinciden con la BD ---
    duracion_meses = db.Column(db.Integer) # ANTES DECÍA "duracion"
    nota_aprobacion = db.Column(db.Float) 
    requisito = db.Column(db.String(200))
    # -------------------------------------------------------
    
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'))
