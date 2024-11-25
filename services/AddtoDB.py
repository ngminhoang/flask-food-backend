import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5437/food-db'
db = SQLAlchemy(app)

# Ingredient model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Ensure unique category names
    ingredients = db.relationship('Ingredient', back_populates='category', lazy=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    nu_grams = db.Column(db.Float)
    nu_calories = db.Column(db.Float)
    nu_proteins = db.Column(db.Float)
    nu_carbs = db.Column(db.Float)
    nu_fibers = db.Column(db.Float)
    nu_fats = db.Column(db.Float)
    nu_sat_fats = db.Column(db.Float)
    nu_price = db.Column(db.Float)
    search_status = db.Column(db.Integer)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='ingredients')


def add_to_db(file_path):
    # Read CSV file into a pandas DataFrame
    data = pd.read_csv(file_path, header=None)

    # Extract and process unique categories from field10
    categories = set(data[10].str.split(',').explode().str.strip().unique())

    # Add categories to the database
    category_map = {}
    for category_name in categories:
        if category_name:  # Avoid empty strings
            category = Category(name=category_name)
            db.session.add(category)
            category_map[category_name] = category
    db.session.commit()

    # Iterate over rows in the DataFrame to add ingredients
    for _, row in data.iterrows():
        try:
            # Extract fields from the row
            name = row[0].strip()
            nu_grams = float(row[2])
            nu_calories = float(row[3])
            nu_proteins = float(row[4])
            nu_fats = float(row[5])
            nu_sat_fats = float(row[6])
            nu_fibers = float(row[7])
            nu_carbs = float(row[8])
            nu_price = float(row[9])
            category_names = row[10].split(',')  # List of categories for the ingredient

            # Associate with the first category (assuming one category per ingredient)
            category = category_map.get(category_names[0].strip())

            # Create and add the ingredient
            ingredient = Ingredient(
                name=name,
                nu_grams=nu_grams,
                nu_calories=nu_calories,
                nu_proteins=nu_proteins,
                nu_fats=nu_fats,
                nu_sat_fats=nu_sat_fats,
                nu_fibers=nu_fibers,
                nu_carbs=nu_carbs,
                nu_price=nu_price,
                search_status=2,  # Default status
                category=category
            )
            db.session.add(ingredient)
            db.session.commit()
            print(f"Added ingredient: {name}")

        except Exception as e:
            db.session.rollback()
            print(f"Error adding {row[0]}: {e}")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        add_to_db("../nutrients_csvfile.csv")
