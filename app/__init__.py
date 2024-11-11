from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from .config import Config

# Khởi tạo các đối tượng
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo database
    db.init_app(app)

    # CORS configuration
    CORS(app, origins=Config.CORS_ORIGINS)

    # Swagger UI configuration
    swaggerui_blueprint = get_swaggerui_blueprint(
        Config.SWAGGER_URL,
        Config.API_URL,
        config={'app_name': "Food API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)

    # Đăng ký các blueprint (các route)
    from .routes import register_blueprints
    register_blueprints(app)

    return app
