from flask import Blueprint, make_response, jsonify
from models.trabajos import Trabajo
from patrones.acta_html import ActaHTML
from patrones.acta_texto import ActaTexto
from datetime import datetime

# Definimos el "Blueprint" (El grupo de rutas) tal como lo pidió Javi
acta_bp = Blueprint('actas', __name__)

def obtener_datos_comunes(trabajo_id):
    """Función auxiliar para no repetir código entre HTML y Texto"""
    trabajo = Trabajo.query.get(trabajo_id)
    if not trabajo:
        return None, None
    
    # Preparamos datos del encabezado
    datos_trabajo = {
        'titulo_trabajo': trabajo.titulo,
        'estudiante_nombre': trabajo.estudiante.nombre,
        'estudiante_apellido': trabajo.estudiante.apellido,
        'estudiante_rut': trabajo.estudiante.rut,
        'institucion': 'Instituto Profesional (IP)',
        'fecha_actual': datetime.now().strftime("%d/%m/%Y")
    }

    # Preparamos lista de evaluaciones
    lista_evaluaciones = []
    for ev in trabajo.evaluaciones:
        lista_evaluaciones.append({
            'evaluador_id': ev.evaluador_id,
            'nota_final': float(ev.nota_final),
            'comentarios': ev.comentarios
        })
        
    return datos_trabajo, lista_evaluaciones

# --- RUTA 1: Generar HTML (Para ver en navegador) ---
@acta_bp.route('/generar-acta/html/<int:trabajo_id>', methods=['GET'])
def generar_acta_html(trabajo_id):
    datos, evaluaciones = obtener_datos_comunes(trabajo_id)
    
    if not datos:
        return jsonify({"error": "Trabajo no encontrado"}), 404

    # Usamos TU patrón Template Method (Versión HTML)
    generador = ActaHTML()
    contenido = generador.generar_acta(datos, evaluaciones)

    response = make_response(contenido)
    response.headers['Content-Type'] = 'text/html'
    return response

# --- RUTA 2: Generar Texto Plano (Para descargar) ---
@acta_bp.route('/generar-acta/texto/<int:trabajo_id>', methods=['GET'])
def generar_acta_texto(trabajo_id):
    datos, evaluaciones = obtener_datos_comunes(trabajo_id)
    
    if not datos:
        return jsonify({"error": "Trabajo no encontrado"}), 404

    # Usamos TU patrón Template Method (Versión Texto)
    generador = ActaTexto()
    contenido = generador.generar_acta(datos, evaluaciones)

    response = make_response(contenido)
    response.headers['Content-Type'] = 'text/plain'
    return response