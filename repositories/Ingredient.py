from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    nu_grams = db.Column(db.Float)
    nu_calories = db.Column(db.Float)
    nu_proteins = db.Column(db.Float)
    nu_carbs = db.Column(db.Float)
    nu_fibers = db.Column(db.Float)
    nu_fats = db.Column(db.Float)
    nu_sat_fats = db.Column(db.Float)
    nu_price = db.Column(db.Float)

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
            'nu_price': self.nu_price
        }
