import unittest
from app import app, mongo
from bson import ObjectId

class TestCoffeeShopApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.db = mongo.db

        self.db.employees.delete_many({})

    def tearDown(self):
        self.db.employees.delete_many({})

    def test_add_employee(self):
        employee_data = {'name': 'David', 'shift': '00:00 to 08:00'}

        response = self.app.post('/employees', json=employee_data)
        self.assertEqual(response.status_code, 201)

        employee = self.db.employees.find_one({'name': 'David'})
        self.assertIsNotNone(employee)

    def test_delete_employee(self):
        employee_id = str(self.db.employees.insert_one({'name': 'David', 'shift': '00:00 to 08:00'}).inserted_id)

        response = self.app.delete(f'/employees/{employee_id}')
        self.assertEqual(response.status_code, 200)

        employee = self.db.employees.find_one({'name': 'David'})
        self.assertIsNone(employee)

    def test_get_employees(self):
        self.db.employees.insert_many([
            {'name': 'Alice', 'shift': '00:00 to 08:00'},
            {'name': 'Sophia', 'shift': '08:00 to 16:00'},
            {'name': 'Michael', 'shift': '16:00 to 24:00'}
        ])

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)

        data = response.json
        for employee in data:
            employee['_id'] = str(employee['_id'])
        self.assertEqual(len(data), 3)

    def test_update_employee(self):
        employee_id = str(self.db.employees.insert_one({'name': 'David', 'shift': '00:00 to 08:00'}).inserted_id)

        response = self.app.put(f'/employees/{employee_id}', json={'name': 'David', 'shift': '00:00 to 08:00'})
        self.assertEqual(response.status_code, 200)

        employee = self.db.employees.find_one({'_id': ObjectId(employee_id)})
        self.assertIsNotNone(employee)
        self.assertEqual(employee['name'], 'David')

    def test_employee_has_shift(self):
        self.db.employees.insert_one({'name': 'David', 'shift': '00:00 to 08:00'})

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data), 1)

    def test_shift_duration(self):
        employee_data = {'name': 'David', 'shift': '00:00 to 08:00'}

        response = self.app.post('/employees', json=employee_data)
        self.assertEqual(response.status_code, 201)

        employee = self.db.employees.find_one({'name': 'David'})
        self.assertIsNotNone(employee)
        self.assertEqual(employee['shift'], '00:00 to 08:00')

    def test_no_duplicate_shifts_on_same_day(self):
        self.db.employees.insert_many([
            {'name': 'David', 'shift': '00:00 to 08:00'},
            {'name': 'Alice', 'shift': '08:00 to 16:00'}
        ])

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)

        data = response.json
        shifts_by_day = {}
        for employee in data:
            shift_day = employee['shift'].split()[0]
            if shift_day in shifts_by_day:
                self.fail(f"Employee {employee['name']} has two shifts on the same day: {shift_day}")
            else:
                shifts_by_day[shift_day] = True

    def test_timetable_covers_24_hours(self):
        self.db.employees.insert_many([
            {'name': 'Alice', 'shift': '00:00 to 08:00'},
            {'name': 'Sophia', 'shift': '08:00 to 16:00'},
            {'name': 'Michael', 'shift': '16:00 to 24:00'}
        ])

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)

        data = response.json

        shifts = set()
        for employee in data:
            shift_start = int(employee['shift'].split()[0].split(':')[0])
            shifts.add(shift_start)

        self.assertEqual(len(shifts), 3)
        self.assertTrue(0 in shifts and 8 in shifts and 16 in shifts, "Shifts don't cover the entire 24-hour period")

if __name__ == '__main__':
    unittest.main()