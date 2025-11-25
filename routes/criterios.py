from flask import Blueprint, jsonify, request
from database import db
from models import Criterio

criterios_bp = Blueprint('criterios', __name__, url_prefix='/criterios')

@criterios_bp.route('/', methods=['GET'])
def listar_criterios():
    lista = Criterio.query.all()
  
    resultado = [{
        "id": c.id,
        "institucion_id": c.institucion_id,
        "nombre": c.nombre,
        "descripcion": c.descripcion,
        "ponderacion": float(c.ponderacion) if c.ponderacion else None
    } for c in lista]
    return jsonify(resultado)

@criterios_bp.route('/', methods=['POST'])
def crear_criterio():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nuevo = Criterio(
        institucion_id=data.get('institucion_id'),
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        ponderacion=data.get('ponderacion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Criterio configurado exitosamente", "id": nuevo.id}), 201

# OBTENER UNO POR ID
@criterios_bp.route('/<int:id>', methods=['GET'])
def obtener_criterio(id):
    criterio = Criterio.query.get_or_404(id)
    return jsonify({
        "id": criterio.id,
        "institucion_id": criterio.institucion_id,
        "nombre": criterio.nombre,
        "descripcion": criterio.descripcion,
        "ponderacion": float(criterio.ponderacion) if criterio.ponderacion else None
    })

# ACTUALIZAR COMPLETO (PUT)
@criterios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_criterio(id):
    criterio = Criterio.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    criterio.institucion_id = data.get('institucion_id')
    criterio.nombre = data.get('nombre')
    criterio.descripcion = data.get('descripcion')
    criterio.ponderacion = data.get('ponderacion')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Criterio actualizado exitosamente",
        "id": criterio.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@criterios_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_criterio_parcial(id):
    criterio = Criterio.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'institucion_id' in data:
        criterio.institucion_id = data.get('institucion_id')
    if 'nombre' in data:
        criterio.nombre = data.get('nombre')
    if 'descripcion' in data:
        criterio.descripcion = data.get('descripcion')
    if 'ponderacion' in data:
        criterio.ponderacion = data.get('ponderacion')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Criterio actualizado exitosamente",
        "id": criterio.id
    })

# ELIMINAR
@criterios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_criterio(id):
    criterio = Criterio.query.get_or_404(id)
    db.session.delete(criterio)
    db.session.commit()
    return jsonify({"mensaje": "Criterio eliminado exitosamente"})