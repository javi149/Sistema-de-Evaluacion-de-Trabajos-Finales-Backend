from flask import Blueprint, jsonify, request
from database import db
from models.estudiantes import Estudiante

# Creamos el Blueprint con url_prefix consistente con otras rutas
estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

# --- RUTA: /estudiantes ---
@estudiantes_bp.route('/', methods=['GET', 'POST'])
def gestionar_estudiantes():
    # 1. CREAR (POST)
    if request.method == 'POST':
        data = request.get_json()
        try:
            nuevo = Estudiante(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                rut=data.get('rut'),
                email=data.get('email'),
                carrera=data.get('carrera')
            )
            db.session.add(nuevo)
            db.session.commit()
            return jsonify({'mensaje': 'Estudiante creado', 'id': nuevo.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 2. LISTAR (GET)
    try:
        lista = Estudiante.query.all()
        resultado = []
        for est in lista:
            resultado.append({
                'id': est.id,
                'nombre': est.nombre,
                'apellido': est.apellido,
                'email': est.email,
                'carrera': est.carrera,
                'rut': est.rut
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500