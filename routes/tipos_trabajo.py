from flask import Blueprint, jsonify, request
from database import db
from models import TipoTrabajo

tipos_trabajo_bp = Blueprint('tipos_trabajo', __name__, url_prefix='/tipos-trabajo')

# LISTAR TODOS
@tipos_trabajo_bp.route('/', methods=['GET'])
def listar_tipos_trabajo():
    tipos = TipoTrabajo.query.all()
    resultado = [{
        "id": t.id,
        "nombre": t.nombre,
        "descripcion": t.descripcion
    } for t in tipos]
    return jsonify(resultado)

# OBTENER UNO POR ID
@tipos_trabajo_bp.route('/<int:id>', methods=['GET'])
def obtener_tipo_trabajo(id):
    tipo = TipoTrabajo.query.get_or_404(id)
    return jsonify({
        "id": tipo.id,
        "nombre": tipo.nombre,
        "descripcion": tipo.descripcion
    })

# CREAR
@tipos_trabajo_bp.route('/', methods=['POST'])
def crear_tipo_trabajo():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nuevo = TipoTrabajo(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "mensaje": "Tipo de trabajo creado exitosamente",
        "id": nuevo.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@tipos_trabajo_bp.route('/<int:id>', methods=['PUT'])
def actualizar_tipo_trabajo(id):
    tipo = TipoTrabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    tipo.nombre = data.get('nombre')
    tipo.descripcion = data.get('descripcion')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Tipo de trabajo actualizado exitosamente",
        "id": tipo.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@tipos_trabajo_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_tipo_trabajo_parcial(id):
    tipo = TipoTrabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'nombre' in data:
        tipo.nombre = data.get('nombre')
    if 'descripcion' in data:
        tipo.descripcion = data.get('descripcion')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Tipo de trabajo actualizado exitosamente",
        "id": tipo.id
    })

# ELIMINAR
@tipos_trabajo_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_tipo_trabajo(id):
    tipo = TipoTrabajo.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    return jsonify({"mensaje": "Tipo de trabajo eliminado exitosamente"})

