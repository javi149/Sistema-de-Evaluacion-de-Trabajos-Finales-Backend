from flask import Blueprint, jsonify, request
from database import db
from models import Institucion

instituciones_bp = Blueprint('instituciones', __name__, url_prefix='/instituciones')

# LISTAR TODOS
@instituciones_bp.route('/', methods=['GET'])
def listar_instituciones():
    instituciones = Institucion.query.all()
    resultado = [{
        "id": i.id,
        "nombre": i.nombre,
        "direccion": i.direccion,
        "contacto": i.contacto,
        "logo_url": i.logo_url
    } for i in instituciones]
    return jsonify(resultado)

# OBTENER UNO POR ID
@instituciones_bp.route('/<int:id>', methods=['GET'])
def obtener_institucion(id):
    institucion = Institucion.query.get_or_404(id)
    return jsonify({
        "id": institucion.id,
        "nombre": institucion.nombre,
        "direccion": institucion.direccion,
        "contacto": institucion.contacto,
        "logo_url": institucion.logo_url
    })

# CREAR
@instituciones_bp.route('/', methods=['POST'])
def crear_institucion():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nueva = Institucion(
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        contacto=data.get('contacto'),
        logo_url=data.get('logo_url')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({
        "mensaje": "Institución creada exitosamente",
        "id": nueva.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@instituciones_bp.route('/<int:id>', methods=['PUT'])
def actualizar_institucion(id):
    institucion = Institucion.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    institucion.nombre = data.get('nombre')
    institucion.direccion = data.get('direccion')
    institucion.contacto = data.get('contacto')
    institucion.logo_url = data.get('logo_url')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Institución actualizada exitosamente",
        "id": institucion.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@instituciones_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_institucion_parcial(id):
    institucion = Institucion.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'nombre' in data:
        institucion.nombre = data.get('nombre')
    if 'direccion' in data:
        institucion.direccion = data.get('direccion')
    if 'contacto' in data:
        institucion.contacto = data.get('contacto')
    if 'logo_url' in data:
        institucion.logo_url = data.get('logo_url')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Institución actualizada exitosamente",
        "id": institucion.id
    })

# ELIMINAR
@instituciones_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_institucion(id):
    institucion = Institucion.query.get_or_404(id)
    db.session.delete(institucion)
    db.session.commit()
    return jsonify({"mensaje": "Institución eliminada exitosamente"})

