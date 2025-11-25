from flask import Blueprint, jsonify, request
from database import db
# IMPORTANTE: Revisa si tu modelo se llama 'Trabajo' o 'Trabajos' y ajusta esta línea
from models import Trabajo 
from datetime import datetime
# 1. IMPORTAMOS TU FÁBRICA
from factories.trabajo_factory import TrabajoFactory

trabajos_bp = Blueprint('trabajos', __name__, url_prefix='/trabajos')

# LISTAR TODOS (Esto queda igual)
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
        "estudiante_id": t.estudiante_id
    } for t in trabajos]
    return jsonify(resultado)

# OBTENER UNO POR ID (Esto queda igual)
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
        "estudiante_id": trabajo.estudiante_id
    })

# --- AQUÍ ESTÁ LA INTEGRACIÓN DE TU FACTORY (POST) ---
@trabajos_bp.route('/', methods=['POST'])
def crear_trabajo():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Validamos datos mínimos
    if not data.get('titulo') or not data.get('tipo'):
        return jsonify({"error": "El título y el tipo (tesis, proyecto...) son requeridos"}), 400
    
    # 2. USAMOS TU FACTORY
    # En lugar de leer la duración del JSON, la calculamos con tu fábrica
    configuracion = TrabajoFactory.crear_configuracion(data.get('tipo'))
    
    if not configuracion:
        return jsonify({"error": "Tipo de trabajo inválido. Use: tesis, proyecto, seminario"}), 400

    # Manejo de fecha (igual que antes)
    fecha_entrega = None
    if data.get('fecha_entrega'):
        try:
            fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    # 3. CREAMOS EL OBJETO CON TUS REGLAS
    nuevo = Trabajo(
        titulo=data.get('titulo'),
        estudiante_id=data.get('estudiante_id'),
        resumen=data.get('resumen'),
        fecha_entrega=fecha_entrega,
        
        # Aquí inyectamos lo que decidió tu Factory:
        duracion_meses=configuracion['duracion_meses'],
        nota_aprobacion=configuracion['nota_aprobacion'],
        requisito_aprobacion=configuracion['requisito'],
        
        # Opcional: Guardamos el nombre del tipo si tienes esa columna
        # tipo_id=data.get('tipo_id') 
    )

    try:
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({
            "mensaje": "Trabajo registrado exitosamente con configuración automática",
            "configuracion_aplicada": configuracion, # Para que vean que tu factory funcionó
            "id": nuevo.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ACTUALIZAR COMPLETO (PUT) - También lo integramos por si cambian el tipo
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
            
    db.session.commit()
    return jsonify({
        "mensaje": "Trabajo actualizado exitosamente",
        "id": trabajo.id
    })

# ELIMINAR (Igual que antes)
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
        "estudiante_id": t.estudiante_id
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