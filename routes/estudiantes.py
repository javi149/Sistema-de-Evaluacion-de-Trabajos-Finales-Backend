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

# OBTENER UNO POR ID
@estudiantes_bp.route('/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    alumno = Estudiante.query.get_or_404(id)
    return jsonify({
        "id": alumno.id,
        "nombre": alumno.nombre,
        "apellido": alumno.apellido,
        "rut": alumno.rut,
        "email": alumno.email,
        "carrera": alumno.carrera
    })

# CREAR
@estudiantes_bp.route('/', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    nuevo = Estudiante(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        rut=data.get('rut'),
        email=data.get('email'),
        carrera=data.get('carrera')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "mensaje": "Estudiante creado exitosamente",
        "id": nuevo.id
    }), 201

# ACTUALIZAR COMPLETO (PUT)
@estudiantes_bp.route('/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    alumno = Estudiante.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if not data.get('nombre'):
        return jsonify({"error": "El nombre es requerido"}), 400
    
    alumno.nombre = data.get('nombre')
    alumno.apellido = data.get('apellido')
    alumno.rut = data.get('rut')
    alumno.email = data.get('email')
    alumno.carrera = data.get('carrera')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Estudiante actualizado exitosamente",
        "id": alumno.id
    })

# ACTUALIZAR PARCIAL (PATCH)
@estudiantes_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_estudiante_parcial(id):
    alumno = Estudiante.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    if 'nombre' in data:
        alumno.nombre = data.get('nombre')
    if 'apellido' in data:
        alumno.apellido = data.get('apellido')
    if 'rut' in data:
        alumno.rut = data.get('rut')
    if 'email' in data:
        alumno.email = data.get('email')
    if 'carrera' in data:
        alumno.carrera = data.get('carrera')
    
    db.session.commit()
    return jsonify({
        "mensaje": "Estudiante actualizado exitosamente",
        "id": alumno.id
    })

# ELIMINAR
@estudiantes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    alumno = Estudiante.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante eliminado exitosamente"})

# OBTENER TRABAJOS DE UN ESTUDIANTE
@estudiantes_bp.route('/<int:id>/trabajos', methods=['GET'])
def obtener_trabajos_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    trabajos = estudiante.trabajos if hasattr(estudiante, 'trabajos') else []
    resultado = [{
        "id": t.id,
        "titulo": t.titulo,
        "duracion_meses": t.duracion_meses,
        "nota_aprobacion": float(t.nota_aprobacion) if t.nota_aprobacion else None,
        "requisito_aprobacion": t.requisito_aprobacion,
        "resumen": t.resumen,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
        "estudiante_id": t.estudiante_id
    } for t in trabajos]
    return jsonify(resultado)