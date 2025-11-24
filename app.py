import os

from flask import Flask
from flask_cors import CORS

from config.config import ConfiguracionGlobal
from database import db

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _build_db_uri():
    direct_uri = os.getenv('DATABASE_URL')
    if direct_uri:
        return direct_uri

    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    driver = os.getenv('DB_DRIVER', 'mysql+mysqlconnector')

    if all([user, password, host, dbname]):
        port_section = f":{port}" if port else ""
        return f"{driver}://{user}:{password}@{host}{port_section}/{dbname}"

    return 'sqlite:///evaluacion.db'


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = _build_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()
    _register_blueprints(app)

    return app


def _register_blueprints(app):
    """Centraliza el registro de rutas para mantener create_app limpio."""
    from routes.notas_routes import notas_bp
    from routes.estudiantes import estudiantes_bp
    from routes.evaluaciones import evaluaciones_bp
    from routes.evaluadores import evaluadores_bp
    from routes.criterios import criterios_bp
    from routes.tipos_trabajo import tipos_trabajo_bp
    from routes.trabajos import trabajos_bp
    from routes.evaluacion_detalle import evaluacion_detalle_bp
    from routes.acta_routes import acta_bp

    app.register_blueprint(notas_bp)
    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(evaluaciones_bp)
    app.register_blueprint(evaluadores_bp)
    app.register_blueprint(criterios_bp)
    app.register_blueprint(tipos_trabajo_bp)
    app.register_blueprint(trabajos_bp)
    app.register_blueprint(evaluacion_detalle_bp)
    app.register_blueprint(acta_bp)


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
