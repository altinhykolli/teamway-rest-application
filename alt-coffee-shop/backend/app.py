import os
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from collections import defaultdict
from bson import ObjectId

app = Flask('Alt Coffee Shop',)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/alt_coffee_shop'
mongo = PyMongo(app)

class Employee:
    def __init__(self, name, shift):
        self.name = name
        self.shift = shift

    def to_dict(self):
        return {'name': self.name, 'shift': self.shift}

def has_shift_on_day(employees, day):
    employee_shifts = defaultdict(list)
    for employee in employees:
        shift_day = employee['shift'].split()[0]
        employee_shifts[shift_day].append(employee['name'])
    return any(len(names) == 3 for names in employee_shifts.values())

def is_valid_shift(shift):
    start_hour = int(shift.split()[0].split(':')[0])
    return start_hour in [0, 8, 16]

def validate_shifts(employees):
    for employee in employees:
        if not is_valid_shift(employee['shift']):
            return False, f"Invalid shift timing for {employee['name']}: {employee['shift']}"
        if has_shift_on_day(employees, employee['shift'].split()[0]):
            return False, f"{employee['name']} already has a shift on {employee['shift'].split()[0]}"
    return True, "Shifts are valid"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/employees-page')
def employees_page():
    return render_template('employees.html')

@app.route('/crud')
def crud():
    return render_template('crud.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = mongo.db.employees.find().sort('shift', 1)
    employees_json = [{**employee, '_id': str(employee['_id'])} for employee in employees]
    return jsonify(employees_json)

@app.route('/employees/<string:id>', methods=['GET'])
def get_employee(id):
    employee = mongo.db.employees.find_one({'_id': ObjectId(id)})
    if employee:
        employee['_id'] = str(employee['_id'])
        return jsonify(employee), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(data['name'], data['shift'])

    existing_employee = mongo.db.employees.find_one({'name': new_employee.name})
    if existing_employee:
        return jsonify({'message': 'Employee already exists in the system'}), 400

    is_valid, message = validate_shifts([new_employee.to_dict()])
    if not is_valid:
        return jsonify({'message': message}), 400

    mongo.db.employees.insert_one(new_employee.to_dict())
    return jsonify({'message': 'Employee added successfully'}), 201

@app.route('/employees/<string:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    updated_employee = Employee(data.get('name'), data.get('shift'))

    is_valid, message = validate_shifts([updated_employee.to_dict()])
    if not is_valid:
        return jsonify({'message': message}), 400

    mongo.db.employees.update_one({'_id': ObjectId(id)}, {'$set': updated_employee.to_dict()})
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<string:id>', methods=['DELETE'])
def delete_employee(id):
    result = mongo.db.employees.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'message': 'Employee not found'}), 404
    else:
        return jsonify({'message': 'Employee deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)