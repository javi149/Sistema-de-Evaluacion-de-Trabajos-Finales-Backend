from flask import Blueprint, jsonify
from sqlalchemy import text
from database import db
from strategies.calculo_notas import PromedioPonderado, Calculadora

notas_bp = Blueprint('notas_bp', __name__)

@notas_bp.route('/api/calcular-nota/<int:trabajo_id>', methods=['GET'])
def calcular_nota_final(trabajo_id):
    try:
        # 1. SQL REAL BASADO EN TU IMAGEN
        # Unimos 'evaluaciones' (para filtrar por trabajo) con 'evaluacion_detalle' (para ver las notas)
        query = text("""
            SELECT d.nota, d.ponderacion
            FROM evaluacion_detalle d
            JOIN evaluaciones e ON d.evaluacion_id = e.id
            WHERE e.trabajo_id = :id_trabajo
        """)
        
        resultado_sql = db.session.execute(query, {'id_trabajo': trabajo_id})
        
        # 2. Convertir datos de la BD a lo que entiende tu Strategy
        lista_calificaciones = []
        for row in resultado_sql:
            # row[0] es la nota, row[1] es la ponderación
            lista_calificaciones.append({
                'nota': float(row[0]),       # Convertimos Decimal a float
                'porcentaje': float(row[1])  # Tu base de datos la llama 'ponderacion'
            })

        # Si la lista está vacía, no hay notas registradas aún
        if not lista_calificaciones:
            return jsonify({
                "mensaje": f"No se encontraron notas para el trabajo ID {trabajo_id}",
                "nota_final": 0.0
            }), 200

        # 3. USAR TU PATRÓN STRATEGY (La lógica que creaste)
        estrategia = PromedioPonderado()
        contexto = Calculadora(estrategia)
        
        nota_final = contexto.obtener_resultado(lista_calificaciones)

        return jsonify({
            "trabajo_id": trabajo_id,
            "notas_procesadas": lista_calificaciones, # Te muestro las notas que encontró
            "nota_final_calculada": nota_final,
            "estado": "Aprobado" if nota_final >= 3.0 else "Reprobado"
        })

    except Exception as e:
        print(f"ERROR: {e}") # Esto imprime el error en tu terminal negra
        return jsonify({"error": str(e)}), 500