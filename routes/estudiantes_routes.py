from flask import Blueprint, jsonify, request
from database import db
from models import Estudiante 

estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

# LISTAR TODOS
@estudiantes_bp.route('/', methods=['GET'])
def listar_estudiantes():
    alumnos = Estudiante.query.all()
    resultado = [{
        "id": a.id, 
        "nombre": a.nombre, 
        "apellido": a.apellido,
        "rut": a.rut,
        "email": a.email,
        "carrera": a.carrera
    } for a in alumnos]
    return jsonify(resultado)

# CREAR UNO
@estudiantes_bp.route('/', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    nuevo = Estudiante(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        rut=data.get('rut'),
        email=data.get('email'),
        carrera=data.get('carrera')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante creado", "id": nuevo.id}), 201

# ELIMINAR
@estudiantes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    alumno = Estudiante.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante eliminado"})
