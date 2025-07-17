from flask import Blueprint
from controllers.auth_controller import procesar_login, procesar_registro, procesar_logout

# Blueprint para las rutas de autenticación
auth_bp = Blueprint("auth", __name__)

# Ruta para mostrar y procesar el formulario de login
@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return procesar_login()

# Ruta para mostrar y procesar el formulario de registro
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    return procesar_registro()

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    return procesar_logout()