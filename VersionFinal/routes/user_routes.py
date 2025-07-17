from flask import Blueprint, render_template
from flask_login import login_required
from controllers.user_controller import obtener_usuarios, saludar_usuario

user_bp = Blueprint("usuarios", __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return "Panel de control - Bienvenido al sistema de grafos"

@user_bp.route('/usuarios/')
@login_required
def listar_usuarios():
    return obtener_usuarios()

@user_bp.route('/saludo/<nombre>')
@login_required
def mostrar_saludo(nombre):
    return saludar_usuario(nombre)