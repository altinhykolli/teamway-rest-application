from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/alt_coffee_shop'
mongo = PyMongo(app)

employee_names = ['John', 'Alice', 'Michael', 'Emma', 'William', 'Sophia', 'David', 'Olivia', 'Daniel']
shifts = ['00:00 to 08:00', '08:00 to 16:00', '16:00 to 24:00']
shift_index = 0

with app.app_context():
    for name in employee_names:
        existing_employee = mongo.db.employees.find_one({'name': name})
        if existing_employee:
            print(f"Employee '{name}' already exists in the database.")
        else:
            shift = shifts[shift_index]
            existing_employee = mongo.db.employees.find_one({'name': name, 'shift': shift})
            if not existing_employee:
                mongo.db.employees.insert_one({'name': name, 'shift': shift})
                print(f"Employee '{name}' assigned to shift '{shift}'")
                shift_index = (shift_index + 1) % len(shifts)
            else:
                print(f"Employee '{name}' already assigned to a shift.")