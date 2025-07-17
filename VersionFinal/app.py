# Importa la clase Flask para crear la aplicación web
from flask import Flask

# Importa la configuración desde el archivo config.py (lee las variables de entorno)
from config import Config

# Importa las instancias de SQLAlchemy y LoginManager desde extensions.py
from extensions import db, login_manager

# Importa la función para registrar los blueprints de las rutas
from routes import register_blueprints


# Función de fábrica para crear y configurar la aplicación Flask
def create_app():
    # Crea una instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Carga la configuración desde la clase Config (incluye conexión a base de datos)
    app.config.from_object(Config)

    # Inicializa la extensión de SQLAlchemy con la app
    db.init_app(app)
    
    # Inicializa LoginManager con la app
    login_manager.init_app(app)
    
    # Configura la vista de login para redireccionar usuarios no autenticados
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Función para cargar usuario desde la base de datos (requerida por Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        from models.user_model import Usuario
        return Usuario.query.get(int(user_id))

    # Importa y registra los blueprints de las rutas
    register_blueprints(app)

    # Devuelve la aplicación completamente configurada
    return app

# Crea la aplicación usando la función de fábrica
app = create_app()

# Ejecuta la aplicación si se llama directamente este archivo
if __name__ == '__main__':
    # Inicia el servidor en modo debug (útil para desarrollo)
    app.run(debug=True)
