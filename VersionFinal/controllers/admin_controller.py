from flask import render_template, redirect, url_for, flash
from models.grafo_model import Ciudad, Ruta
from extensions import db
from utils.grafo_utils import obtener_provincias


def gestionar_ciudades():
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    provincias = obtener_provincias()
    return render_template('admin/ciudades.html', ciudades=ciudades, provincias=provincias)

def agregar_ciudad(nombre, provincia, es_costera):
    if not nombre or not provincia:
        flash('Nombre y provincia son requeridos', 'error')
        return redirect(url_for('admin.ciudades'))
    
    # Verificar si la ciudad ya existe
    if Ciudad.query.filter_by(nombre=nombre).first():
        flash(f'La ciudad {nombre} ya existe', 'error')
        return redirect(url_for('admin.ciudades'))
    
    try:
        nueva_ciudad = Ciudad(nombre=nombre, provincia=provincia, es_costera=es_costera)
        db.session.add(nueva_ciudad)
        db.session.commit()
        flash(f'Ciudad {nombre} agregada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar la ciudad: {str(e)}', 'error')
    
    return redirect(url_for('admin.ciudades'))

def eliminar_ciudad(ciudad_id):
    ciudad = Ciudad.query.get_or_404(ciudad_id)
    
    # Verificar si la ciudad tiene rutas asociadas
    rutas_origen = Ruta.query.filter_by(ciudad_origen_id=ciudad_id).count()
    rutas_destino = Ruta.query.filter_by(ciudad_destino_id=ciudad_id).count()
    
    if rutas_origen > 0 or rutas_destino > 0:
        flash(f'No se puede eliminar {ciudad.nombre} porque tiene rutas asociadas', 'error')
        return redirect(url_for('admin.ciudades'))
    
    try:
        db.session.delete(ciudad)
        db.session.commit()
        flash(f'Ciudad {ciudad.nombre} eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la ciudad: {str(e)}', 'error')
    
    return redirect(url_for('admin.ciudades'))

def gestionar_rutas():
    rutas = Ruta.query.all()
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    return render_template('admin/rutas.html', rutas=rutas, ciudades=ciudades)

def agregar_ruta(ciudad_origen_id, ciudad_destino_id, costo):
    if not ciudad_origen_id or not ciudad_destino_id or not costo:
        flash('Todos los campos son requeridos', 'error')
        return redirect(url_for('admin.rutas'))
    
    if ciudad_origen_id == ciudad_destino_id:
        flash('La ciudad de origen y destino no pueden ser la misma', 'error')
        return redirect(url_for('admin.rutas'))
    
    # Verificar si la ruta ya existe
    ruta_existente = Ruta.query.filter_by(
        ciudad_origen_id=ciudad_origen_id, 
        ciudad_destino_id=ciudad_destino_id
    ).first()
    
    if ruta_existente:
        flash('Esta ruta ya existe', 'error')
        return redirect(url_for('admin.rutas'))
    
    try:
        costo = float(costo)
        if costo <= 0:
            flash('El costo debe ser mayor a 0', 'error')
            return redirect(url_for('admin.rutas'))
        
        nueva_ruta = Ruta(
            ciudad_origen_id=ciudad_origen_id,
            ciudad_destino_id=ciudad_destino_id,
            costo=costo
        )
        db.session.add(nueva_ruta)
        db.session.commit()
        flash('Ruta agregada exitosamente', 'success')
    except ValueError:
        flash('El costo debe ser un número válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar la ruta: {str(e)}', 'error')
    
    return redirect(url_for('admin.rutas'))

def eliminar_ruta(ruta_id):
    ruta = Ruta.query.get_or_404(ruta_id)
    
    try:
        db.session.delete(ruta)
        db.session.commit()
        flash('Ruta eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la ruta: {str(e)}', 'error')
    
    return redirect(url_for('admin.rutas'))
