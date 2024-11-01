from typing import List
from __future__ import annotations  # Enables forward references

class FoodAnalysisResponse:
    def __init__(self, analysis_id, items):
        self.analysis_id = analysis_id
        self.items = items

    def to_dict(self):
        return {
            "analysis_id": self.analysis_id,
            "items": [item.to_dict() for item in self.items]
        }

class AnalysisItem:
    def __init__(self, food):
        self.food = food

    def to_dict(self):
        return {
            "food": [f.to_dict() for f in self.food]
        }

class FoodItem:
    def __init__(self, confidence, food_info, ingredients):
        self.confidence = confidence
        self.food_info = food_info
        self.ingredients = ingredients

    def to_dict(self):
        return {
            "confidence": self.confidence,
            "food_info": self.food_info.to_dict() if self.food_info else None,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients]
        }

class FoodInfo:
    def __init__(self, display_name, food_id, fv_grade, g_per_serving, nutrition):
        self.display_name = display_name
        self.food_id = food_id
        self.fv_grade = fv_grade
        self.g_per_serving = g_per_serving
        self.nutrition = nutrition

    def to_dict(self):
        return {
            "display_name": self.display_name,
            "food_id": self.food_id,
            "fv_grade": self.fv_grade,
            "g_per_serving": self.g_per_serving,
            "nutrition": self.nutrition.to_dict() if self.nutrition else None
        }

class Nutrition:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__

class Ingredient:
    def __init__(
            self,
            confidence: float,
            food_info: FoodInfo,
            ingredients: List[Ingredient],
            quantity: float
    ):
        self.confidence = confidence
        self.food_info = food_info
        self.ingredients = ingredients
        self.quantity = quantity

    def to_dict(self):
        return {
            "confidence": self.confidence,
            "food_info": self.food_info.to_dict() if self.food_info else None,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "quantity": self.quantity
        }
