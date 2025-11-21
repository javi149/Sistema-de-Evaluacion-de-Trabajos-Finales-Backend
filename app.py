import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
from config.config import ConfiguracionGlobal
# Importamos el modelo para poder guardar cosas en la base de datos
from models.instituciones import Institucion

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

    # Registrar Rutas (Blueprints de Adán si existen)
    try:
        from routes.estudiantes import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    # --- RUTA PRINCIPAL (GET y POST) ---
    @app.route('/api/instituciones', methods=['GET', 'POST'])
    def gestionar_instituciones():
        if request.method == 'POST':
            # 1. Recibimos los datos que manda Postman
            data = request.get_json()
            
            # 2. Creamos la nueva institución
            try:
                nueva_inst = Institucion(
                    nombre=data.get('nombre'),
                    direccion=data.get('direccion'),
                    contacto=data.get('contacto')
                )
                
                # 3. Guardamos en Base de Datos
                db.session.add(nueva_inst)
                db.session.commit()
                
                return jsonify({'mensaje': 'Institución creada con éxito', 'id': nueva_inst.id}), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        # Si no es POST, entonces es GET (Devolver lista)
        lista = Institucion.query.all()
        resultado = []
        for inst in lista:
            resultado.append({
                'id': inst.id,
                'nombre': inst.nombre,
                'direccion': inst.direccion
            })
        return jsonify(resultado)

    # ¡ESTA ES LA LÍNEA QUE FALTABA! 
    return app

# --- Configuración Global ---
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)