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

    # Validar campos obligatorios (tipo_id ya no es obligatorio si se envían los datos manuales)
    if not data.get('titulo') or not data.get('estudiante_id'):
        return jsonify({"error": "Faltan campos obligatorios (titulo, estudiante_id)"}), 400

    try:
        # Valores por defecto o desde la fábrica si existe tipo_id
        duracion = 6
        nota = 4.0
        requisito = "Cumplir requisitos estándar"
        
        if data.get('tipo_id'):
            tipo_trabajo = TipoTrabajo.query.get(data.get('tipo_id'))
            if tipo_trabajo:
                configuracion = TrabajoFactory.crear_configuracion(tipo_trabajo.nombre)
                if configuracion:
                    duracion = configuracion['duracion_meses']
                    nota = configuracion['nota_aprobacion']
                    requisito = configuracion['requisito']

        # Sobrescribir con valores manuales si vienen del frontend
        if data.get('duracion_meses'):
            duracion = data.get('duracion_meses')
        if data.get('nota_aprobacion'):
            nota = data.get('nota_aprobacion')
        if data.get('requisito'): # El frontend puede enviar 'requisito'
            requisito = data.get('requisito')
        elif data.get('requisito_aprobacion'):
             requisito = data.get('requisito_aprobacion')

        nuevo_trabajo = Trabajo(
            titulo=data.get('titulo'),
            resumen=data.get('resumen'),
            estudiante_id=data.get('estudiante_id'),
            tipo_id=data.get('tipo_id'), # Puede ser None
            fecha_entrega=datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date() if data.get('fecha_entrega') else None,
            duracion_meses=duracion,
            nota_aprobacion=nota,
            requisito_aprobacion=requisito,
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
        "estudiante_id": trabajo.estudiante_id,
        "tipo_id": trabajo.tipo_id,
        "estado": trabajo.estado
    })

# ACTUALIZAR
@trabajos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_trabajo(id):
    trabajo = Trabajo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Si cambian el tipo de trabajo, aplicamos configuración base, pero permitimos sobrescribir
    if data.get('tipo_id'): # Corregido de 'tipo' a 'tipo_id' para consistencia
        trabajo.tipo_id = data.get('tipo_id')
        tipo_obj = TipoTrabajo.query.get(trabajo.tipo_id)
        if tipo_obj:
            configuracion = TrabajoFactory.crear_configuracion(tipo_obj.nombre)
            if configuracion:
                trabajo.duracion_meses = configuracion['duracion_meses']
                trabajo.nota_aprobacion = configuracion['nota_aprobacion']
                trabajo.requisito_aprobacion = configuracion['requisito']

    # Actualización manual de campos (sobrescribe la fábrica si se envían)
    if data.get('duracion_meses') is not None:
        trabajo.duracion_meses = data.get('duracion_meses')
    if data.get('nota_aprobacion') is not None:
        trabajo.nota_aprobacion = data.get('nota_aprobacion')
    if data.get('requisito') is not None:
        trabajo.requisito_aprobacion = data.get('requisito')
    elif data.get('requisito_aprobacion') is not None:
        trabajo.requisito_aprobacion = data.get('requisito_aprobacion')

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