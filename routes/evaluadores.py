from flask import Blueprint, jsonify, request
from database import db
from models import Evaluadores

evaluadores_bp = Blueprint('evaluadores', __name__, url_prefix='/evaluadores')

# LISTAR TODOS
@evaluadores_bp.route('/', methods=['GET'])
def listar_evaluadores():
    evaluadores = Evaluadores.query.all()
    resultado = [{
        "id": e.id, 
        "nombre": e.nombre, 
        "email": e.email,
        "rol": e.rol,  # Tutor, Jurado
        "tipo": e.tipo # Interno, Externo
    } for e in evaluadores]
    return jsonify(resultado)

# OBTENER UNO POR ID
@evaluadores_bp.route('/<int:id>', methods=['GET'])
def obtener_evaluador(id):
    evaluador = Evaluadores.query.get_or_404(id)
    return jsonify({
        "id": evaluador.id,
        "nombre": evaluador.nombre,
        "email": evaluador.email,
        "rol": evaluador.rol,
        "tipo": evaluador.tipo
    })

# CREAR
@evaluadores_bp.route('/', methods=['POST'])
def crear_evaluador():
    data = request.get_json()
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nuevo = Evaluadores(
        nombre=data.get('nombre'),
        email=data.get('email'),
        rol=data.get('rol'),
        tipo=data.get('tipo')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluador creado exitosamente",
        "id": nuevo.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@evaluadores_bp.route('/<int:id>', methods=['PUT'])
def actualizar_evaluador(id):
    evaluador = Evaluadores.query.get_or_404(id)
    data = request.get_json()
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    evaluador.nombre = data.get('nombre')
    evaluador.email = data.get('email')
    evaluador.rol = data.get('rol')
    evaluador.tipo = data.get('tipo')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluador actualizado exitosamente",
        "id": evaluador.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@evaluadores_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_evaluador_parcial(id):
    evaluador = Evaluadores.query.get_or_404(id)
    data = request.get_json()
    
    if 'nombre' in data:
        evaluador.nombre = data.get('nombre')
    if 'email' in data:
        evaluador.email = data.get('email')
    if 'rol' in data:
        evaluador.rol = data.get('rol')
    if 'tipo' in data:
        evaluador.tipo = data.get('tipo')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Evaluador actualizado exitosamente",
        "id": evaluador.id
    })

# ELIMINAR
@evaluadores_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_evaluador(id):
    evaluador = Evaluadores.query.get_or_404(id)
    db.session.delete(evaluador)
    db.session.commit()
    return jsonify({"mensaje": "Evaluador eliminado exitosamente"})
