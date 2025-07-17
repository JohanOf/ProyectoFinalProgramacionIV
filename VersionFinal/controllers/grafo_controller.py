# Importa las funciones para renderizar plantillas HTML
from flask import render_template, send_file, request

# Importa las funciones de utilidades de grafos
from utils.grafo_utils import grafo_a_imagen, camino_optimo_con_costera, obtener_ciudades

# Función que genera y envía la imagen del grafo
# Utiliza NetworkX y Matplotlib para crear una visualización del grafo de ciudades
def obtener_imagen_grafo():
    # Verificar si se solicita resaltar un camino específico
    camino_param = request.args.get('camino')
    camino_resaltado = None
    
    if camino_param:
        try:
            # El camino viene como string separado por comas
            camino_resaltado = camino_param.split(',')
        except:
            camino_resaltado = None
    
    img = grafo_a_imagen(camino_resaltado)
    return send_file(img, mimetype='image/png')

# Función que calcula y muestra el camino predeterminado de Ibarra a Loja
# Usa el algoritmo de Dijkstra para encontrar el camino más corto
def obtener_camino_predeterminado():
    resultado = camino_optimo_con_costera()
    return render_template("grafo/camino.html", resultado=resultado)

# Función que procesa el formulario para buscar caminos personalizados
# Permite al usuario seleccionar origen y destino, luego calcula la ruta óptima
def procesar_formulario_camino(origen=None, destino=None):
    ciudades = obtener_ciudades()
    resultado = None

    # Si se proporcionan origen y destino, calcula la ruta
    if origen and destino and origen != destino:
        resultado = camino_optimo_con_costera(origen, destino)

    return render_template("grafo/formulario.html", ciudades=ciudades, resultado=resultado)