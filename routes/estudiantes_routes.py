from flask import Blueprint, jsonify
estudiantes_bp = Blueprint('estudiantes_bp', _name_)
@estudiantes_bp.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    return jsonify({"mensaje": "Aquí irán los estudiantes desde la BD"})
