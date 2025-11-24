from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models import EvaluacionDetalle, Criterio, Evaluacion
from strategies.calculo_notas import PromedioPonderado, Calculadora

notas_bp = Blueprint('notas_bp', __name__)


@notas_bp.route('/api/calcular-nota/<int:trabajo_id>', methods=['GET'])
def calcular_nota_final(trabajo_id):
    try:
        calificaciones = (
            db.session.query(EvaluacionDetalle.nota, Criterio.ponderacion)
            .join(Criterio, EvaluacionDetalle.criterio_id == Criterio.id)
            .join(Evaluacion, EvaluacionDetalle.evaluacion_id == Evaluacion.id)
            .filter(Evaluacion.trabajo_id == trabajo_id)
            .all()
        )

        lista_calificaciones = [
            {
                'nota': float(nota) if nota is not None else 0.0,
                'ponderacion': float(ponderacion) if ponderacion is not None else 0.0
            }
            for nota, ponderacion in calificaciones
        ]

        if not lista_calificaciones:
            return jsonify({
                "mensaje": f"No se encontraron notas para el trabajo ID {trabajo_id}",
                "nota_final": 0.0
            }), 200

        estrategia = PromedioPonderado()
        contexto = Calculadora(estrategia)
        nota_final = contexto.obtener_resultado(lista_calificaciones)

        return jsonify({
            "trabajo_id": trabajo_id,
            "notas_procesadas": lista_calificaciones,
            "nota_final_calculada": nota_final,
            "estado": "Aprobado" if nota_final >= 3.0 else "Reprobado"
        })

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"ERROR SQL: {e}")
        return jsonify({"error": "Ocurrió un error al consultar las notas"}), 500