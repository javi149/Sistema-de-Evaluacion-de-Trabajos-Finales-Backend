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

    # Habilitar CORS (Permite que React se conecte)
    CORS(app)

    # Configuración de Base de Datos
    db_uri = os.getenv('DATABASE_URL')
    if not db_uri:
        # Fallback a SQLite local si no hay nube configurada
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluacion.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()

    # --- REGISTRO DE RUTAS (BLUEPRINTS) ---
    # Conectamos cada archivo de la carpeta 'routes' con el sistema principal.

    # 1. Estudiantes
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception as e:
        print(f"⚠️ Estudiantes no cargado: {e}")

    # 2. Evaluadores (Docentes)
    try:
        from routes.evaluadores import evaluadores_bp
        app.register_blueprint(evaluadores_bp)
    except Exception as e:
        print(f"⚠️ Evaluadores no cargado: {e}")

    # 3. Tipos de Trabajo
    try:
        from routes.tipos_trabajo import tipos_trabajo_bp
        app.register_blueprint(tipos_trabajo_bp)
    except Exception as e:
        print(f"⚠️ Tipos de Trabajo no cargado: {e}")

    # 4. Trabajos
    try:
        from routes.trabajos import trabajos_bp
        app.register_blueprint(trabajos_bp)
    except Exception as e:
        print(f"⚠️ Trabajos no cargado: {e}")

    # 5. Criterios
    try:
        from routes.criterios import criterios_bp
        app.register_blueprint(criterios_bp)
    except Exception as e:
        print(f"⚠️ Criterios no cargado: {e}")

    # 6. Evaluaciones (Cabecera)
    try:
        from routes.evaluaciones import evaluaciones_bp
        app.register_blueprint(evaluaciones_bp)
    except Exception as e:
        print(f"⚠️ Evaluaciones no cargado: {e}")

    # 7. Detalle de Evaluación (Notas por criterio)
    try:
        from routes.evaluacion_detalle import evaluacion_detalle_bp
        app.register_blueprint(evaluacion_detalle_bp)
    except Exception as e:
        print(f"⚠️ Detalle Evaluación no cargado: {e}")

    # 8. Actas (CRUD: Crear, Listar, Borrar actas)
    try:
        from routes.actas import actas_bp
        app.register_blueprint(actas_bp)
    except Exception as e:
        print(f"⚠️ Actas (CRUD) no cargado: {e}")

    # 9. Generación de Actas (Patrones de Diseño: Template Method)
    try:
        from routes.acta_routes import acta_bp
        app.register_blueprint(acta_bp)
    except Exception as e:
        print(f"⚠️ Generación de Actas no cargado: {e}")

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