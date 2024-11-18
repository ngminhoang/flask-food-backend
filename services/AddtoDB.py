import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5437/food-db'
db = SQLAlchemy(app)

# Ingredient model
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

def add_to_db(file_path):
    # Read CSV file into a pandas DataFrame (without headers)
    data = pd.read_csv(file_path, header=None)

    # Iterate over rows in the DataFrame
    for _, row in data.iterrows():
        try:
            # Split the single column (row[0]) by commas to extract fields
            field0 = row[0].split(',')
            field1 = row[1].split(',')
            field2 = row[2].split(',')
            field3 = row[3].split(',')
            field4 = row[4].split(',')
            field5 = row[5].split(',')
            field6 = row[6].split(',')
            field7 = row[7].split(',')
            field8 = row[8].split(',')
            field9 = row[9].split(',')
            # Map the fields to the database columns
            ingredient = Ingredient(
                name=field0[0],  # First field is 'Food'
                nu_grams=float(field2[0]),  # Third field is 'Grams'
                nu_calories=float(field3[0]),  # Fourth field is 'Calories'
                nu_proteins=float(field4[0]),  # Fifth field is 'Protein'
                nu_carbs=float(field8[0]),  # Ninth field is 'Carbs'
                nu_fibers=float(field7[0]),  # Eighth field is 'Fiber'
                nu_fats=float(field5[0]),  # Sixth field is 'Fat'
                nu_sat_fats=float(field6[0]),  # Seventh field is 'Sat.Fat'
                nu_price=0,  # Default price
                search_status=2  # Default status
            )

            # Debug print
            print(f"Adding {field0[0]} with grams: {field2[0]} and calories: {field3[0]}")

            # Uncomment to insert into the database
            db.session.add(ingredient)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error adding {row[0]}: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        add_to_db("../nutrients_csvfile.csv")
