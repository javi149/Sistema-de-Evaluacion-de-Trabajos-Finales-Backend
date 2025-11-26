import os
from flask import Flask, request, make_response
from flask_cors import CORS
from config.config import ConfiguracionGlobal
from database import db

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Función Auxiliar para construir la URL de la Base de Datos ---
def _build_db_uri():
    # 1. Si existe la URL completa en .env (Railway), úsala.
    direct_uri = os.getenv('DATABASE_URL')
    if direct_uri:
        return direct_uri

    # 2. Si no, intenta armarla con partes (Usuario, Pass, Host...)
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    driver = os.getenv('DB_DRIVER', 'mysql+mysqlconnector')

    if all([user, password, host, dbname]):
        port_section = f":{port}" if port else ""
    ConfiguracionGlobal()

    # --- REGISTRO DE RUTAS (BLUEPRINTS) ---
    
    # 1. Estudiantes
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception as e:
        print(f"⚠️ Estudiantes no cargado: {e}")

    # 2. Evaluadores
    try:
        from routes.evaluadores_routes import evaluadores_bp
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
        from routes.trabajos_routes import trabajos_bp
        app.register_blueprint(trabajos_bp)
    except Exception as e:
        print(f"⚠️ Trabajos no cargado: {e}")

    # 5. Criterios
    try:
        from routes.criterios import criterios_bp
        app.register_blueprint(criterios_bp)
    except Exception as e:
        print(f"⚠️ Criterios no cargado: {e}")

    # 6. Evaluaciones
    try:
        from routes.evaluaciones import evaluaciones_bp
        app.register_blueprint(evaluaciones_bp)
    except Exception as e:
        print(f"⚠️ Evaluaciones no cargado: {e}")

    # 7. Detalle de Evaluación
    try:
        from routes.evaluacion_detalle import evaluacion_detalle_bp
        app.register_blueprint(evaluacion_detalle_bp)
    except Exception as e:
        print(f"⚠️ Detalle Evaluación no cargado: {e}")

    # 8. Actas (CRUD y Generación)
    try:
        # Asegúrate de que este archivo maneje tanto el CRUD como la generación
        # O si tienes un 'acta_routes.py' separado, agrégalo abajo.
        from routes.actas import actas_bp
        app.register_blueprint(actas_bp)
    except Exception as e:
        print(f"⚠️ Actas no cargado: {e}")

    # 9. Cálculo de Notas
    try:
        from routes.notas_routes import notas_bp
        app.register_blueprint(notas_bp)
    except Exception as e:
        print(f"⚠️ Cálculo de Notas no cargado: {e}")

    # --------------------------------------------------

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

# --- Inicialización ---
app = crear_app()

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Mensaje de inicio prolijo
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print("\n" + "="*60)
    print("🚀  SISTEMA DE EVALUACIÓN - BACKEND INICIADO")
    print("="*60)
    print(f"📡  URL Local:   http://localhost:{port}")
    # Ocultamos la contraseña de la DB en el print por seguridad
    db_name = app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]
    print(f"🗄️   Base de Datos: {db_name}")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)