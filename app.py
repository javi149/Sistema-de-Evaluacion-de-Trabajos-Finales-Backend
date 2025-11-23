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

    # --- AQUÍ REGISTRAMOS LOS DEPARTAMENTOS (Rutas) ---
    
    # 1. Rutas de Instituciones (La que acabas de crear)
    try:
        from routes.instituciones import instituciones_bp
        app.register_blueprint(instituciones_bp)
    except Exception as e:
        print(f"Error importando instituciones: {e}")

    # 2. Rutas de Estudiantes (Ejemplo para Adán)
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    # --------------------------------------------------

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)