from .calculate_routes import calculate_bp
from .data_routes import data_bp
from .analyze_routes import analyze_bp

def register_blueprints(app):
    app.register_blueprint(calculate_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(analyze_bp)
