from app import app, db
from sqlalchemy import text  # Importamos esto para enviar comandos directos

def reiniciar_base_de_datos():
    print("⏳ Conectando a la base de datos...")
    
    with app.app_context():
        try:
            # 1. Desactivar el chequeo de llaves foráneas (La seguridad)
            print("🔓 Desactivando seguridad de llaves foráneas...")
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
            db.session.commit()

            # 2. Borrar TODO (Ahora sí nos dejará borrar padres e hijos)
            print("🗑️  Eliminando todas las tablas...")
            db.drop_all()
            
            # 3. Crear TODO de nuevo
            print("✨ Creando tablas nuevas...")
            db.create_all()

            # 4. Volver a activar la seguridad
            print("🔒 Reactivando seguridad...")
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
            db.session.commit()
            
            print("✅ ¡ÉXITO TOTAL! La base de datos está limpia y lista.")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    reiniciar_base_de_datos()