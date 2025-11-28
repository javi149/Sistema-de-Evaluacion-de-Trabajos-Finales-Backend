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
    app.url_map.strict_slashes = False # Permite URLs con o sin slash final (evita redirects 308 que rompen CORS)

    # Configuración de Base de Datos
    db_uri = _build_db_uri()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()

    # Habilitar CORS con configuración completa
    CORS(app, 
         resources={r"/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
             "expose_headers": ["Content-Type"],
             "supports_credentials": False,
             "max_age": 3600
         }}
    )
    
    # Agregar headers CORS manualmente para asegurar compatibilidad total
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With,Accept'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response

    # --- REGISTRO DE RUTAS (BLUEPRINTS) ---
    # Conectamos cada archivo de la carpeta 'routes' con el sistema principal.

    # 1. Estudiantes
    from routes.estudiantes import estudiantes_bp
    app.register_blueprint(estudiantes_bp)

    # 2. Evaluadores (Docentes)
    try:
        from routes.evaluadores import evaluadores_bp
        app.register_blueprint(evaluadores_bp)
    except Exception as e:
        print(f"WARNING: Evaluadores no cargado: {e}")

    # 3. Tipos de Trabajo
    try:
        from routes.tipos_trabajo import tipos_trabajo_bp
        app.register_blueprint(tipos_trabajo_bp)
    except Exception as e:
        print(f"WARNING: Tipos de Trabajo no cargado: {e}")

    # 4. Trabajos
    from routes.trabajos import trabajos_bp
    app.register_blueprint(trabajos_bp)

    # 5. Criterios
    try:
        from routes.criterios import criterios_bp
        app.register_blueprint(criterios_bp)
    except Exception as e:
        print(f"WARNING: Criterios no cargado: {e}")

    # 6. Evaluaciones (Cabecera)
    try:
        from routes.evaluaciones import evaluaciones_bp
        app.register_blueprint(evaluaciones_bp)
    except Exception as e:
        print(f"WARNING: Evaluaciones no cargado: {e}")

    # 7. Detalle de Evaluación (Notas por criterio)
    try:
        from routes.evaluacion_detalle import evaluacion_detalle_bp
        app.register_blueprint(evaluacion_detalle_bp)
    except Exception as e:
        print(f"WARNING: Detalle Evaluación no cargado: {e}")

    # 8. Actas (CRUD: Crear, Listar, Borrar actas + Generación con Template Method)
    try:
        from routes.actas import actas_bp
        app.register_blueprint(actas_bp)
    except Exception as e:
        print(f"WARNING: Actas no cargado: {e}")

    # 9. Cálculo de Notas
    try:
        from routes.notas_routes import notas_bp
        app.register_blueprint(notas_bp)
    except Exception as e:
        print(f"WARNING: Cálculo de Notas no cargado: {e}")

    # --------------------------------------------------

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

# --- Configuración Global ---
app = create_app()

# Esto asegura que las tablas existan al iniciar
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
