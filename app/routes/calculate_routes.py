from flask import Blueprint, jsonify, request
from services.OptimizeService import scale

calculate_bp = Blueprint('calculate', __name__)

@calculate_bp.route('/api/calculate_by_body', methods=['GET'])
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