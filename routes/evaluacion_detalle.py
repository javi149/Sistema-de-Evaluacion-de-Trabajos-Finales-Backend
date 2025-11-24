from flask import Blueprint, jsonify, request
from database import db
from models import EvaluacionDetalle

evaluacion_detalle_bp = Blueprint('evaluacion_detalle', __name__, url_prefix='/evaluacion-detalle')

# LISTAR TODOS
@evaluacion_detalle_bp.route('/', methods=['GET'])
def listar_evaluacion_detalles():
    detalles = EvaluacionDetalle.query.all()
    resultado = [{
        "id": d.id,
        "evaluacion_id": d.evaluacion_id,
        "criterio_id": d.criterio_id,
        "nota": d.nota,
        "comentarios": d.comentarios
    } for d in detalles]
    return jsonify(resultado)

# OBTENER UNO POR ID
@evaluacion_detalle_bp.route('/<int:id>', methods=['GET'])
def obtener_evaluacion_detalle(id):
    detalle = EvaluacionDetalle.query.get_or_404(id)
    return jsonify({
        "id": detalle.id,
        "evaluacion_id": detalle.evaluacion_id,
        "criterio_id": detalle.criterio_id,
        "nota": detalle.nota,
        "comentarios": detalle.comentarios
    })

# LISTAR POR EVALUACION
@evaluacion_detalle_bp.route('/evaluacion/<int:evaluacion_id>', methods=['GET'])
def listar_detalles_por_evaluacion(evaluacion_id):
    detalles = EvaluacionDetalle.query.filter_by(evaluacion_id=evaluacion_id).all()
    resultado = [{
        "id": d.id,
        "evaluacion_id": d.evaluacion_id,
        "criterio_id": d.criterio_id,
        "nota": d.nota,
        "comentarios": d.comentarios
    } for d in detalles]
    return jsonify(resultado)

# CREAR
@evaluacion_detalle_bp.route('/', methods=['POST'])
def crear_evaluacion_detalle():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('evaluacion_id'):
        return jsonify({"error": "El evaluacion_id es requerido"}), 400
    if not data.get('criterio_id'):
        return jsonify({"error": "El criterio_id es requerido"}), 400
    if data.get('nota') is None:
        return jsonify({"error": "La nota es requerida"}), 400
    
    nuevo = EvaluacionDetalle(
        evaluacion_id=data.get('evaluacion_id'),
        criterio_id=data.get('criterio_id'),
        nota=data.get('nota'),
        comentarios=data.get('comentarios')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "mensaje": "Detalle de evaluación creado exitosamente",
        "id": nuevo.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@evaluacion_detalle_bp.route('/<int:id>', methods=['PUT'])
def actualizar_evaluacion_detalle(id):
    detalle = EvaluacionDetalle.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('evaluacion_id'):
        return jsonify({"error": "El evaluacion_id es requerido"}), 400
    if not data.get('criterio_id'):
        return jsonify({"error": "El criterio_id es requerido"}), 400
    if data.get('nota') is None:
        return jsonify({"error": "La nota es requerida"}), 400
    
    detalle.evaluacion_id = data.get('evaluacion_id')
    detalle.criterio_id = data.get('criterio_id')
    detalle.nota = data.get('nota')
    detalle.comentarios = data.get('comentarios')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Detalle de evaluación actualizado exitosamente",
        "id": detalle.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@evaluacion_detalle_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_evaluacion_detalle_parcial(id):
    detalle = EvaluacionDetalle.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'evaluacion_id' in data:
        detalle.evaluacion_id = data.get('evaluacion_id')
    if 'criterio_id' in data:
        detalle.criterio_id = data.get('criterio_id')
    if 'nota' in data:
        detalle.nota = data.get('nota')
    if 'comentarios' in data:
        detalle.comentarios = data.get('comentarios')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Detalle de evaluación actualizado exitosamente",
        "id": detalle.id
    })

# ELIMINAR
@evaluacion_detalle_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_evaluacion_detalle(id):
    detalle = EvaluacionDetalle.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"mensaje": "Detalle de evaluación eliminado exitosamente"})

