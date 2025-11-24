import os
from flask import Flask
from flask_cors import CORS
from database import db
from config.config import ConfiguracionGlobal

# Cargar .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def create_app():
    app = Flask(__name__)

    # Habilitar CORS
    CORS(app)

    # Configuración de Base de Datos
    db_uri = os.getenv('DATABASE_URL')
    if not db_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluacion.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()

    # --- REGISTRO DE RUTAS (BLUEPRINTS) ---
    # Aquí conectamos los módulos de tus compañeros

    # 1. Rutas de Estudiantes
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    # 2. Rutas de Evaluadores (Profesores)
    try:
        from routes.evaluadores import evaluadores_bp
        app.register_blueprint(evaluadores_bp)
    except Exception:
        pass

    # 3. Rutas de Trabajos
    try:
        from routes.trabajos import trabajos_bp
        app.register_blueprint(trabajos_bp)
    except Exception:
        pass

    # 4. Rutas de Tipos de Trabajo
    try:
        from routes.tipos_trabajo import tipos_trabajo_bp
        app.register_blueprint(tipos_trabajo_bp)
    except Exception:
        pass

    # 5. Rutas de Criterios
    try:
        from routes.criterios import criterios_bp
        app.register_blueprint(criterios_bp)
    except Exception:
        pass

    # 6. Rutas de Evaluaciones
    try:
        from routes.evaluaciones import evaluaciones_bp
        app.register_blueprint(evaluaciones_bp)
    except Exception:
        pass

    # 7. Rutas de Actas
    try:
        from routes.actas import actas_bp
        app.register_blueprint(actas_bp)
    except Exception:
        pass

    # --------------------------------------------------

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

# --- Configuración Global ---
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)