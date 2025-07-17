# Importa la instancia de SQLAlchemy desde el archivo extensions.py
from extensions import db

# Importa UserMixin para agregar métodos requeridos por Flask-Login
from flask_login import UserMixin


# Define el modelo 'Usuario', que representará la tabla 'usuario' en la base de datos
# UserMixin proporciona implementaciones por defecto para is_authenticated, is_active, is_anonymous y get_id
class Usuario(UserMixin, db.Model):
    # Columna 'id' será la clave primaria y se autoincrementa automáticamente
    id = db.Column(db.Integer, primary_key=True)
    
    # Columna 'nombre' almacenará texto de hasta 100 caracteres, y no puede ser nula
    nombre = db.Column(db.String(100), nullable=False)
    
    # Columna 'email' almacenará texto de hasta 120 caracteres, debe ser único y no nulo
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Columna 'password_hash' almacenará la contraseña hasheada de hasta 255 caracteres
    password_hash = db.Column(db.String(100), nullable=False)
    
    # Método para establecer la contraseña del usuario de forma segura
    def establecer_password(self, password):
        self.password_hash = password  
    
    # Método para verificar si una contraseña coincide 
    def verificar_password(self, password):
        return self.password_hash == password 
    
    # Representación en cadena del objeto Usuario (útil para debugging)
    def __repr__(self):
        return f'<Usuario {self.nombre}>'
