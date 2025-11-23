from flask import Blueprint, jsonify, request
from database import db
from models import Evaluacion
from datetime import datetime

evaluaciones_bp = Blueprint('evaluaciones', __name__, url_prefix='/evaluaciones')

@evaluaciones_bp.route('/', methods=['GET'])
def listar_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": e.nota_final,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)

@evaluaciones_bp.route('/', methods=['POST'])
def registrar_evaluacion():
    data = request.get_json()
    
    fecha_evaluacion = None
    if data.get('fecha_evaluacion'):
        fecha_evaluacion = datetime.strptime(data.get('fecha_evaluacion'), '%Y-%m-%d').date()
    elif not fecha_evaluacion:
        fecha_evaluacion = datetime.now().date()
    
    nueva = Evaluacion(
        trabajo_id=data.get('trabajo_id'),
        evaluador_id=data.get('evaluador_id'),
        nota_final=data.get('nota_final'),
        comentarios=data.get('comentarios'),
        fecha_evaluacion=fecha_evaluacion
    )
    
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Evaluación registrada", "id": nueva.id}), 201
