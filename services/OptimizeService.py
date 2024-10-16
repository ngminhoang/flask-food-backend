from flask import Flask
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from pyomo.common.tests.deps import pyo
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5437/food-db'
db = SQLAlchemy(app)

# Ensure Ingredient model has a to_dict() method
class Ingredient(db.Model):
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
    # Add relevant fields here

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

def scale(calo, pro, fat, satfat, fiber, carb):
    with app.app_context():
        ingredients = Ingredient.query.all()

        # Convert ingredient objects into a list of dictionaries
        ingredient_data = [ingredient.to_dict() for ingredient in ingredients]

        # Debug print to see the queried ingredients
        # print("Queried Ingredients:", ingredient_data)




        # raw_data = [

        #     ["Cows' milk", "1 qt.", 976, 660, 32, 40, 36, 0, 48, 1, 250, 1500, 5, "Yes"],
        #     ["Milk skim", "1 qt.", 984, 360, 36, 0, 0, 0, 52, 1, 250, 1500, 5, "Yes"],
        #     ["Buttermilk", "1 cup", 246, 127, 9, 5, 4, 0, 13, 1, 100, 500, 2, "Yes"],
        #     ["Evaporated, undiluted", "1 cup", 252, 345, 16, 20, 18, 0, 24, 1, 100, 500, 3, "Yes"],
        #     ["Fortified milk", "6 cups", 414, 373, 89, 42, 23, 1.4, 119, 10, 250, 1000, 4, "Yes"],
        #     ["Powdered milk", "1 cup", 103, 515, 27, 28, 24, 0, 39, 1, 100, 500, 2, "No"],
        #     ["skim, instant", "1 1/3 cups", 85, 290, 30, 0, 0, 0, 42, 1, 100, 400, 2, "Yes"],
        #     ["skim, non-instant", "2/3 cup", 85, 290, 30, 0, 0, 1, 42, 1, 100, 400, 2, "Yes"],
        #     ["Goats' milk", "1 cup", 244, 165, 8, 10, 8, 0, 11, 1, 100, 500, 3, "Yes"],
        #     ["Ice cream (1/2 cup)", "2 cups", 540, 690, 24, 24, 22, 0, 70, 1, 200, 1000, 5, "Yes"],
        #     ["Cocoa", "1 cup", 252, 235, 8, 11, 10, 0, 26, 1, 100, 500, 2, "Yes"],
        #     ["skim. milk", "1 cup", 250, 128, 18, 4, 3, 1, 13, 1, 100, 500, 2, "Yes"],
        #     ["cornstarch", "1 cup", 248, 275, 9, 10, 9, 0, 40, 1, 100, 500, 2, "Yes"],
        #     ["Custard", "1 cup", 248, 285, 13, 14, 11, 0, 28, 1, 100, 500, 3, "Yes"],
        #     ["Ice cream", "1 cup", 188, 300, 6, 18, 16, 0, 29, 1, 100, 500, 3, "Yes"],
        #     ["Ice milk", "1 cup", 190, 275, 9, 10, 9, 0, 32, 1, 100, 500, 2, "Yes"],
        #     ["Cream or half-and-half", "1/2 cup", 120, 170, 4, 15, 13, 0, 5, 1, 100, 500, 2, "Yes"],
        #     ["whipping", "1/2 cup", 119, 430, 2, 44, 27, 1, 3, 1, 100, 500, 3, "Yes"],
        #     ["Cheese", "1 cup", 225, 240, 30, 11, 10, 0, 6, 1, 100, 500, 3, "Yes"],
        #     ["uncreamed", "1 cup", 225, 195, 38, 0, 0, 0, 6, 1, 100, 500, 2, "Yes"],
        #     ["Cheddar", "1-in. cube", 17, 70, 4, 6, 5, 0, 0, 1, 10, 100, 0.5, "Yes"],
        #     ["Cheddar, grated cup", "1/2 cup", 56, 226, 14, 19, 17, 0, 1, 1, 30, 150, 1, "Yes"],
        #     ["Cream cheese", "1 oz.", 28, 105, 2, 11, 10, 0, 1, 1, 10, 100, 1, "Yes"],
        #     ["Processed cheese", "1 oz.", 28, 105, 7, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
        #     ["Roquefort type", "1 oz.", 28, 105, 6, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
        #     ["Swiss", "1 oz.", 28, 105, 7, 8, 7, 0, 0, 1, 10, 100, 1, "Yes"],
        #     ["Eggs raw", "2", 100, 150, 12, 12, 10, 0, 0, 1, 50, 200, 2, "Yes"],
        #     ["Eggs Scrambled or fried", "2", 128, 220, 13, 16, 14, 0, 1, 1, 50, 200, 2, "Yes"],
        #     ["Yolks", "2", 34, 120, 6, 10, 8, 0, 0, 1, 20, 100, 1, "Yes"],
        #     ["Butter", "1 T.", 14, 100, 0, 11, 10, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Butter", "1/2 cup", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
        #     ["Butter", "1/4 lb.", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
        #     ["Hydrogenated cooking fat", "1/2 cup", 100, 665, 0, 100, 88, 0, 0, 1, 50, 200, 5, "Yes"],
        #     ["Lard", "1/2 cup", 110, 992, 0, 110, 92, 0, 0, 1, 50, 200, 5, "Yes"],
        #     ["Margarine", "1/2 cup", 112, 806, 0, 91, 76, 0, 0, 1, 50, 200, 5, "Yes"],
        #     ["Margarine", "2 pat or 1 T.", 14, 100, 0, 11, 9, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Mayonnaise", "1 T.", 15, 110, 0, 12, 5, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Corn oil", "1 T.", 14, 125, 0, 14, 5, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Olive oil", "1 T.", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Safflower seed oil", "1 T.", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["French dressing", "1 T.", 15, 60, 0, 6, 2, 0, 2, 1, 10, 50, 1, "Yes"],
        #     ["Thousand Island sauce", "1 T.", 15, 75, 0, 8, 3, 0, 1, 1, 10, 50, 1, "Yes"],
        #     ["Salt pork", "2 oz.", 60, 470, 3, 55, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Bacon", "2 slices", 16, 95, 4, 8, 7, 0, 1, 1, 10, 50, 2, "Yes"],
        #     ["Beef", "3 oz.", 85, 245, 23, 16, 15, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Hamburger", "3 oz.", 85, 245, 21, 17, 15, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Ground lean", "3 oz.", 85, 185, 24, 10, 9, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Roast beef", "3 oz.", 85, 390, 16, 36, 35, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Steak", "3 oz.", 85, 330, 20, 27, 25, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Steak, lean, as round", "3 oz.", 85, 220, 24, 12, 11, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Corned beef", "3 oz.", 85, 185, 22, 10, 9, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Corned beef hash canned", "3 oz.", 85, 120, 12, 8, 7, 0, 6, 1, 20, 100, 3, "Yes"],
        #     ["Corned beef hash dried", "2 oz.", 56, 115, 19, 4, 4, 0, 0, 1, 10, 50, 1, "Yes"],
        #     ["Pot-pie", "1 pie", 227, 480, 18, 28, 25, 0, 32, 1, 200, 1000, 5, "Yes"],
        #     ["Corned beef hash stew", "1 cup", 235, 185, 15, 10, 9, 0, 15, 1, 100, 500, 3, "Yes"],
        #     ["Chicken", "3 oz.", 85, 185, 23, 9, 7, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Fried, breast or leg and thigh chicken", "3 oz.", 85, 245, 25, 15, 11, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Roasted chicken", "3 oz.", 85, 190, 28, 7, 5, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Duck, meat only", "3 oz.", 85, 200, 22, 12, 11, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Turkey, meat only", "3 oz.", 85, 180, 25, 6, 2, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Lamb, meat only", "3 oz.", 85, 270, 25, 20, 15, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Pork, lean", "3 oz.", 85, 260, 30, 15, 14, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Pork sausage", "3 oz.", 85, 190, 14, 15, 10, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Veal", "3 oz.", 85, 250, 30, 14, 12, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Fish", "3 oz.", 85, 140, 20, 5, 2, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Catfish", "3 oz.", 85, 205, 23, 10, 3, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Haddock", "3 oz.", 85, 150, 24, 3, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Salmon", "3 oz.", 85, 186, 25, 9, 2, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Sardines", "3 oz.", 85, 220, 24, 12, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Shrimp", "3 oz.", 85, 84, 18, 1, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Tuna", "3 oz.", 85, 119, 26, 1, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Trout", "3 1/2 oz.", 100, 171, 29, 6, 0, 0, 0, 1, 20, 100, 3, "Yes"],
        #     ["Cabbage", "1 cup", 70, 22, 1, 0, 0, 3, 5, 1, 50, 200, 1, "Yes"],
        #     ["Carrots", "1 cup", 128, 55, 1, 0, 0, 3, 13, 1, 50, 200, 1, "Yes"],
        #     ["Corn", "1 cup", 154, 132, 5, 2, 0, 4, 29, 1, 50, 200, 1, "Yes"],
        #     ["Green beans", "1 cup", 125, 44, 2, 0, 0, 4, 10, 1, 50, 200, 1, "Yes"],
        #     ["Lettuce", "1 cup", 36, 5, 0, 0, 0, 1, 1, 1, 50, 200, 1, "Yes"],
        #     ["Peas", "1 cup", 160, 60, 5, 0, 0, 5, 12, 1, 50, 200, 1, "Yes"],
        #     ["Potatoes", "1 cup", 146, 121, 3, 0, 0, 2, 28, 1, 50, 200, 1, "Yes"],
        #     ["Tomatoes", "1 cup", 240, 50, 3, 0, 0, 1, 12, 1, 50, 200, 1, "Yes"],
        #     ["Turnips", "1 cup", 140, 49, 1, 0, 0, 3, 11, 1, 50, 200, 1, "Yes"],
        #     ["Onions", "1 cup", 146, 64, 1, 0, 0, 3, 15, 1, 50, 200, 1, "Yes"],
        #     ["Sweet potatoes", "1 cup", 200, 180, 4, 0, 0, 7, 41, 1, 50, 200, 1, "Yes"],
        #     ["Squash", "1 cup", 120, 50, 1, 0, 0, 3, 12, 1, 50, 200, 1, "Yes"],
        #     ["Spinach", "1 cup", 180, 41, 5, 0, 0, 5, 7, 1, 50, 200, 1, "Yes"],
        #     ["Broccoli", "1 cup", 150, 50, 4, 0, 0, 5, 10, 1, 50, 200, 1, "Yes"],
        #     ["Asparagus", "1 cup", 120, 20, 2, 0, 0, 2, 4, 1, 50, 200, 1, "Yes"],
        #     ["Artichokes", "1 cup", 120, 60, 4, 0, 0, 7, 13, 1, 50, 200, 1, "Yes"],
        #     ["Brussels sprouts", "1 cup", 120, 36, 3, 0, 0, 4, 8, 1, 50, 200, 1, "Yes"],
        #     ["Cauliflower", "1 cup", 120, 25, 2, 0, 0, 3, 5, 1, 50, 200, 1, "Yes"],
        #     ["Eggplant", "1 cup", 90, 35, 1, 0, 0, 3, 8, 1, 50, 200, 1, "Yes"],
        #     ["Mushrooms", "1 cup", 150, 44, 5, 0, 0, 2, 8, 1, 50, 200, 1, "Yes"],
        #     ["Green pepper", "1 cup", 120, 23, 1, 0, 0, 2, 5, 1, 50, 200, 1, "Yes"],
        #     ["Bell pepper", "1 cup", 120, 20, 1, 0, 0, 2, 5, 1, 50, 200, 1, "Yes"],
        #     ["Rhubarb", "1 cup", 120, 26, 1, 0, 0, 2, 7, 1, 50, 200, 1, "Yes"],
        #     ["Cucumber", "1 cup", 120, 16, 1, 0, 0, 1, 4, 1, 50, 200, 1, "Yes"],
        #     ["Spinach", "1 cup", 120, 30, 3, 0, 0, 5, 4, 1, 50, 200, 1, "Yes"],
        #     ["Lettuce", "1 cup", 36, 5, 0, 0, 0, 1, 1, 1, 50, 200, 1, "Yes"],
        #     ["Radishes", "1 cup", 116, 19, 1, 0, 0, 1, 4, 1, 50, 200, 1, "Yes"],
        # ]

        # index =1

        # for item in raw_data:
            
        #     del item[13]
        #     del item[12]
        #     del item[11]
        #     item[10] = index
        #     index += 1 
        #     del item[1]



        # food_objects = [
        #     {
        #         "name": item[0],
        #         "nuGrams": item[1],
        #         "nuCalories": item[2],
        #         "nuProteins": item[3],
        #         "nuCarbs": item[4],
        #         "nuFibers": item[5],
        #         "nuFats": item[6],
        #         "nuSatFats": item[7],
        #         "nuPrice": item[8]
        #     }
        #     for item in raw_data
        # ]

        # # Print the result
        # print(food_objects)


        raw_data = [
            [item['name'], item['nu_grams'], item['nu_calories'], item['nu_proteins'], item['nu_fats'], item['nu_sat_fats'], item['nu_fibers'], item['nu_carbs'], item['nu_price'],item['id']]
            for item in ingredient_data
        ]

        # Output the transformed data
        # for row in raw_data:
        #     print(row)

        data = pd.DataFrame(raw_data, columns=["Food", "Grams", "Calories", "Protein", "Fat", "Sat.Fat", "Fiber", "Carbs", "Cost","id"])

        # Tách label và các thông số
        data0 = data.iloc[:, 2:8].values  # Dinh dưỡng từ Calories đến Carbs
        data1 = data.iloc[:, 9].values     # Tên thực phẩm
        data2 = data.iloc[:, 1].values     # Trọng lượng thực phẩm
        prices = data.iloc[:, 8].values     # Cột giá
        number = len(data0)  # Số lượng thực phẩm

        # Chuyển đổi dữ liệu sang dạng dictionary
        b = {}
        for i in range(number):
            for j in range(6):
                b[i + 1, j + 1] = float(data0[i][j])

        # Tạo model
        model = pyo.ConcreteModel()
        model.i = pyo.RangeSet(1, number)  # Tạo range set từ 1 đến số thực phẩm
        model.j = pyo.RangeSet(1, 6)  # Tạo range set cho 6 loại dinh dưỡng
        model.p = pyo.Param(model.i, model.j, initialize=b)  # Áp dụng tham số dinh dưỡng
        model.price = pyo.Param(model.i, initialize=lambda model, i: prices[i - 1])  # Cột giá

        model.x = pyo.Var(model.i, within=pyo.NonNegativeReals)  # Biến quyết định

        # Hàm mục tiêu
        model.Obj = pyo.Objective(rule=lambda model: sum(model.price[i] * model.x[i] for i in model.i), sense=pyo.minimize)

        # Ràng buộc dinh dưỡng
        model.Const2 = pyo.Constraint(rule=lambda model: sum(model.p[i, 1] * model.x[i] for i in model.i) >= calo - 70)
        model.Const3 = pyo.Constraint(rule=lambda model: sum(model.p[i, 2] * model.x[i] for i in model.i) >= pro - 20)
        model.Const4 = pyo.Constraint(rule=lambda model: sum(model.p[i, 3] * model.x[i] for i in model.i) >= fat - 20)
        model.Const5 = pyo.Constraint(rule=lambda model: sum(model.p[i, 4] * model.x[i] for i in model.i) >= satfat - 20)
        model.Const6 = pyo.Constraint(rule=lambda model: sum(model.p[i, 5] * model.x[i] for i in model.i) >= fiber - 20)
        model.Const7 = pyo.Constraint(rule=lambda model: sum(model.p[i, 6] * model.x[i] for i in model.i) >= carb - 20)

        # Ràng buộc tối đa
        model.Const8 = pyo.Constraint(rule=lambda model: sum(model.p[i, 1] * model.x[i] for i in model.i) <= calo + 70)
        model.Const9 = pyo.Constraint(rule=lambda model: sum(model.p[i, 2] * model.x[i] for i in model.i) <= pro + 20)
        model.Const10 = pyo.Constraint(rule=lambda model: sum(model.p[i, 3] * model.x[i] for i in model.i) <= fat + 20)
        model.Const11 = pyo.Constraint(rule=lambda model: sum(model.p[i, 4] * model.x[i] for i in model.i) <= satfat + 20)
        model.Const12 = pyo.Constraint(rule=lambda model: sum(model.p[i, 5] * model.x[i] for i in model.i) <= fiber + 20)
        model.Const13 = pyo.Constraint(rule=lambda model: sum(model.p[i, 6] * model.x[i] for i in model.i) <= carb + 20)



        # Giải bài toán
        optm = SolverFactory('glpk')
        results = optm.solve(model)

        # Kiểm tra kết quả tối ưu
        food_results = []
        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            # Lưu trữ giải pháp
            solution = []
            for i in range(number):
                percent = pyo.value(model.x[i + 1])
                if percent > 0.0:
                    solution.append((data1[i], percent))

            food_results.append(solution)



        # Giả lập nhiều lần chạy để thu thập nhiều giải pháp (nên chạy với các tham số khác nhau)
        # for _ in range(0):  # Thí dụ: lặp lại 10 lần
        #     results = optm.solve(model)

        #     if results.solver.termination_condition == pyo.TerminationCondition.optimal:
        #         total_cost = pyo.value(model.Obj)
        #         solution = []
        #         for i in range(number):
        #             food_weight = pyo.value(model.x[i + 1]) * float(data2[i])
        #             if food_weight > 0.0:
        #                 solution.append((data1[i], food_weight, pyo.value(model.price[i + 1]) * food_weight / 100))

        #         food_results.append((total_cost, solution))

        # Sắp xếp danh sách theo tổng chi phí
        food_results.sort(key=lambda x: x[0])  # Sắp xếp theo giá thành

        # In ra 10 giải pháp có giá thành thấp nhất
        
        # Convert nested structure to the desired model format
        model_results = [{"id": int(subitem[0]), "percent": subitem[1]} for item in food_results[:10] for subitem in item]

        # Print the result  
        return model_results        

print(scale(660,32,40,36,0,48))


#
# raw_data = [
#
#     ["Cows' milk", "1 qt.", 976, 660, 32, 40, 36, 0, 48, 1, 250, 1500, 5, "Yes"],
#     ["Milk skim", "1 qt.", 984, 360, 36, 0, 0, 0, 52, 1, 250, 1500, 5, "Yes"],
#     ["Buttermilk", "1 cup", 246, 127, 9, 5, 4, 0, 13, 1, 100, 500, 2, "Yes"],
#     ["Evaporated, undiluted", "1 cup", 252, 345, 16, 20, 18, 0, 24, 1, 100, 500, 3, "Yes"],
#     ["Fortified milk", "6 cups", 414, 373, 89, 42, 23, 1.4, 119, 10, 250, 1000, 4, "Yes"],
#     ["Powdered milk", "1 cup", 103, 515, 27, 28, 24, 0, 39, 1, 100, 500, 2, "No"],
#     ["skim, instant", "1 1/3 cups", 85, 290, 30, 0, 0, 0, 42, 1, 100, 400, 2, "Yes"],
#     ["skim, non-instant", "2/3 cup", 85, 290, 30, 0, 0, 1, 42, 1, 100, 400, 2, "Yes"],
#     ["Goats' milk", "1 cup", 244, 165, 8, 10, 8, 0, 11, 1, 100, 500, 3, "Yes"],
#     ["Ice cream (1/2 cup)", "2 cups", 540, 690, 24, 24, 22, 0, 70, 1, 200, 1000, 5, "Yes"],
#     ["Cocoa", "1 cup", 252, 235, 8, 11, 10, 0, 26, 1, 100, 500, 2, "Yes"],
#     ["skim. milk", "1 cup", 250, 128, 18, 4, 3, 1, 13, 1, 100, 500, 2, "Yes"],
#     ["cornstarch", "1 cup", 248, 275, 9, 10, 9, 0, 40, 1, 100, 500, 2, "Yes"],
#     ["Custard", "1 cup", 248, 285, 13, 14, 11, 0, 28, 1, 100, 500, 3, "Yes"],
#     ["Ice cream", "1 cup", 188, 300, 6, 18, 16, 0, 29, 1, 100, 500, 3, "Yes"],
#     ["Ice milk", "1 cup", 190, 275, 9, 10, 9, 0, 32, 1, 100, 500, 2, "Yes"],
#     ["Cream or half-and-half", "1/2 cup", 120, 170, 4, 15, 13, 0, 5, 1, 100, 500, 2, "Yes"],
#     ["whipping", "1/2 cup", 119, 430, 2, 44, 27, 1, 3, 1, 100, 500, 3, "Yes"],
#     ["Cheese", "1 cup", 225, 240, 30, 11, 10, 0, 6, 1, 100, 500, 3, "Yes"],
#     ["uncreamed", "1 cup", 225, 195, 38, 0, 0, 0, 6, 1, 100, 500, 2, "Yes"],
#     ["Cheddar", "1-in. cube", 17, 70, 4, 6, 5, 0, 0, 1, 10, 100, 0.5, "Yes"],
#     ["Cheddar, grated cup", "1/2 cup", 56, 226, 14, 19, 17, 0, 1, 1, 30, 150, 1, "Yes"],
#     ["Cream cheese", "1 oz.", 28, 105, 2, 11, 10, 0, 1, 1, 10, 100, 1, "Yes"],
#     ["Processed cheese", "1 oz.", 28, 105, 7, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Roquefort type", "1 oz.", 28, 105, 6, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Swiss", "1 oz.", 28, 105, 7, 8, 7, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Eggs raw", "2", 100, 150, 12, 12, 10, 0, 0, 1, 50, 200, 2, "Yes"],
#     ["Eggs Scrambled or fried", "2", 128, 220, 13, 16, 14, 0, 1, 1, 50, 200, 2, "Yes"],
#     ["Yolks", "2", 34, 120, 6, 10, 8, 0, 0, 1, 20, 100, 1, "Yes"],
#     ["Butter", "1 T.", 14, 100, 0, 11, 10, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Butter", "1/2 cup", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
#     ["Butter", "1/4 lb.", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
#     ["Hydrogenated cooking fat", "1/2 cup", 100, 665, 0, 100, 88, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Lard", "1/2 cup", 110, 992, 0, 110, 92, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Margarine", "1/2 cup", 112, 806, 0, 91, 76, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Margarine", "2 pat or 1 T.", 14, 100, 0, 11, 9, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Mayonnaise", "1 T.", 15, 110, 0, 12, 5, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Corn oil", "1 T.", 14, 125, 0, 14, 5, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Olive oil", "1 T.", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Safflower seed oil", "1 T.", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["French dressing", "1 T.", 15, 60, 0, 6, 2, 0, 2, 1, 10, 50, 1, "Yes"],
#     ["Thousand Island sauce", "1 T.", 15, 75, 0, 8, 3, 0, 1, 1, 10, 50, 1, "Yes"],
#     ["Salt pork", "2 oz.", 60, 470, 3, 55, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Bacon", "2 slices", 16, 95, 4, 8, 7, 0, 1, 1, 10, 50, 2, "Yes"],
#     ["Beef", "3 oz.", 85, 245, 23, 16, 15, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Hamburger", "3 oz.", 85, 245, 21, 17, 15, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Ground lean", "3 oz.", 85, 185, 24, 10, 9, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Roast beef", "3 oz.", 85, 390, 16, 36, 35, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Steak", "3 oz.", 85, 330, 20, 27, 25, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Steak, lean, as round", "3 oz.", 85, 220, 24, 12, 11, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Corned beef", "3 oz.", 85, 185, 22, 10, 9, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Corned beef hash canned", "3 oz.", 85, 120, 12, 8, 7, 0, 6, 1, 20, 100, 3, "Yes"],
#     ["Corned beef hash dried", "2 oz.", 56, 115, 19, 4, 4, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Pot-pie", "1 pie", 227, 480, 18, 28, 25, 0, 32, 1, 200, 1000, 5, "Yes"],
#     ["Corned beef hash stew", "1 cup", 235, 185, 15, 10, 9, 0, 15, 1, 100, 500, 3, "Yes"],
#     ["Chicken", "3 oz.", 85, 185, 23, 9, 7, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Fried, breast or leg and thigh chicken", "3 oz.", 85, 245, 25, 15, 11, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Roasted chicken", "3 oz.", 85, 190, 28, 7, 5, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Duck, meat only", "3 oz.", 85, 200, 22, 12, 11, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Turkey, meat only", "3 oz.", 85, 180, 25, 6, 2, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Lamb, meat only", "3 oz.", 85, 270, 25, 20, 15, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Pork, lean", "3 oz.", 85, 260, 30, 15, 14, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Pork sausage", "3 oz.", 85, 190, 14, 15, 10, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Veal", "3 oz.", 85, 250, 30, 14, 12, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Fish", "3 oz.", 85, 140, 20, 5, 2, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Catfish", "3 oz.", 85, 205, 23, 10, 3, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Haddock", "3 oz.", 85, 150, 24, 3, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Salmon", "3 oz.", 85, 186, 25, 9, 2, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Sardines", "3 oz.", 85, 220, 24, 12, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Shrimp", "3 oz.", 85, 84, 18, 1, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Tuna", "3 oz.", 85, 119, 26, 1, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Trout", "3 1/2 oz.", 100, 171, 29, 6, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Cabbage", "1 cup", 70, 22, 1, 0, 0, 3, 5, 1, 50, 200, 1, "Yes"],
#     ["Carrots", "1 cup", 128, 55, 1, 0, 0, 3, 13, 1, 50, 200, 1, "Yes"],
#     ["Corn", "1 cup", 154, 132, 5, 2, 0, 4, 29, 1, 50, 200, 1, "Yes"],
#     ["Green beans", "1 cup", 125, 44, 2, 0, 0, 4, 10, 1, 50, 200, 1, "Yes"],
#     ["Lettuce", "1 cup", 36, 5, 0, 0, 0, 1, 1, 1, 50, 200, 1, "Yes"],
#     ["Peas", "1 cup", 160, 60, 5, 0, 0, 5, 12, 1, 50, 200, 1, "Yes"],
#     ["Potatoes", "1 cup", 146, 121, 3, 0, 0, 2, 28, 1, 50, 200, 1, "Yes"],
#     ["Tomatoes", "1 cup", 240, 50, 3, 0, 0, 1, 12, 1, 50, 200, 1, "Yes"],
#     ["Turnips", "1 cup", 140, 49, 1, 0, 0, 3, 11, 1, 50, 200, 1, "Yes"],
#     ["Onions", "1 cup", 146, 64, 1, 0, 0, 3, 15, 1, 50, 200, 1, "Yes"],
#     ["Sweet potatoes", "1 cup", 200, 180, 4, 0, 0, 7, 41, 1, 50, 200, 1, "Yes"],
#     ["Squash", "1 cup", 120, 50, 1, 0, 0, 3, 12, 1, 50, 200, 1, "Yes"],
#     ["Spinach", "1 cup", 180, 41, 5, 0, 0, 5, 7, 1, 50, 200, 1, "Yes"],
#     ["Broccoli", "1 cup", 150, 50, 4, 0, 0, 5, 10, 1, 50, 200, 1, "Yes"],
#     ["Asparagus", "1 cup", 120, 20, 2, 0, 0, 2, 4, 1, 50, 200, 1, "Yes"],
#     ["Artichokes", "1 cup", 120, 60, 4, 0, 0, 7, 13, 1, 50, 200, 1, "Yes"],
#     ["Brussels sprouts", "1 cup", 120, 36, 3, 0, 0, 4, 8, 1, 50, 200, 1, "Yes"],
#     ["Cauliflower", "1 cup", 120, 25, 2, 0, 0, 3, 5, 1, 50, 200, 1, "Yes"],
#     ["Eggplant", "1 cup", 90, 35, 1, 0, 0, 3, 8, 1, 50, 200, 1, "Yes"],
#     ["Mushrooms", "1 cup", 150, 44, 5, 0, 0, 2, 8, 1, 50, 200, 1, "Yes"],
#     ["Green pepper", "1 cup", 120, 23, 1, 0, 0, 2, 5, 1, 50, 200, 1, "Yes"],
#     ["Bell pepper", "1 cup", 120, 20, 1, 0, 0, 2, 5, 1, 50, 200, 1, "Yes"],
#     ["Rhubarb", "1 cup", 120, 26, 1, 0, 0, 2, 7, 1, 50, 200, 1, "Yes"],
#     ["Cucumber", "1 cup", 120, 16, 1, 0, 0, 1, 4, 1, 50, 200, 1, "Yes"],
#     ["Spinach", "1 cup", 120, 30, 3, 0, 0, 5, 4, 1, 50, 200, 1, "Yes"],
#     ["Lettuce", "1 cup", 36, 5, 0, 0, 0, 1, 1, 1, 50, 200, 1, "Yes"],
#     ["Radishes", "1 cup", 116, 19, 1, 0, 0, 1, 4, 1, 50, 200, 1, "Yes"],
# ]



# raw_data = [
#     ["Cows' milk", 976, 660, 32, 40, 36, 0, 48, 1, 250, 1500, 5, "Yes"],
#     ["Milk skim", 984, 360, 36, 0, 0, 0, 52, 1, 250, 1500, 5, "Yes"],
#     ["Buttermilk", 246, 127, 9, 5, 4, 0, 13, 1, 100, 500, 2, "Yes"],
#     ["Evaporated, undiluted", 252, 345, 16, 20, 18, 0, 24, 1, 100, 500, 3, "Yes"],
#     ["Fortified milk", 414, 373, 89, 42, 23, 1.4, 119, 10, 250, 1000, 4, "Yes"],
#     ["Powdered milk", 103, 515, 27, 28, 24, 0, 39, 1, 100, 500, 2, "No"],
#     ["skim, instant", 85, 290, 30, 0, 0, 0, 42, 1, 100, 400, 2, "Yes"],
#     ["skim, non-instant", 85, 290, 30, 0, 0, 1, 42, 1, 100, 400, 2, "Yes"],
#     ["Goats' milk", 244, 165, 8, 10, 8, 0, 11, 1, 100, 500, 3, "Yes"],
#     ["Ice cream (1/2 cup)", 540, 690, 24, 24, 22, 0, 70, 1, 200, 1000, 5, "Yes"],
#     ["Cocoa", 252, 235, 8, 11, 10, 0, 26, 1, 100, 500, 2, "Yes"],
#     ["skim. milk", 250, 128, 18, 4, 3, 1, 13, 1, 100, 500, 2, "Yes"],
#     ["cornstarch", 248, 275, 9, 10, 9, 0, 40, 1, 100, 500, 2, "Yes"],
#     ["Custard", 248, 285, 13, 14, 11, 0, 28, 1, 100, 500, 3, "Yes"],
#     ["Ice cream", 188, 300, 6, 18, 16, 0, 29, 1, 100, 500, 3, "Yes"],
#     ["Ice milk", 190, 275, 9, 10, 9, 0, 32, 1, 100, 500, 2, "Yes"],
#     ["Cream or half-and-half", 120, 170, 4, 15, 13, 0, 5, 1, 100, 500, 2, "Yes"],
#     ["whipping", 119, 430, 2, 44, 27, 1, 3, 1, 100, 500, 3, "Yes"],
#     ["Cheese", 225, 240, 30, 11, 10, 0, 6, 1, 100, 500, 3, "Yes"],
#     ["uncreamed", 225, 195, 38, 0, 0, 0, 6, 1, 100, 500, 2, "Yes"],
#     ["Cheddar", 17, 70, 4, 6, 5, 0, 0, 1, 10, 100, 0.5, "Yes"],
#     ["Cheddar, grated cup", 56, 226, 14, 19, 17, 0, 1, 1, 30, 150, 1, "Yes"],
#     ["Cream cheese", 28, 105, 2, 11, 10, 0, 1, 1, 10, 100, 1, "Yes"],
#     ["Processed cheese", 28, 105, 7, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Roquefort type", 28, 105, 6, 9, 8, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Swiss", 28, 105, 7, 8, 7, 0, 0, 1, 10, 100, 1, "Yes"],
#     ["Eggs raw", 100, 150, 12, 12, 10, 0, 0, 1, 50, 200, 2, "Yes"],
#     ["Eggs Scrambled or fried", 128, 220, 13, 16, 14, 0, 1, 1, 50, 200, 2, "Yes"],
#     ["Yolks", 34, 120, 6, 10, 8, 0, 0, 1, 20, 100, 1, "Yes"],
#     ["Butter", 14, 100, 0, 11, 10, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Butter", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
#     ["Butter", 112, 113, 114, 115, 116, 117, 118, 1, 50, 200, 2, "Yes"],
#     ["Hydrogenated cooking fat", 100, 665, 0, 100, 88, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Lard", 110, 992, 0, 110, 92, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Margarine", 112, 806, 0, 91, 76, 0, 0, 1, 50, 200, 5, "Yes"],
#     ["Margarine", 14, 100, 0, 11, 9, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Mayonnaise", 15, 110, 0, 12, 5, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Corn oil", 14, 125, 0, 14, 5, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Olive oil", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["Safflower seed oil", 14, 125, 0, 14, 3, 0, 0, 1, 10, 50, 1, "Yes"],
#     ["French dressing", 15, 60, 0, 6, 2, 0, 2, 1, 10, 50, 1, "Yes"],
#     ["Thousand Island sauce", 15, 75, 0, 8, 3, 0, 1, 1, 10, 50, 1, "Yes"],
#     ["Salt pork", 60, 470, 3, 55, 0, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Bacon", 16, 95, 4, 8, 7, 0, 1, 1, 10, 50, 2, "Yes"],
#     ["Beef", 85, 245, 23, 16, 15, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Hamburger", 85, 245, 21, 17, 15, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Ground lean", 85, 185, 24, 10, 9, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Roast beef", 85, 390, 16, 36, 35, 0, 0, 1, 20, 100, 3, "Yes"],
#     ["Steak", 85, 215, 25, 14, 13, 0, 0, 1, 20, 100, 3, "Yes"],
# ]