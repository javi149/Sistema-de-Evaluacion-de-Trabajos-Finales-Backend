import os

# Estructura de carpetas y archivos para el Proyecto Opción B
structure = {
    "config": {
        "config.py": """class ConfiguracionGlobal:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.APP_NAME = "Sistema de Evaluación de Trabajos Finales"
            cls._instance.VERSION = "1.0"
            cls._instance.INSTITUCION = "Universidad Ejemplo"
        return cls._instance
"""
    },
    "models": {
        "__init__.py": "from .estudiante import Estudiante\nfrom .trabajo import Trabajo",
        "estudiante.py": """from database import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    carrera = db.Column(db.String(120))
""",
        "trabajo.py": """from database import db

class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    tipo = db.Column(db.String(100)) # Tesis, Proyecto, etc.
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'))
"""
    },
    "routes": {
        "__init__.py": "",
        "estudiantes.py": """from flask import Blueprint, jsonify
from models import Estudiante

estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

@estudiantes_bp.route('/', methods=['GET'])
def listar_estudiantes():
    # Retorna lista vacia o datos si existen
    alumnos = Estudiante.query.all()
    resultado = [{"id": a.id, "nombre": a.nombre, "carrera": a.carrera} for a in alumnos]
    return jsonify(resultado)
"""
    },
    "factories": {},
    "strategies": {},
    "templates_methods": {},
    "static": {},
    "": { # Archivos en la raiz
        "app.py": """import os
from flask import Flask
from database import db
from config.config import ConfiguracionGlobal
from routes.estudiantes import estudiantes_bp

# Intentar cargar dotenv si existe, sino continuar
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def crear_app():
    app = Flask(__name__)
    
    # Configuración de Base de Datos (Prioridad: MySQL via .env, sino SQLite local)
    db_uri = os.getenv('DATABASE_URL')
    if db_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluacion.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Inicializar Singleton de Configuración
    ConfiguracionGlobal()

    # Registrar Rutas
    app.register_blueprint(estudiantes_bp)

    @app.route("/ping")
    def ping():
        return {"msg": "pong", "status": "ok"}

    return app

if __name__ == "__main__":
    app = crear_app()
    with app.app_context():
        db.create_all() # Crea las tablas vacias si no existen
    app.run(debug=True)
""",
        "database.py": """from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
""",
        "requirements.txt": """flask
flask_sqlalchemy
python-dotenv
mysql-connector-python
""",
        ".gitignore": """venv/
__pycache__/
*.pyc
.env
instance/
*.sqlite3
*.db
""",
        "README.md": """# Sistema de Evaluación de Trabajos Finales

Proyecto para la gestión de tesis y trabajos de grado.

## Ejecución
1. Crear entorno virtual: `python -m venv venv`
2. Activar entorno.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python app.py`
"""
    }
}

def crear_estructura(ruta_base, estructura):
    for nombre, contenido in estructura.items():
        ruta = os.path.join(ruta_base, nombre)
        if isinstance(contenido, dict):
            if not os.path.exists(ruta):
                os.makedirs(ruta)
            crear_estructura(ruta, contenido)
        else:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"Creado archivo: {ruta}")

if __name__ == "__main__":
    crear_estructura(".", structure)
    print("¡Estructura del proyecto generada con éxito!")