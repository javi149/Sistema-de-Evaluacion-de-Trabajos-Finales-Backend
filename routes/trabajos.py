from flask import Blueprint, jsonify, request
from database import db
from models import Trabajo
from datetime import datetime

trabajos_bp = Blueprint('trabajos', __name__, url_prefix='/trabajos')

# LISTAR TODOS
@trabajos_bp.route('/', methods=['GET'])
def listar_trabajos():
    trabajos = Trabajo.query.all()
    resultado = [{
        "id": t.id, 
        "titulo": t.titulo,
        "tipo_id": t.tipo_id,
        "duracion_meses": t.duracion_meses,
        "nota_aprobacion": float(t.nota_aprobacion) if t.nota_aprobacion else None,
        "requisito_aprobacion": t.requisito_aprobacion,
        "resumen": t.resumen,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
        "estudiante_id": t.estudiante_id
    } for t in trabajos]
    return jsonify(resultado)

# OBTENER UNO POR ID
@trabajos_bp.route('/<int:id>', methods=['GET'])
def obtener_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    return jsonify({
        "id": trabajo.id,
        "titulo": trabajo.titulo,
        "tipo_id": trabajo.tipo_id,
        "duracion_meses": trabajo.duracion_meses,
        "nota_aprobacion": float(trabajo.nota_aprobacion) if trabajo.nota_aprobacion else None,
        "requisito_aprobacion": trabajo.requisito_aprobacion,
        "resumen": trabajo.resumen,
        "fecha_entrega": trabajo.fecha_entrega.isoformat() if trabajo.fecha_entrega else None,
        "estudiante_id": trabajo.estudiante_id
    })

# CREAR
@trabajos_bp.route('/', methods=['POST'])
def crear_trabajo():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('titulo'):
        return jsonify({"error": "El título es requerido"}), 400
    
    fecha_entrega = None
    if data.get('fecha_entrega'):
        try:
            fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    nuevo = Trabajo(
        titulo=data.get('titulo'),
        tipo_id=data.get('tipo_id'),
        duracion_meses=data.get('duracion_meses'),
        nota_aprobacion=data.get('nota_aprobacion'),
        requisito_aprobacion=data.get('requisito_aprobacion'),
        resumen=data.get('resumen'),
        fecha_entrega=fecha_entrega,
        estudiante_id=data.get('estudiante_id')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "mensaje": "Trabajo registrado exitosamente",
        "id": nuevo.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@trabajos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('titulo'):
        return jsonify({"error": "El título es requerido"}), 400
    
    trabajo.titulo = data.get('titulo')
    trabajo.tipo_id = data.get('tipo_id')
    trabajo.duracion_meses = data.get('duracion_meses')
    trabajo.nota_aprobacion = data.get('nota_aprobacion')
    trabajo.requisito_aprobacion = data.get('requisito_aprobacion')
    trabajo.resumen = data.get('resumen')
    trabajo.estudiante_id = data.get('estudiante_id')
    
    if data.get('fecha_entrega'):
        try:
            trabajo.fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    else:
        trabajo.fecha_entrega = None
    
    db.session.commit()
    return jsonify({
        "mensaje": "Trabajo actualizado exitosamente",
        "id": trabajo.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@trabajos_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_trabajo_parcial(id):
    trabajo = Trabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'titulo' in data:
        trabajo.titulo = data.get('titulo')
    if 'tipo_id' in data:
        trabajo.tipo_id = data.get('tipo_id')
    if 'duracion_meses' in data:
        trabajo.duracion_meses = data.get('duracion_meses')
    if 'nota_aprobacion' in data:
        trabajo.nota_aprobacion = data.get('nota_aprobacion')
    if 'requisito_aprobacion' in data:
        trabajo.requisito_aprobacion = data.get('requisito_aprobacion')
    if 'resumen' in data:
        trabajo.resumen = data.get('resumen')
    if 'estudiante_id' in data:
        trabajo.estudiante_id = data.get('estudiante_id')
    if 'fecha_entrega' in data:
        if data.get('fecha_entrega'):
            try:
                trabajo.fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
        else:
            trabajo.fecha_entrega = None
    
    db.session.commit()
    return jsonify({
        "mensaje": "Trabajo actualizado exitosamente",
        "id": trabajo.id
    })

# ELIMINAR
@trabajos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    db.session.delete(trabajo)
    db.session.commit()
    return jsonify({"mensaje": "Trabajo eliminado exitosamente"})
