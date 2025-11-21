from flask import Blueprint, jsonify, request
from database import db
from models.instituciones import Institucion

# Creamos el "Blueprint" (es como un mini-app solo para instituciones)
instituciones_bp = Blueprint('instituciones', __name__)

# Nota que aquí usamos @instituciones_bp, ya no @app
@instituciones_bp.route('/api/instituciones', methods=['GET', 'POST'])
def gestionar_instituciones():
    if request.method == 'POST':
        # Lógica para CREAR
        data = request.get_json()
        try:
            nueva_inst = Institucion(
                nombre=data.get('nombre'),
                direccion=data.get('direccion'),
                contacto=data.get('contacto')
            )
            db.session.add(nueva_inst)
            db.session.commit()
            return jsonify({'mensaje': 'Institución creada con éxito', 'id': nueva_inst.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Lógica para LEER (GET)
    lista = Institucion.query.all()
    resultado = []
    for inst in lista:
        resultado.append({
            'id': inst.id,
            'nombre': inst.nombre,
            'direccion': inst.direccion,
            'contacto': inst.contacto
        })
    return jsonify(resultado)