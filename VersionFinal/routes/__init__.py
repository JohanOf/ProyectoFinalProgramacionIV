from .home_routes import home_bp
from .user_routes import user_bp
from .general_routes import auth_bp
from .grafo_routes import grafo_img_bp, grafo_camino_bp, grafo_camino_buscar_bp
from .admin_routes import admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(grafo_img_bp)
    app.register_blueprint(grafo_camino_bp)
    app.register_blueprint(grafo_camino_buscar_bp)
    app.register_blueprint(admin_bp)