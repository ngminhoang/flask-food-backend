import os

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename

from repositories.Ingredient import Ingredient, db
from services.DetectImageService import analyze_image
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

CORS(app, origins=["http://localhost:3000"])


@app.route('/')
def hello_world():
    return 'Hello World!'




@app.route('/api/calculate_by_body', methods=['GET'])
def calculate_nutrition():
    # Lấy dữ liệu từ request, đảm bảo chuyển đổi đúng định dạng
    weight_kg = float(request.args.get('weight_kg', '0').replace(",", "."))
    height_cm = float(request.args.get('height_cm', '0').replace(",", "."))
    age = float(request.args.get('age', '0').replace(",", "."))
    gender = request.args.get('gender', 'male').lower()  # 'male' or 'female'
    activity_level = request.args.get('activity_level', 'moderately_active').lower()

    # BMR calculation based on gender using Mifflin-St Jeor
    if gender == "male":
        BMR = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender == "female":
        BMR = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        return jsonify({"error": "Gender should be 'male' or 'female'."}), 400

    # Hệ số hoạt động cho TDEE
    activity_multipliers = {
        "sedentary": 1.2,              # ít hoạt động hoặc không vận động
        "lightly_active": 1.375,       # hoạt động nhẹ nhàng, tập 1-3 buổi/tuần
        "moderately_active": 1.55,     # vận động vừa, tập 3-5 buổi/tuần
        "very_active": 1.725,          # vận động nhiều, tập 6-7 buổi/tuần
        "super_active": 1.9            # vận động cực nhiều (vận động viên, công việc nặng)
    }

    if activity_level not in activity_multipliers:
        return jsonify({"error": "Invalid activity level. Choose from 'sedentary', 'lightly_active', 'moderately_active', 'very_active', or 'super_active'."}), 400

    # TDEE: Tổng năng lượng tiêu thụ hàng ngày
    TDEE = BMR * activity_multipliers[activity_level]

    # Phân bố Macronutrients (carbs, protein, fat)
    # Giả định:
    # 20-30% protein, 45-65% carbohydrate, và 20-35% fat (phổ biến theo các tiêu chuẩn dinh dưỡng)

    # Tỉ lệ dinh dưỡng cơ bản
    protein_ratio = 0.25  # 25% calories từ protein
    carb_ratio = 0.50     # 50% calories từ carbs
    fat_ratio = 0.25      # 25% calories từ fat

    # Tính toán khối lượng từng chất
    # 1g protein = 4 cal, 1g carb = 4 cal, 1g fat = 9 cal
    protein = (protein_ratio * TDEE) / 4   # g protein
    carbs = (carb_ratio * TDEE) / 4        # g carbohydrate
    fats = (fat_ratio * TDEE) / 9          # g fat

    # Saturated fats = 10% of total calories, converted to grams
    sat_fat = (0.1 * TDEE) / 9  # 10% calories từ chất béo bão hòa

    # Lượng chất xơ khuyến nghị: 38g cho nam và 25g cho nữ
    fiber = 38 if gender == "male" else 25

    # Tạo kết quả trả về
    print({
        "BMI": weight_kg / (height_cm / 100) ** 2,
        "BMR (calories)": BMR,
        "TDEE (calories)": TDEE,
        "Protein (g)": protein,
        "Carbohydrates (g)": carbs,
        "Fats (g)": fats,
        "Saturated Fat (g)": sat_fat,
        "Fiber (g)": fiber
    })

    # return jsonify(result)


    result = scale(TDEE, protein, fats, sat_fat, fiber, carbs)
    return jsonify(result)



@app.route('/api/data', methods=['GET'])
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

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Get the API key
    api_key = "4VQKUVUF.lEnStEKIxQVQLLYZEhc24kpiNaQTI3SA"

    # Check if an image file is included in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    # Get the image from the request
    image = request.files['image']
    filename = secure_filename(image.filename)

    # Set up the temporary directory
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    image_path = os.path.join(tmp_dir, filename)
    image.save(image_path)

    # Call the analyze_image function
    try:
        result = analyze_image(api_key, image_path)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Optionally, remove the image after processing if not needed
        if os.path.exists(image_path):
            os.remove(image_path)



if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development
