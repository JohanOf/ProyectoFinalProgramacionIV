from extensions import db

class Ciudad(db.Model):
    __tablename__ = 'ciudades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    provincia = db.Column(db.String(100), nullable=False)
    es_costera = db.Column(db.Boolean, default=False)
    
    # Relaciones
    rutas_origen = db.relationship('Ruta', foreign_keys='Ruta.ciudad_origen_id', backref='ciudad_origen_rel')
    rutas_destino = db.relationship('Ruta', foreign_keys='Ruta.ciudad_destino_id', backref='ciudad_destino_rel')
    
    def __repr__(self):
        return f'<Ciudad {self.nombre}>'

class Ruta(db.Model):
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    ciudad_origen_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    ciudad_destino_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Ruta {self.ciudad_origen_rel.nombre} -> {self.ciudad_destino_rel.nombre}: {self.costo}>'