from flask import Blueprint, jsonify, request
from database import db
from models import Trabajo, TipoTrabajo
from datetime import datetime
from factories.trabajo_factory import TrabajoFactory

trabajos_bp = Blueprint('trabajos', __name__, url_prefix='/trabajos')

# CREAR TRABAJO
@trabajos_bp.route('/', methods=['POST'])
def crear_trabajo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400

    # Validar campos obligatorios
    if not data.get('titulo') or not data.get('estudiante_id') or not data.get('tipo_id'):
        return jsonify({"error": "Faltan campos obligatorios (titulo, estudiante_id, tipo_id)"}), 400

    try:
        # Obtener el nombre del tipo de trabajo para la fábrica
        tipo_trabajo = TipoTrabajo.query.get(data.get('tipo_id'))
        if not tipo_trabajo:
             return jsonify({"error": "Tipo de trabajo no válido"}), 400

        # Usar la fábrica para obtener la configuración
        configuracion = TrabajoFactory.crear_configuracion(tipo_trabajo.nombre)
        
        nuevo_trabajo = Trabajo(
            titulo=data.get('titulo'),
            resumen=data.get('resumen'),
            estudiante_id=data.get('estudiante_id'),
            tipo_id=data.get('tipo_id'),
            fecha_entrega=datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date() if data.get('fecha_entrega') else None,
            # Campos configurados por la fábrica
            duracion_meses=configuracion['duracion_meses'] if configuracion else 6,
            nota_aprobacion=configuracion['nota_aprobacion'] if configuracion else 4.0,
            requisito_aprobacion=configuracion['requisito'] if configuracion else "Cumplir requisitos estándar",
            estado='pendiente'
        )

        db.session.add(nuevo_trabajo)
        db.session.commit()

        return jsonify({
            "mensaje": "Trabajo creado exitosamente",
            "id": nuevo_trabajo.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear trabajo: {str(e)}"}), 500

# LISTAR TODOS
@trabajos_bp.route('/', methods=['GET'])
def listar_trabajos():
    trabajos = Trabajo.query.all()
    resultado = [{
        "id": t.id, 
        "titulo": t.titulo,
        "duracion_meses": t.duracion_meses,
        "nota_aprobacion": float(t.nota_aprobacion) if t.nota_aprobacion else None,
        "requisito_aprobacion": t.requisito_aprobacion,
        "resumen": t.resumen,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
        "estudiante_id": t.estudiante_id,
        "estado": t.estado,
        "tipo_id": t.tipo_id
    } for t in trabajos]
    return jsonify(resultado)

# OBTENER UNO POR ID
@trabajos_bp.route('/<int:id>', methods=['GET'])
def obtener_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    return jsonify({
        "id": trabajo.id,
        "titulo": trabajo.titulo,
        "duracion_meses": trabajo.duracion_meses,
        "nota_aprobacion": float(trabajo.nota_aprobacion) if trabajo.nota_aprobacion else None,
        "requisito_aprobacion": trabajo.requisito_aprobacion,
        "resumen": trabajo.resumen,
        "fecha_entrega": trabajo.fecha_entrega.isoformat() if trabajo.fecha_entrega else None,
    })

# ACTUALIZAR
@trabajos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Si cambian el tipo de trabajo, debemos recalcular las reglas
    if data.get('tipo'):
        configuracion = TrabajoFactory.crear_configuracion(data.get('tipo'))
        if configuracion:
            trabajo.duracion_meses = configuracion['duracion_meses']
            trabajo.nota_aprobacion = configuracion['nota_aprobacion']
            trabajo.requisito_aprobacion = configuracion['requisito']

    if data.get('titulo'):
        trabajo.titulo = data.get('titulo')
    if data.get('resumen'):
        trabajo.resumen = data.get('resumen')
    
    if data.get('fecha_entrega'):
        try:
            trabajo.fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400
            
    if data.get('estado'):
        trabajo.estado = data.get('estado')
        
    if data.get('tipo_id'):
        trabajo.tipo_id = data.get('tipo_id')
            
    db.session.commit()
    return jsonify({
        "mensaje": "Trabajo actualizado exitosamente",
        "id": trabajo.id
    })

# ELIMINAR
@trabajos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    db.session.delete(trabajo)
    db.session.commit()
    return jsonify({"mensaje": "Trabajo eliminado exitosamente"})

# LISTAR TRABAJOS POR ESTUDIANTE
@trabajos_bp.route('/estudiante/<int:estudiante_id>', methods=['GET'])
def listar_trabajos_por_estudiante(estudiante_id):
    trabajos = Trabajo.query.filter_by(estudiante_id=estudiante_id).all()
    resultado = [{
        "id": t.id, 
        "titulo": t.titulo,
        "duracion_meses": t.duracion_meses,
        "nota_aprobacion": float(t.nota_aprobacion) if t.nota_aprobacion else None,
        "requisito_aprobacion": t.requisito_aprobacion,
        "resumen": t.resumen,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
        "estudiante_id": t.estudiante_id,
        "estado": t.estado,
        "tipo_id": t.tipo_id
    } for t in trabajos]
    return jsonify(resultado)

# OBTENER EVALUACIONES DE UN TRABAJO
@trabajos_bp.route('/<int:id>/evaluaciones', methods=['GET'])
def obtener_evaluaciones_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    evaluaciones = trabajo.evaluaciones if hasattr(trabajo, 'evaluaciones') else []
    resultado = [{
        "id": e.id,
        "trabajo_id": e.trabajo_id,
        "evaluador_id": e.evaluador_id,
        "nota_final": float(e.nota_final) if e.nota_final else None,
        "comentarios": e.comentarios,
        "fecha_evaluacion": e.fecha_evaluacion.isoformat() if e.fecha_evaluacion else None
    } for e in evaluaciones]
    return jsonify(resultado)