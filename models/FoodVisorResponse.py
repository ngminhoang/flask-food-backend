from typing import List


class AnalysisResponse:
    def __init__(self, analysis_id: str, scopes: List[str], items: List['Item']):
        self.analysis_id = analysis_id
        self.scopes = scopes
        self.items = items

    def to_dict(self):
        return {
            'analysis_id': self.analysis_id,
            'scopes': self.scopes,
            'items': [item.to_dict() for item in self.items]
        }

class Item:
    def __init__(self, position: 'Position', food: List['Food']):
        self.position = position
        self.food = food

    def to_dict(self):
        return {
            'position': self.position.to_dict(),
            'food': [food.to_dict() for food in self.food]
        }

class Position:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

class Food:
    def __init__(self, confidence: float, quantity: float, ingredients: List[str], food_info: 'FoodInfo'):
        self.confidence = confidence
        self.quantity = quantity
        self.ingredients = ingredients
        self.food_info = food_info

    def to_dict(self):
        return {
            'confidence': self.confidence,
            'quantity': self.quantity,
            'ingredients': self.ingredients,
            'food_info': self.food_info.to_dict()
        }

class FoodInfo:
    def __init__(self, food_id: str, fv_grade: str, g_per_serving: float, display_name: str, nutrition: 'Nutrition'):
        self.food_id = food_id
        self.fv_grade = fv_grade
        self.g_per_serving = g_per_serving
        self.display_name = display_name
        self.nutrition = nutrition

    def to_dict(self):
        return {
            'food_id': self.food_id,
            'fv_grade': self.fv_grade,
            'g_per_serving': self.g_per_serving,
            'display_name': self.display_name,
            'nutrition': self.nutrition.to_dict()
        }

class Nutrition:
    def __init__(self, alcohol_100g: float, calcium_100g: float, calories_100g: float, carbs_100g: float,
                 cholesterol_100g: float, fat_100g: float, fibers_100g: float, proteins_100g: float,
                 sugars_100g: float, vitamin_c_100g: float):
        self.alcohol_100g = alcohol_100g
        self.calcium_100g = calcium_100g
        self.calories_100g = calories_100g
        self.carbs_100g = carbs_100g
        self.cholesterol_100g = cholesterol_100g
        self.fat_100g = fat_100g
        self.fibers_100g = fibers_100g
        self.proteins_100g = proteins_100g
        self.sugars_100g = sugars_100g
        self.vitamin_c_100g = vitamin_c_100g

    def to_dict(self):
        return {
            'alcohol_100g': self.alcohol_100g,
            'calcium_100g': self.calcium_100g,
            'calories_100g': self.calories_100g,
            'carbs_100g': self.carbs_100g,
            'cholesterol_100g': self.cholesterol_100g,
            'fat_100g': self.fat_100g,
            'fibers_100g': self.fibers_100g,
            'proteins_100g': self.proteins_100g,
            'sugars_100g': self.sugars_100g,
            'vitamin_c_100g': self.vitamin_c_100g
        }

from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingradient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    nuGrams = db.Column(db.Float, nullable=True)
    nuCalories = db.Column(db.Float, nullable=True)
    nuProteins = db.Column(db.Float, nullable=True)
    nuCarbs = db.Column(db.Float, nullable=True)
    nuFibers = db.Column(db.Float, nullable=True)
    nuFats = db.Column(db.Float, nullable=True)
    nuSatFats = db.Column(db.Float, nullable=True)
    nuPrice = db.Column(db.Float, nullable=True)
    search_status = db.Column(db.Integer, default=0)  # Default to 0 (PENDING)

    def __init__(self, name, nuGrams=None, nuCalories=None, nuProteins=None, nuCarbs=None, nuFibers=None,
                 nuFats=None, nuSatFats=None, nuPrice=None):
        self.name = name
        self.nuGrams = nuGrams
        self.nuCalories = nuCalories
        self.nuProteins = nuProteins
        self.nuCarbs = nuCarbs
        self.nuFibers = nuFibers
        self.nuFats = nuFats
        self.nuSatFats = nuSatFats
        self.nuPrice = nuPrice