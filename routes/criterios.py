from flask import Blueprint, jsonify, request
from database import db
from models import Criterio

criterios_bp = Blueprint('criterios', __name__, url_prefix='/criterios')

@criterios_bp.route('/', methods=['GET'])
def listar_criterios():
    lista = Criterio.query.all()
  
    resultado = [{
        "id": c.id,
        "institucion_id": c.institucion_id,
        "nombre": c.nombre,
        "descripcion": c.descripcion,
        "ponderacion": float(c.ponderacion) if c.ponderacion else None
    } for c in lista]
    return jsonify(resultado)

@criterios_bp.route('/', methods=['POST'])
def crear_criterio():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nuevo = Criterio(
        institucion_id=data.get('institucion_id'),
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        ponderacion=data.get('ponderacion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Criterio configurado exitosamente", "id": nuevo.id}), 201
