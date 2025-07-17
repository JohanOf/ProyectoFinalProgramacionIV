from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Si el usuario está autenticado, redirige al home
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    # Si no está autenticado, redirige al login
    return redirect(url_for('auth.login'))

@home_bp.route('/home')
@login_required
def home():
    return render_template("home/bienvenida.html")