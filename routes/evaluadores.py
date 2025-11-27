from flask import Blueprint, jsonify, request
from database import db
from models import Evaluador
from factories.evaluador_factory import EvaluadorFactory

evaluadores_bp = Blueprint('evaluadores', __name__, url_prefix='/evaluadores')

# LISTAR TODOS
@evaluadores_bp.route('/', methods=['GET'])
def listar_evaluadores():
    evaluadores = Evaluador.query.all()
    resultado = [{
        "id": e.id, 
        "nombre": e.nombre, 
        "email": e.email,
        "rol": e.rol,
        "tipo": e.tipo
    } for e in evaluadores]
    return jsonify(resultado)

# OBTENER UNO POR ID
@evaluadores_bp.route('/<int:id>', methods=['GET'])
def obtener_evaluador(id):
    evaluador = Evaluador.query.get_or_404(id)
    return jsonify({
        "id": evaluador.id,
        "nombre": evaluador.nombre,
        "email": evaluador.email,
        "rol": evaluador.rol,
        "tipo": evaluador.tipo
    })

# CREAR (POST) - CON DEBUGGING
@evaluadores_bp.route('/', methods=['POST'])
def crear_evaluador():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400
        
        # Validamos datos mínimos
        if not data.get('nombre') or not data.get('tipo'):
            return jsonify({"error": "El nombre y el tipo (guia, comision, informante) son requeridos"}), 400
        
        # Factory
        perfil = EvaluadorFactory.crear_perfil(data.get('tipo'))
        
        if not perfil:
            return jsonify({"error": "Tipo de evaluador inválido. Use: guia, comision, informante"}), 400
        
        # Crear Objeto
        nuevo = Evaluador(
            nombre=data.get('nombre'),
            email=data.get('email'),
            rol=perfil['rol'],
            tipo=perfil['tipo_oficial'] # CORREGIDO: Usar 'tipo_oficial' que es lo que devuelve la fábrica
        )
        
        db.session.add(nuevo)
        db.session.commit()
        
        return jsonify({
            "mensaje": "Evaluador creado exitosamente",
            "perfil_asignado": perfil,
            "id": nuevo.id
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# ACTUALIZAR COMPLETO (PUT)
@evaluadores_bp.route('/<int:id>', methods=['PUT'])
def actualizar_evaluador(id):
    evaluador = Evaluador.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    if data.get('tipo'):
        perfil = EvaluadorFactory.crear_perfil(data.get('tipo'))
        if perfil:
            evaluador.rol = perfil['rol']
            evaluador.tipo = perfil['tipo_oficial'] # CORREGIDO TAMBIÉN AQUÍ
    
    if data.get('nombre'):
        evaluador.nombre = data.get('nombre')
    if data.get('email'):
        evaluador.email = data.get('email')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluador actualizado exitosamente",
        "rol_actual": evaluador.rol,
        "id": evaluador.id
    })

# ELIMINAR
@evaluadores_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_evaluador(id):
    evaluador = Evaluador.query.get_or_404(id)
    db.session.delete(evaluador)
    db.session.commit()
    return jsonify({"mensaje": "Evaluador eliminado exitosamente"})

# OBTENER EVALUACIONES DE UN EVALUADOR
@evaluadores_bp.route('/<int:id>/evaluaciones', methods=['GET'])
def obtener_evaluaciones_evaluador(id):
    evaluador = Evaluador.query.get_or_404(id)
    evaluaciones = evaluador.evaluaciones_realizadas if hasattr(evaluador, 'evaluaciones_realizadas') else []
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)