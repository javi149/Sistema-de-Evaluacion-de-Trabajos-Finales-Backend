from flask import Blueprint, jsonify, request
from database import db
from models.estudiantes import Estudiante
from sqlalchemy.exc import IntegrityError

# Creamos el Blueprint con url_prefix consistente con otras rutas
estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

# --- RUTA: /estudiantes ---
@estudiantes_bp.route('/', methods=['GET', 'POST'])
def gestionar_estudiantes():
    # 1. CREAR (POST)
    if request.method == 'POST':
        data = request.get_json()
        
        # Validación: Nombre es obligatorio
        if not data.get('nombre'):
            return jsonify({'error': 'El nombre es obligatorio'}), 400
            
        # Validación: RUT es obligatorio
        if not data.get('rut'):
            return jsonify({'error': 'El RUT es obligatorio'}), 400

        # Validación: Unicidad del RUT
        if Estudiante.query.filter_by(rut=data.get('rut')).first():
            return jsonify({'error': 'El RUT ya está registrado'}), 400

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
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Error de integridad en la base de datos'}), 400
        except Exception as e:
            db.session.rollback()
            print(f"ERROR CREANDO ESTUDIANTE: {e}")
            import traceback
            traceback.print_exc()
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

# --- RUTAS PARA UN ESTUDIANTE ESPECÍFICO ---

# 3. OBTENER UNO (GET)
@estudiantes_bp.route('/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    est = Estudiante.query.get_or_404(id)
    return jsonify({
        'id': est.id,
        'nombre': est.nombre,
        'apellido': est.apellido,
        'email': est.email,
        'carrera': est.carrera,
        'rut': est.rut
    })

# 4. ACTUALIZAR COMPLETO (PUT)
@estudiantes_bp.route('/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    est = Estudiante.query.get_or_404(id)
    data = request.get_json()
    
    # Validación: Nombre no puede estar vacío si se envía
    if 'nombre' in data and not data.get('nombre'):
        return jsonify({'error': 'El nombre no puede estar vacío'}), 400

    # Validación: Unicidad del RUT si cambia
    nuevo_rut = data.get('rut')
    if nuevo_rut and nuevo_rut != est.rut:
        if Estudiante.query.filter_by(rut=nuevo_rut).first():
            return jsonify({'error': 'El RUT ya está registrado por otro estudiante'}), 400
    
    est.nombre = data.get('nombre', est.nombre)
    est.apellido = data.get('apellido', est.apellido)
    est.rut = data.get('rut', est.rut)
    est.email = data.get('email', est.email)
    est.carrera = data.get('carrera', est.carrera)
    
    try:
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante actualizado', 'id': est.id})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error de integridad al actualizar'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 5. ACTUALIZAR PARCIAL (PATCH)
@estudiantes_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_estudiante_parcial(id):
    est = Estudiante.query.get_or_404(id)
    data = request.get_json()
    
    if 'nombre' in data:
        if not data.get('nombre'):
             return jsonify({'error': 'El nombre no puede estar vacío'}), 400
        est.nombre = data.get('nombre')
        
    if 'rut' in data:
        nuevo_rut = data.get('rut')
        if nuevo_rut != est.rut:
             if Estudiante.query.filter_by(rut=nuevo_rut).first():
                return jsonify({'error': 'El RUT ya está registrado por otro estudiante'}), 400
        est.rut = nuevo_rut

    if 'apellido' in data: est.apellido = data.get('apellido')
    if 'email' in data: est.email = data.get('email')
    if 'carrera' in data: est.carrera = data.get('carrera')
    
    try:
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante actualizado', 'id': est.id})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error de integridad al actualizar'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 6. ELIMINAR (DELETE)
@estudiantes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    est = Estudiante.query.get_or_404(id)
    try:
        db.session.delete(est)
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500