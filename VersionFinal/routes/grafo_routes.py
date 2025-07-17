from flask import Blueprint, request
from flask_login import login_required
from controllers.grafo_controller import obtener_imagen_grafo, obtener_camino_predeterminado, procesar_formulario_camino

grafo_img_bp = Blueprint('grafo', __name__)
grafo_camino_bp = Blueprint('camino', __name__)
grafo_camino_buscar_bp = Blueprint('camino_buscar', __name__)

@grafo_img_bp.route('/grafo')
@login_required
def ver_grafo():
    return obtener_imagen_grafo()

@grafo_camino_bp.route('/camino')
@login_required
def ver_camino():
    return obtener_camino_predeterminado()


@grafo_camino_buscar_bp.route('/camino_formulario', methods=['GET', 'POST'])
@login_required
def camino_formulario():
    if request.method == 'POST':
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        return procesar_formulario_camino(origen, destino)
    else:
        return procesar_formulario_camino()

