from flask import Blueprint, jsonify
from sqlalchemy import text
from database import db
from strategies.calculo_notas import PromedioPonderado, Calculadora

notas_bp = Blueprint('notas_bp', __name__)

@notas_bp.route('/api/calcular-nota/<int:trabajo_id>', methods=['GET'])
def calcular_nota_final(trabajo_id):
    try:
        # --- CAMBIO IMPORTANTE AQUÍ ---
        # Ahora hacemos JOIN con la tabla 'criterios' (letra c) para sacar la ponderacion
        query = text("""
            SELECT d.nota, c.ponderacion
            FROM evaluacion_detalle d
            JOIN criterios c ON d.criterio_id = c.id
            JOIN evaluaciones e ON d.evaluacion_id = e.id
            WHERE e.trabajo_id = :id_trabajo
        """)
        
        resultado_sql = db.session.execute(query, {'id_trabajo': trabajo_id})
        
        lista_calificaciones = []
        for row in resultado_sql:
            lista_calificaciones.append({
                'nota': float(row[0]),       # La nota viene de 'evaluacion_detalle'
                'porcentaje': float(row[1])  # La ponderación viene de 'criterios'
            })

        if not lista_calificaciones:
            return jsonify({
                "mensaje": f"No se encontraron notas para el trabajo ID {trabajo_id}",
                "nota_final": 0.0
            }), 200

        # Estrategia de Cálculo
        estrategia = PromedioPonderado()
        contexto = Calculadora(estrategia)
        nota_final = contexto.obtener_resultado(lista_calificaciones)

        return jsonify({
            "trabajo_id": trabajo_id,
            "notas_procesadas": lista_calificaciones,
            "nota_final_calculada": nota_final,
            "estado": "Aprobado" if nota_final >= 3.0 else "Reprobado"
        })

    except Exception as e:
        print(f"ERROR SQL: {e}")
        return jsonify({"error": str(e)}), 500