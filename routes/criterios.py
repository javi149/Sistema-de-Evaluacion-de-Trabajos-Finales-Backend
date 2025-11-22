from flask import Blueprint, jsonify, request
from app import db
from models import Criterio

criterios_bp = Blueprint('criterios', __name__, url_prefix='/criterios')

@criterios_bp.route('/', methods=['GET'])
def listar_criterios():
    lista = Criterio.query.all()
  
    resultado = [{
        "id": c.criterios_id, 
        "nombre": c.nombre, 
        "ponderacion": str(c.ponderacion) 
    } for c in lista]
    return jsonify(resultado)

@criterios_bp.route('/', methods=['POST'])
def crear_criterio():
    data = request.get_json()
    nuevo = Criterio(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        ponderacion=data.get('ponderacion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Criterio configurado", "id": nuevo.criterios_id}), 201
