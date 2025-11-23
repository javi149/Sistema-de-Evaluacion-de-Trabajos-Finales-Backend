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
        "tipo": t.tipo,
        "estado": t.estado,
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
        "tipo": trabajo.tipo,
        "estado": trabajo.estado,
        "fecha_entrega": trabajo.fecha_entrega.isoformat() if trabajo.fecha_entrega else None,
        "estudiante_id": trabajo.estudiante_id
    })

# CREAR
@trabajos_bp.route('/', methods=['POST'])
def crear_trabajo():
    data = request.get_json()
    
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
        tipo=data.get('tipo'),  # Tesis, Proyecto, etc.
        estado=data.get('estado', 'PENDIENTE'),  # Valor inicial por defecto
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
    
    if not data.get('titulo'):
        return jsonify({"error": "El título es requerido"}), 400
    
    trabajo.titulo = data.get('titulo')
    trabajo.tipo = data.get('tipo')
    trabajo.estado = data.get('estado', 'PENDIENTE')
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
    
    if 'titulo' in data:
        trabajo.titulo = data.get('titulo')
    if 'tipo' in data:
        trabajo.tipo = data.get('tipo')
    if 'estado' in data:
        trabajo.estado = data.get('estado')
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
