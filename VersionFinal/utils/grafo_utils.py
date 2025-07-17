import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io
from models.grafo_model import Ciudad, Ruta

# Construir el grafo dirigido y ponderado desde la base de datos
def construir_grafo():
    G = nx.DiGraph()
    
    # Si no hay datos en la BD, usar datos por defecto
    if Ciudad.query.count() == 0:
        _inicializar_datos_por_defecto()
    
    # Obtener todas las rutas de la base de datos
    rutas = Ruta.query.all()
    
    for ruta in rutas:
        origen = ruta.ciudad_origen_rel.nombre
        destino = ruta.ciudad_destino_rel.nombre
        costo = ruta.costo
        G.add_edge(origen, destino, weight=costo)
    
    return G

def _inicializar_datos_por_defecto():
    """Inicializa datos por defecto si la base de datos está vacía"""
    from extensions import db
    
    # Crear ciudades por defecto
    ciudades_data = [
        ('Ibarra', 'Imbabura', False),
        ('Quito', 'Pichincha', False),
        ('Santo Domingo', 'Santo Domingo de los Tsáchilas', False),
        ('Manta', 'Manabí', True),
        ('Portoviejo', 'Manabí', True),
        ('Guayaquil', 'Guayas', True),
        ('Cuenca', 'Azuay', False),
        ('Loja', 'Loja', False),
    ]
    
    ciudades_obj = {}
    for nombre, provincia, es_costera in ciudades_data:
        ciudad = Ciudad(nombre=nombre, provincia=provincia, es_costera=es_costera)
        db.session.add(ciudad)
        ciudades_obj[nombre] = ciudad
    
    db.session.commit()
    
    # Crear rutas por defecto
    rutas_data = [
        ('Ibarra', 'Quito', 10),
        ('Quito', 'Santo Domingo', 15),
        ('Quito', 'Manta', 30),
        ('Santo Domingo', 'Manta', 12),
        ('Manta', 'Portoviejo', 5),
        ('Portoviejo', 'Guayaquil', 20),
        ('Guayaquil', 'Cuenca', 25),
        ('Cuenca', 'Loja', 18),
        ('Quito', 'Cuenca', 35),
        ('Santo Domingo', 'Guayaquil', 22),
        ('Guayaquil', 'Loja', 40),
    ]
    
    for origen_nombre, destino_nombre, costo in rutas_data:
        origen = ciudades_obj[origen_nombre]
        destino = ciudades_obj[destino_nombre]
        ruta = Ruta(ciudad_origen_id=origen.id, ciudad_destino_id=destino.id, costo=costo)
        db.session.add(ruta)
    
    db.session.commit()

# Función para renderizar el grafo como imagen
def grafo_a_imagen(camino_resaltado=None):
    G = construir_grafo()
    pos = nx.spring_layout(G, seed=85)
    pesos = nx.get_edge_attributes(G, 'weight')

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Colores por defecto
    node_colors = []
    edge_colors = []
    edge_widths = []
    
    # Obtener ciudades costeras desde la BD
    ciudades_costeras = {c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()}
    
    # Colorear nodos
    for node in G.nodes():
        if camino_resaltado and node in camino_resaltado:
            if node in ciudades_costeras:
                node_colors.append('lightcoral')  # Costeras en el camino
            else:
                node_colors.append('lightgreen')  # No costeras en el camino
        else:
            if node in ciudades_costeras:
                node_colors.append('lightblue')   # Costeras fuera del camino
            else:
                node_colors.append('lightgray')   # No costeras fuera del camino
    
    # Colorear aristas
    for edge in G.edges():
        if camino_resaltado and _edge_in_path(edge, camino_resaltado):
            edge_colors.append('red')
            edge_widths.append(3)
        else:
            edge_colors.append('black')
            edge_widths.append(1)
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, 
            font_weight='bold', arrows=True, edge_color=edge_colors, width=edge_widths)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)
    
    # Agregar leyenda
    if camino_resaltado:
        plt.title(f"Grafo de Ciudades - Ruta: {' → '.join(camino_resaltado)}", fontsize=14, fontweight='bold')
    else:
        plt.title("Grafo de Ciudades del Ecuador", fontsize=14, fontweight='bold')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    plt.close()
    return buf

def _edge_in_path(edge, path):
    """Verifica si una arista está en el camino dado"""
    for i in range(len(path) - 1):
        if (edge[0] == path[i] and edge[1] == path[i + 1]):
            return True
    return False


def camino_optimo_con_costera(origen='Ibarra', destino='Loja'):
    G = construir_grafo()

    try:
        camino = nx.dijkstra_path(G, origen, destino, weight='weight')
        costo = nx.dijkstra_path_length(G, origen, destino, weight='weight')

        # Obtener ciudades costeras desde la BD
        ciudades_costeras = {c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()}
        contiene_costera = any(ciudad in ciudades_costeras for ciudad in camino)
        
        return {
            "camino": camino,
            "costo": costo,
            "valido": contiene_costera
        }
    except nx.NetworkXNoPath:
        return {
            "camino": [],
            "costo": None,
            "valido": False
        }


def obtener_ciudades():
    """Obtiene la lista de ciudades desde la base de datos"""
    if Ciudad.query.count() == 0:
        _inicializar_datos_por_defecto()
    
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    return [ciudad.nombre for ciudad in ciudades]

def obtener_provincias():
    """Obtiene la lista de provincias únicas desde la base de datos"""
    if Ciudad.query.count() == 0:
        _inicializar_datos_por_defecto()
    
    from extensions import db
    provincias = db.session.query(Ciudad.provincia).distinct().order_by(Ciudad.provincia).all()
    return [provincia[0] for provincia in provincias]
