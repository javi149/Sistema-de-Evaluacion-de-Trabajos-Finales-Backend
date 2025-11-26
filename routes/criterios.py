from flask import Blueprint, jsonify, request
from database import db
from models.criterios import Criterio

# Definimos el Blueprint
criterios_bp = Blueprint('criterios', __name__)

# --- RUTA CORRECTA: /api/criterios ---
@criterios_bp.route('/api/criterios', methods=['GET'])
def listar_criterios():
    try:
        lista = Criterio.query.all()
        resultado = [{
            "id": c.id,
            "nombre": c.nombre,
            "descripcion": c.descripcion,
            "ponderacion": float(c.ponderacion) if c.ponderacion else 0
        } for c in lista]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@criterios_bp.route('/api/criterios', methods=['POST'])
def crear_criterio():
    data = request.get_json()
    try:
        nuevo = Criterio(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            ponderacion=data.get('ponderacion'),
            institucion_id=1 # Valor por defecto para evitar errores si no se envía
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Criterio creado", "id": nuevo.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500