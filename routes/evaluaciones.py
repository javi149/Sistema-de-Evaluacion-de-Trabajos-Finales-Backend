from flask import Blueprint, jsonify, request
from app import db
from models import Evaluacion

evaluaciones_bp = Blueprint('evaluaciones', __name__, url_prefix='/evaluaciones')

@evaluaciones_bp.route('/', methods=['POST'])
def registrar_evaluacion():
    data = request.get_json()
    

    nueva = Evaluacion(
        trabajo_id=data.get('trabajo_id'),
        evaluador_id=data.get('evaluador_id'),
        nota_final=data.get('nota_final'),
        comentarios=data.get('comentarios')
    )
    
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Evaluación registrada", "id": nueva.evaluaciones_id}), 201
