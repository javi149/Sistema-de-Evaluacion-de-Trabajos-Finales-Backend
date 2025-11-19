import os
from flask import Flask
from flask_cors import CORS  # <--- NUEVO IMPORT
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

    # Habilitar CORS para que Katy pueda conectarse
    CORS(app)  # <--- NUEVA LÍNEA MÁGICA

    # Configuración de Base de Datos
    db_uri = os.getenv('DATABASE_URL')
    if not db_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluacion.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()

    # Registrar Rutas (Lo de Adán)
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)