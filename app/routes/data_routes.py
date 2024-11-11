from flask import Blueprint, jsonify, request
from services.OptimizeService import scale

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/data', methods=['GET'])
def get_data():
    # Retrieve query parameters
    calo = float(request.args.get('calo', '0').replace(",", "."))
    protein = float(request.args.get('protein', '0').replace(",", "."))
    fat = float(request.args.get('fat', '0').replace(",", "."))
    sat_fat = float(request.args.get('sat_fat', '0').replace(",", "."))
    fiber = float(request.args.get('fiber', '0').replace(",", "."))
    carb = float(request.args.get('carb', '0').replace(",", "."))

    result = scale(calo, protein, fat, sat_fat, fiber, carb)
    return jsonify(result)
