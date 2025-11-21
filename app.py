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

    # Habilitar CORS para que Katy pueda conectarse
    CORS(app)

    # Configuración de Base de Datos
    db_uri = os.getenv('DATABASE_URL')
    if not db_uri:
        # Fallback por si falla la variable de entorno
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluacion.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ConfiguracionGlobal()

    # Registrar Rutas
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}
    
    # Agregamos ruta de prueba de instituciones
    from flask import jsonify
    from models.institucion import Institucion
    @app.route('/api/instituciones', methods=['GET'])
    def obtener_instituciones():
        try:
            lista = Institucion.query.all()
            resultado = []
            for inst in lista:
                resultado.append({
                    'id': inst.id,
                    'nombre': inst.nombre,
                    'direccion': inst.direccion
                })
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# --- CAMBIO IMPORTANTE AQUÍ ABAJO ---

# 1. Creamos la app AQUÍ AFUERA (Globalmente) para que Gunicorn la vea
app = create_app()

# 2. Opcional: Aseguramos que las tablas existan al iniciar
with app.app_context():
    db.create_all()

# 3. El bloque main solo se usa para correr en local
if __name__ == "__main__":
    app.run(debug=True)