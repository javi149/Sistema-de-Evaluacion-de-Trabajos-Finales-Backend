from flask import Blueprint, jsonify, request
from database import db
from models import Acta
from datetime import datetime

actas_bp = Blueprint('actas', __name__, url_prefix='/actas')

# LISTAR TODOS
@actas_bp.route('/', methods=['GET'])
def listar_actas():
    actas = Acta.query.all()
    resultado = [{
        "id": a.id,
        "trabajo_id": a.trabajo_id,
        "fecha": a.fecha.isoformat() if a.fecha else None,
        "url_pdf": a.url_pdf,
        "estado": a.estado
    } for a in actas]
    return jsonify(resultado)

# OBTENER UNO POR ID
@actas_bp.route('/<int:id>', methods=['GET'])
def obtener_acta(id):
    acta = Acta.query.get_or_404(id)
    return jsonify({
        "id": acta.id,
        "trabajo_id": acta.trabajo_id,
        "fecha": acta.fecha.isoformat() if acta.fecha else None,
        "url_pdf": acta.url_pdf,
        "estado": acta.estado
    })

# CREAR
@actas_bp.route('/', methods=['POST'])
def crear_acta():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('trabajo_id'):
        return jsonify({"error": "El trabajo_id es requerido"}), 400
    
    # Validar estado si se proporciona
    if data.get('estado') and data.get('estado') not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
        return jsonify({"error": "El estado debe ser: APROBADO, REPROBADO o PENDIENTE"}), 400
    
    fecha = None
    if data.get('fecha'):
        try:
            fecha = datetime.fromisoformat(data.get('fecha').replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            try:
                fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO format"}), 400
    
    nueva = Acta(
        trabajo_id=data.get('trabajo_id'),
        fecha=fecha,
        url_pdf=data.get('url_pdf'),
        estado=data.get('estado', 'PENDIENTE')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({
        "mensaje": "Acta creada exitosamente",
        "id": nueva.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@actas_bp.route('/<int:id>', methods=['PUT'])
def actualizar_acta(id):
    acta = Acta.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('trabajo_id'):
        return jsonify({"error": "El trabajo_id es requerido"}), 400
    
    # Validar estado si se proporciona
    if data.get('estado') and data.get('estado') not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
        return jsonify({"error": "El estado debe ser: APROBADO, REPROBADO o PENDIENTE"}), 400
    
    acta.trabajo_id = data.get('trabajo_id')
    acta.url_pdf = data.get('url_pdf')
    acta.estado = data.get('estado', 'PENDIENTE')
    
    if data.get('fecha'):
        try:
            acta.fecha = datetime.fromisoformat(data.get('fecha').replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            try:
                acta.fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO format"}), 400
    else:
        acta.fecha = None
    
    db.session.commit()
    return jsonify({
        "mensaje": "Acta actualizada exitosamente",
        "id": acta.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@actas_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_acta_parcial(id):
    acta = Acta.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'trabajo_id' in data:
        acta.trabajo_id = data.get('trabajo_id')
    if 'url_pdf' in data:
        acta.url_pdf = data.get('url_pdf')
    if 'estado' in data:
        if data.get('estado') not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
            return jsonify({"error": "El estado debe ser: APROBADO, REPROBADO o PENDIENTE"}), 400
        acta.estado = data.get('estado')
    if 'fecha' in data:
        if data.get('fecha'):
            try:
                acta.fecha = datetime.fromisoformat(data.get('fecha').replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                try:
                    acta.fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO format"}), 400
        else:
            acta.fecha = None
    
    db.session.commit()
    return jsonify({
        "mensaje": "Acta actualizada exitosamente",
        "id": acta.id
    })

# ELIMINAR
@actas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_acta(id):
    acta = Acta.query.get_or_404(id)
    db.session.delete(acta)
    db.session.commit()
    return jsonify({"mensaje": "Acta eliminada exitosamente"})

