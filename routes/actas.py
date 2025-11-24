from datetime import datetime

from flask import Blueprint, jsonify, make_response, request

from database import db
from models import Acta, Trabajo
from patrones.acta_html import ActaHTML
from patrones.acta_texto import ActaTexto


actas_bp = Blueprint('actas', __name__, url_prefix='/actas')


# =============================================================================
#  Generación de actas (Template Method)
# =============================================================================

def _obtener_datos_para_patron(trabajo_id):
    """Prepara la data cruda para alimentar los generadores de actas."""
    trabajo = Trabajo.query.get(trabajo_id)
    if not trabajo:
        return None, None

    datos_trabajo = {
        'titulo_trabajo': trabajo.titulo,
        'estudiante_nombre': trabajo.estudiante.nombre if trabajo.estudiante else 'Desconocido',
        'estudiante_apellido': trabajo.estudiante.apellido if trabajo.estudiante else '',
        'estudiante_rut': trabajo.estudiante.rut if trabajo.estudiante else 'S/N',
        'institucion': 'Instituto Profesional',
        'fecha_actual': datetime.now().strftime('%d/%m/%Y')
    }

    lista_evaluaciones = []
    for ev in getattr(trabajo, 'evaluaciones', []):
        lista_evaluaciones.append({
            'evaluador_id': ev.evaluador_id,
            'nota_final': float(ev.nota_final) if ev.nota_final else 0.0,
            'comentarios': ev.comentarios or 'Sin comentarios'
        })

    return datos_trabajo, lista_evaluaciones


@actas_bp.route('/generar/html/<int:trabajo_id>', methods=['GET'])
def generar_acta_html(trabajo_id):
    datos, evaluaciones = _obtener_datos_para_patron(trabajo_id)
    if not datos:
        return jsonify({'error': 'Trabajo no encontrado'}), 404

    generador = ActaHTML()
    contenido = generador.generar_acta(datos, evaluaciones)

    response = make_response(contenido)
    response.headers['Content-Type'] = 'text/html'
    return response


@actas_bp.route('/generar/texto/<int:trabajo_id>', methods=['GET'])
def generar_acta_texto(trabajo_id):
    datos, evaluaciones = _obtener_datos_para_patron(trabajo_id)
    if not datos:
        return jsonify({'error': 'Trabajo no encontrado'}), 404

    generador = ActaTexto()
    contenido = generador.generar_acta(datos, evaluaciones)

    response = make_response(contenido)
    response.headers['Content-Type'] = 'text/plain'
    return response


# =============================================================================
#  CRUD de Actas
# =============================================================================

@actas_bp.route('/', methods=['GET'])
def listar_actas():
    actas = Acta.query.all()
    resultado = [{
        'id': a.id,
        'trabajo_id': a.trabajo_id,
        'fecha': a.fecha.isoformat() if a.fecha else None,
        'url_pdf': a.url_pdf,
        'estado': a.estado
    } for a in actas]
    return jsonify(resultado)


@actas_bp.route('/', methods=['POST'])
def crear_acta():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos JSON'}), 400
    if not data.get('trabajo_id'):
        return jsonify({'error': 'El trabajo_id es requerido'}), 400
    if data.get('estado') and data['estado'] not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
        return jsonify({'error': 'El estado debe ser APROBADO, REPROBADO o PENDIENTE'}), 400

    fecha = None
    if data.get('fecha'):
        try:
            fecha = datetime.fromisoformat(data.get('fecha').replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            try:
                fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO'}), 400

    nueva = Acta(
        trabajo_id=data.get('trabajo_id'),
        fecha=fecha,
        url_pdf=data.get('url_pdf'),
        estado=data.get('estado', 'PENDIENTE')
    )

    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Acta creada exitosamente', 'id': nueva.id}), 201


@actas_bp.route('/<int:id>', methods=['PUT'])
def actualizar_acta(id):
    acta = Acta.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos JSON'}), 400
    if not data.get('trabajo_id'):
        return jsonify({'error': 'El trabajo_id es requerido'}), 400
    if data.get('estado') and data['estado'] not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
        return jsonify({'error': 'El estado debe ser APROBADO, REPROBADO o PENDIENTE'}), 400

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
                return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO'}), 400
    else:
        acta.fecha = None

    db.session.commit()
    return jsonify({'mensaje': 'Acta actualizada exitosamente', 'id': acta.id})


@actas_bp.route('/<int:id>', methods=['PATCH'])
def actualizar_acta_parcial(id):
    acta = Acta.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos JSON'}), 400

    if 'trabajo_id' in data:
        acta.trabajo_id = data.get('trabajo_id')
    if 'url_pdf' in data:
        acta.url_pdf = data.get('url_pdf')
    if 'estado' in data:
        if data['estado'] not in ['APROBADO', 'REPROBADO', 'PENDIENTE']:
            return jsonify({'error': 'El estado debe ser APROBADO, REPROBADO o PENDIENTE'}), 400
        acta.estado = data.get('estado')
    if 'fecha' in data:
        if data.get('fecha'):
            try:
                acta.fecha = datetime.fromisoformat(data.get('fecha').replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                try:
                    acta.fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS o ISO'}), 400
        else:
            acta.fecha = None

    db.session.commit()
    return jsonify({'mensaje': 'Acta actualizada exitosamente', 'id': acta.id})


@actas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_acta(id):
    acta = Acta.query.get_or_404(id)
    db.session.delete(acta)
    db.session.commit()
    return jsonify({'mensaje': 'Acta eliminada exitosamente'})