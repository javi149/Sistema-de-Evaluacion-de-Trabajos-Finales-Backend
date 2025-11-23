from flask import Blueprint, jsonify, request
from database import db
from models import Evaluacion

evaluaciones_bp = Blueprint('evaluaciones', __name__, url_prefix='/evaluaciones')

@evaluaciones_bp.route('/', methods=['GET'])
def listar_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios
    } for e in evaluaciones]
    return jsonify(resultado)

@evaluaciones_bp.route('/', methods=['POST'])
def registrar_evaluacion():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Validaciones
    if not data.get('trabajo_id'):
        return jsonify({"error": "El trabajo_id es requerido"}), 400
    
    nueva = Evaluacion(
        trabajo_id=data.get('trabajo_id'),
        evaluador_id=data.get('evaluador_id'),
        nota_final=data.get('nota_final'),
        comentarios=data.get('comentarios')
    )
    
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Evaluación registrada exitosamente", "id": nueva.id}), 201
