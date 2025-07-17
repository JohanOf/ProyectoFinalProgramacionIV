# Importa las funciones necesarias de Flask para manejo de formularios y redirecciones
from flask import render_template, request, redirect, url_for, flash

# Importa las funciones de Flask-Login para manejar sesiones de usuario
from flask_login import login_user, logout_user, login_required, current_user

# Importa el modelo Usuario y la instancia de base de datos
from models.user_model import Usuario
from extensions import db

# Función para procesar el inicio de sesión de un usuario
def procesar_login():
    # Si el usuario ya está autenticado, redirige al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    # Si es una petición POST (envío del formulario)
    if request.method == 'POST':
        # Obtiene los datos del formulario
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Busca el usuario por email en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Verifica si el usuario existe y la contraseña es correcta
        if usuario and usuario.verificar_password(password):
            # Inicia sesión del usuario
            login_user(usuario)
            # Redirige a la página solicitada originalmente o al dashboard principal
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            # Muestra mensaje de error si las credenciales son incorrectas
            flash('Email o contraseña incorrectos', 'error')
    
    # Renderiza el formulario de login
    return render_template('auth/login.html')

# Función para procesar el registro de un nuevo usuario
def procesar_registro():
    # Si el usuario ya está autenticado, redirige al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    # Si es una petición POST (envío del formulario)
    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Verifica si el email ya está registrado
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El email ya está registrado', 'error')
            return render_template('auth/registro.html')
        
        # Crea un nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.establecer_password(password)
        
        # Guarda el usuario en la base de datos
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar el usuario', 'error')
    
    # Renderiza el formulario de registro
    return render_template('auth/registro.html')

# Función para cerrar sesión del usuario actual
def procesar_logout():
    # Cierra la sesión del usuario
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    # Redirige al login
    return redirect(url_for('auth.login'))
