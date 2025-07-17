from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from controllers.admin_controller import (
    gestionar_ciudades, agregar_ciudad, eliminar_ciudad,
    gestionar_rutas, agregar_ruta, eliminar_ruta
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/ciudades')
@login_required
def ciudades():
    return gestionar_ciudades()

@admin_bp.route('/ciudades/agregar', methods=['POST'])
@login_required
def agregar_ciudad_route():
    nombre = request.form.get('nombre')
    provincia = request.form.get('provincia')
    es_costera = request.form.get('es_costera') == 'on'
    return agregar_ciudad(nombre, provincia, es_costera)

@admin_bp.route('/ciudades/eliminar/<int:ciudad_id>', methods=['POST'])
@login_required
def eliminar_ciudad_route(ciudad_id):
    return eliminar_ciudad(ciudad_id)

@admin_bp.route('/rutas')
@login_required
def rutas():
    return gestionar_rutas()

@admin_bp.route('/rutas/agregar', methods=['POST'])
@login_required
def agregar_ruta_route():
    ciudad_origen_id = request.form.get('ciudad_origen_id')
    ciudad_destino_id = request.form.get('ciudad_destino_id')
    costo = request.form.get('costo')
    return agregar_ruta(ciudad_origen_id, ciudad_destino_id, costo)

@admin_bp.route('/rutas/eliminar/<int:ruta_id>', methods=['POST'])
@login_required
def eliminar_ruta_route(ruta_id):
    return eliminar_ruta(ruta_id)
