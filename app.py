from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from repositories.Ingredient import Ingredient, db
from services.OptimizeService import scale

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/api-docs'  # Point to your Swagger JSON or YAML

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Food API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5437/food-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    # Retrieve query parameters
    calo = request.args.get('calo', type=float)
    protein = request.args.get('protein', type=float)
    fat = request.args.get('fat', type=float)
    sat_fat = request.args.get('sat_fat', type=float)
    fiber = request.args.get('fiber', type=float)
    carb = request.args.get('carb', type=float)

    result = scale(calo, protein, fat, sat_fat, fiber, carb)
    return jsonify(result)

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development
