from flask import Blueprint, jsonify, request
from database import db
from models import Evaluacion, EvaluacionDetalle
from datetime import datetime

evaluaciones_bp = Blueprint('evaluaciones', __name__, url_prefix='/evaluaciones')

@evaluaciones_bp.route('/', methods=['GET'])
def listar_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)

@evaluaciones_bp.route('/', methods=['POST'])
def registrar_evaluacion():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Validaciones básicas
    if not data.get('trabajo_id'):
        return jsonify({"error": "El trabajo_id es requerido"}), 400
    if not data.get('evaluador_id'):
        return jsonify({"error": "El evaluador_id es requerido"}), 400
    
    try:
        # 1. Buscar si ya existe la cabecera de evaluación
        evaluacion = Evaluacion.query.filter_by(
            trabajo_id=data.get('trabajo_id'),
            evaluador_id=data.get('evaluador_id')
        ).first()

        # Si no existe, la creamos
        if not evaluacion:
            fecha_evaluacion = datetime.now().date()
            if data.get('fecha_evaluacion'):
                try:
                    fecha_evaluacion = datetime.strptime(data.get('fecha_evaluacion'), '%Y-%m-%d').date()
                except ValueError:
                    pass # Usamos fecha actual si falla

            evaluacion = Evaluacion(
                trabajo_id=data.get('trabajo_id'),
                evaluador_id=data.get('evaluador_id'),
                fecha_evaluacion=fecha_evaluacion,
                nota_final=data.get('nota_final') # Opcional al inicio
            )
            db.session.add(evaluacion)
            db.session.flush() # Para obtener el ID

        # 2. Si vienen datos de detalle (Criterio y Nota), registramos el detalle
        if data.get('criterio_id') and data.get('nota') is not None:
            # Verificar si ya existe calificación para este criterio en esta evaluación
            detalle = EvaluacionDetalle.query.filter_by(
                evaluacion_id=evaluacion.id,
                criterio_id=data.get('criterio_id')
            ).first()

            if detalle:
                # Actualizar existente
                detalle.nota = data.get('nota')
                detalle.comentarios = data.get('observacion') or data.get('comentarios')
            else:
                # Crear nuevo detalle
                detalle = EvaluacionDetalle(
                    evaluacion_id=evaluacion.id,
                    criterio_id=data.get('criterio_id'),
                    nota=data.get('nota'),
                    comentarios=data.get('observacion') or data.get('comentarios')
                )
                db.session.add(detalle)

        db.session.commit()
        return jsonify({
            "mensaje": "Evaluación registrada/actualizada exitosamente", 
            "id": evaluacion.id,
            "detalle_registrado": bool(data.get('criterio_id'))
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar evaluación: {str(e)}"}), 500

# OBTENER UNO POR ID
@evaluaciones_bp.route('/<int:id>', methods=['GET'])
def obtener_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    return jsonify({
        "id": evaluacion.id,
        "trabajo_id": evaluacion.trabajo_id,
        "evaluador_id": evaluacion.evaluador_id,
        "nota_final": float(evaluacion.nota_final) if evaluacion.nota_final else None,
        "comentarios": evaluacion.comentarios,
        "fecha_evaluacion": evaluacion.fecha_evaluacion.isoformat() if evaluacion.fecha_evaluacion else None
    })

# LISTAR POR TRABAJO
@evaluaciones_bp.route('/trabajo/<int:trabajo_id>', methods=['GET'])
def listar_evaluaciones_por_trabajo(trabajo_id):
    evaluaciones = Evaluacion.query.filter_by(trabajo_id=trabajo_id).all()
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)

# LISTAR POR EVALUADOR
@evaluaciones_bp.route('/evaluador/<int:evaluador_id>', methods=['GET'])
def listar_evaluaciones_por_evaluador(evaluador_id):
    evaluaciones = Evaluacion.query.filter_by(evaluador_id=evaluador_id).all()
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)

# ACTUALIZAR COMPLETO (PUT)
@evaluaciones_bp.route('/<int:id>', methods=['PUT'])
def actualizar_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('trabajo_id'):
        return jsonify({"error": "El trabajo_id es requerido"}), 400
    
    evaluacion.trabajo_id = data.get('trabajo_id')
    evaluacion.evaluador_id = data.get('evaluador_id')
    evaluacion.nota_final = data.get('nota_final')
    evaluacion.comentarios = data.get('comentarios')
    
    if data.get('fecha_evaluacion'):
        try:
            evaluacion.fecha_evaluacion = datetime.strptime(data.get('fecha_evaluacion'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluación actualizada exitosamente",
        "id": evaluacion.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@evaluaciones_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_evaluacion_parcial(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'trabajo_id' in data:
        evaluacion.trabajo_id = data.get('trabajo_id')
    if 'evaluador_id' in data:
        evaluacion.evaluador_id = data.get('evaluador_id')
    if 'nota_final' in data:
        evaluacion.nota_final = data.get('nota_final')
    if 'comentarios' in data:
        evaluacion.comentarios = data.get('comentarios')
    if 'fecha_evaluacion' in data:
        if data.get('fecha_evaluacion'):
            try:
                evaluacion.fecha_evaluacion = datetime.strptime(data.get('fecha_evaluacion'), '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
        else:
            evaluacion.fecha_evaluacion = None
    
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluación actualizada exitosamente",
        "id": evaluacion.id
    })

# ELIMINAR
@evaluaciones_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    return jsonify({"mensaje": "Evaluación eliminada exitosamente"})