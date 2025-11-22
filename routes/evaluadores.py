from flask import Blueprint, jsonify, request
from app import db
from models import Evaluador

evaluadores_bp = Blueprint('evaluadores', __name__, url_prefix='/evaluadores')

@evaluadores_bp.route('/', methods=['GET'])
def listar_evaluadores():
    evaluadores = Evaluador.query.all()
    resultado = [{
        "id": e.evaluadores_id, 
        "nombre": e.nombre, 
        "email": e.email,
        "rol": e.rol,  # Tutor, Jurado
        "tipo": e.tipo # Interno, Externo
    } for e in evaluadores]
    return jsonify(resultado)

@evaluadores_bp.route('/', methods=['POST'])
def crear_evaluador():
    data = request.get_json()
    nuevo = Evaluador(
        nombre=data.get('nombre'),
        email=data.get('email'),
        rol=data.get('rol'),
        tipo=data.get('tipo')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Evaluador creado", "id": nuevo.evaluadores_id}), 201
