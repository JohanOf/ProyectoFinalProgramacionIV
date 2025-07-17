# Importa la clase SQLAlchemy, que permite usar un ORM (Object Relational Mapper)
# para interactuar con la base de datos en Flask de forma orientada a objetos
from flask_sqlalchemy import SQLAlchemy

# Importa LoginManager para manejar las sesiones de usuario y autenticación
from flask_login import LoginManager

# Crea una instancia global de SQLAlchemy llamada 'db'
# Esta instancia será compartida por todos los modelos y controladores que necesiten acceso a la base de datos
db = SQLAlchemy()

# Crea una instancia global de LoginManager para manejar la autenticación
# Esta instancia manejará las sesiones de usuario y protegerá las rutas que requieran login
login_manager = LoginManager()
