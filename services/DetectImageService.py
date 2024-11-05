from re import search
from typing import List

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.FoodVisorResponse import AnalysisResponse, Position, Nutrition, FoodInfo, Food, Item

# Initialize Flask and SQLAlchemy instances
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5437/food-db'
db = SQLAlchemy(app)

# Ingredient model with a unique constraint on 'name' and the to_dict() method
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Unique constraint for name
    nu_grams = db.Column(db.Float)
    nu_calories = db.Column(db.Float)
    nu_proteins = db.Column(db.Float)
    nu_carbs = db.Column(db.Float)
    nu_fibers = db.Column(db.Float)
    nu_fats = db.Column(db.Float)
    nu_sat_fats = db.Column(db.Float)
    nu_price = db.Column(db.Float)
    search_status = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nu_grams': self.nu_grams,
            'nu_calories': self.nu_calories,
            'nu_proteins': self.nu_proteins,
            'nu_carbs': self.nu_carbs,
            'nu_fibers': self.nu_fibers,
            'nu_fats': self.nu_fats,
            'nu_sat_fats': self.nu_sat_fats,
            'nu_price': self.nu_price,
            'search_status': self.search_status
        }

# Parsing function that checks and adds ingredients if they don't exist in the database
def parse_analysis_response(data: dict) -> AnalysisResponse:
    analysis_id = data.get('analysis_id', '')
    scopes = data.get('scopes', [])
    items = []

    for item_data in data.get('items', []):
        # Process position information
        position_data = item_data.get('position', {})
        position = Position(
            x=position_data.get('x', 0),
            y=position_data.get('y', 0),
            width=position_data.get('width', 0),
            height=position_data.get('height', 0)
        )

        # Process food items
        food_list = []
        for food_data in item_data.get('food', []):
            # Extract nutrition data
            nutrition_data = food_data.get('food_info', {}).get('nutrition', {})
            total_nutrition = Nutrition(
                alcohol_100g=nutrition_data.get('alcohol_100g', 0),
                calcium_100g=nutrition_data.get('calcium_100g', 0),
                calories_100g=nutrition_data.get('calories_100g', 0),
                carbs_100g=nutrition_data.get('carbs_100g', 0),
                cholesterol_100g=nutrition_data.get('cholesterol_100g', 0),
                fat_100g=nutrition_data.get('fat_100g', 0),
                fibers_100g=nutrition_data.get('fibers_100g', 0),
                proteins_100g=nutrition_data.get('proteins_100g', 0),
                sugars_100g=nutrition_data.get('sugars_100g', 0),
                vitamin_c_100g=nutrition_data.get('vitamin_c_100g', 0)
            )

            for ingredient_data in food_data.get('ingredients', []):
                nutrition_data = ingredient_data.get('food_info', {}).get('nutrition', {})
                nutrition = Nutrition(
                    alcohol_100g=nutrition_data.get('alcohol_100g', 0),
                    calcium_100g=nutrition_data.get('calcium_100g', 0),
                    calories_100g=nutrition_data.get('calories_100g', 0),
                    carbs_100g=nutrition_data.get('carbs_100g', 0),
                    cholesterol_100g=nutrition_data.get('cholesterol_100g', 0),
                    fat_100g=nutrition_data.get('fat_100g', 0),
                    fibers_100g=nutrition_data.get('fibers_100g', 0),
                    proteins_100g=nutrition_data.get('proteins_100g', 0),
                    sugars_100g=nutrition_data.get('sugars_100g', 0),
                    vitamin_c_100g=nutrition_data.get('vitamin_c_100g', 0)
                )


                # Get the ingredient name
                ingredient_name = ingredient_data.get('food_info', {}).get("display_name", "Unknown")

                # Use Flask app context for database operations
                with app.app_context():
                    # Ensure ingredient_name is a string
                    if isinstance(ingredient_name, str):
                        # Check if the ingredient exists
                        existing_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()

                        # If the ingredient doesn't exist, add it
                        if not existing_ingredient:
                            new_ingredient = Ingredient(
                                name=ingredient_name,
                                nu_grams=100,  # Assuming grams per serving as default
                                nu_calories=nutrition.calories_100g,
                                nu_proteins=nutrition.proteins_100g,
                                nu_carbs=nutrition.carbs_100g,
                                nu_fibers=nutrition.fibers_100g,
                                nu_fats=nutrition.fat_100g,
                                nu_sat_fats=nutrition.fat_100g,  # Adjust based on actual sat_fat field if exists
                                nu_price=None,  # Replace with actual price if available
                                search_status = 2
                            )
                            db.session.add(new_ingredient)
                            db.session.commit()
                        else:
                            print(f"Ingredient '{ingredient_name}' already exists in the database.")


            # Create the FoodInfo and Food objects
            food_info_data = food_data.get('food_info', {})
            food_info = FoodInfo(
                food_id=food_info_data.get('food_id', ''),
                fv_grade=food_info_data.get('fv_grade', ''),
                g_per_serving=food_info_data.get('g_per_serving', 0),
                display_name=food_info_data.get('display_name', ''),
                nutrition=total_nutrition
            )

            food = Food(
                confidence=food_data.get('confidence', 0),
                quantity=food_data.get('quantity', 0),
                ingredients=food_data.get('ingredients', []),
                food_info=food_info
            )
            food_list.append(food)

        # Create the Item object
        item = Item(position=position, food=food_list)
        items.append(item)

    # Return the fully parsed AnalysisResponse
    return AnalysisResponse(analysis_id=analysis_id, scopes=scopes, items=items)

# Sử dụng hàm trong analyze_image
def analyze_image(api_key, image_path):
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": f"Api-Key {api_key}"}

    with open(image_path, "rb") as image:
        response = requests.post(url, headers=headers, files={"image": image})
        response.raise_for_status()

    # Chuyển đổi dữ liệu JSON thành đối tượng AnalysisResponse
    analysis_response = parse_analysis_response(response.json())
    return analysis_response.to_dict()


#
# def parse_analysis_response(data: dict) -> AnalysisResponse:
#     analysis_id = data.get('analysis_id', '')
#     scopes = data.get('scopes', [])
#     items = []
#
#     for item_data in data.get('items', []):
#         position_data = item_data.get('position', {})
#         position = Position(
#             x=position_data.get('x', 0),
#             y=position_data.get('y', 0),
#             width=position_data.get('width', 0),
#             height=position_data.get('height', 0)
#         )
#
#         food_list = []
#         for food_data in item_data.get('food', []):
#             nutrition_data = food_data.get('food_info', {}).get('nutrition', {})
#             nutrition = Nutrition(
#                 alcohol_100g=nutrition_data.get('alcohol_100g', 0),
#                 calcium_100g=nutrition_data.get('calcium_100g', 0),
#                 calories_100g=nutrition_data.get('calories_100g', 0),
#                 carbs_100g=nutrition_data.get('carbs_100g', 0),
#                 cholesterol_100g=nutrition_data.get('cholesterol_100g', 0),
#                 fat_100g=nutrition_data.get('fat_100g', 0),
#                 fibers_100g=nutrition_data.get('fibers_100g', 0),
#                 proteins_100g=nutrition_data.get('proteins_100g', 0),
#                 sugars_100g=nutrition_data.get('sugars_100g', 0),
#                 vitamin_c_100g=nutrition_data.get('vitamin_c_100g', 0)
#             )
#
#             # Kiểm tra và thêm vào DB
#             ingredient_name = food_data.get('ingredients', [])[0] if food_data.get('ingredients') else "Unknown"
#             existing_ingredient = Ingradient.query.filter_by(name=ingredient_name).first()
#
#             if not existing_ingredient:
#                 # Nếu không tồn tại, tạo mới
#                 new_ingredient = Ingradient(
#                     name=ingredient_name,
#                     nuGrams=nutrition.nuGrams,  # Giả định bạn có trường này trong Nutrition
#                     nuCalories=nutrition.calories_100g,
#                     nuProteins=nutrition.proteins_100g,
#                     nuCarbs=nutrition.carbs_100g,
#                     nuFibers=nutrition.fibers_100g,
#                     nuFats=nutrition.fat_100g,
#                     nuSatFats=nutrition.satFats,  # Giả định bạn có trường này trong Nutrition
#                     nuPrice=None  # Thay thế với giá nếu có
#                 )
#                 db.session.add(new_ingredient)
#
#             food_info_data = food_data.get('food_info', {})
#             food_info = FoodInfo(
#                 food_id=food_info_data.get('food_id', ''),
#                 fv_grade=food_info_data.get('fv_grade', ''),
#                 g_per_serving=food_info_data.get('g_per_serving', 0),
#                 display_name=food_info_data.get('display_name', ''),
#                 nutrition=nutrition
#             )
#
#             food = Food(
#                 confidence=food_data.get('confidence', 0),
#                 quantity=food_data.get('quantity', 0),
#                 ingredients=food_data.get('ingredients', []),
#                 food_info=food_info
#             )
#             food_list.append(food)
#
#         item = Item(position=position, food=food_list)
#         items.append(item)
#
#     # Lưu tất cả các thay đổi vào DB
#     db.session.commit()
#
#     return AnalysisResponse(analysis_id=analysis_id, scopes=scopes, items=items)
