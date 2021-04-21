from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Food(Resource):
    def get(self):
        data = pd.read_csv('food.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('foodname', required=True)
        parser.add_argument('Carbs', required=True)
        parser.add_argument('proteins', required=True)
        parser.add_argument('fats', required=True)
        parser.add_argument('Calories', required=False)
        args = parser.parse_args()

        data = pd.read_csv('food.csv')

        new_data = pd.DataFrame({
            'foodname': [args['foodname']],
            'Carbs': [args['Carbs']],
            'proteins': [args['proteins']],
            'fats': [args['fats']],
            'Calories': [args['Calories']],


        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('food.csv', index=False)
        return {'data': new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('foodname', required=True)
        args = parser.parse_args()

        data = pd.read_csv('food.csv')

        data = data[data['foodname'] != args['foodname']]

        data.to_csv('food.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200



# Add URL endpoints
api.add_resource(Food, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
