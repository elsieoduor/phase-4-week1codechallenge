from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Define a route to list all restaurants
@app.route('/restaurants', methods=['GET'])
def list_restaurants():
    # Query all restaurants from the database
    restaurants = Restaurant.query.all()
    restaurant_info = []

    # Iterate through the restaurants and create a JSON response
    for restaurant in restaurants:
        restaurant_info.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        })

    # Create a JSON response 
    response = make_response(
        jsonify(restaurant_info),
        200
    )
    return response

# Define a route to list all pizzas
@app.route('/pizzas', methods=['GET'])
def list_pizzas():
    # Query all pizzas from the database
    pizzas = Pizza.query.all()
    pizza_info = []

    # Iterate through the pizzas and create a JSON response
    for pizza in pizzas:
        pizza_info.append({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        })

    # Create a JSON response 
    response = make_response(
        jsonify(pizza_info),
        200
    )
    return response

# Define a route to get a restaurant by its ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    # Query the restaurant by its ID
    restaurant = Restaurant.query.get(id)

    if restaurant:
        
        response = make_response(
            jsonify(restaurant.to_dict()),
            200
        )
        return response
    else:
        # Create a JSON response 
        response_dict = {
            "error": "Restaurant not found"
        }
        response = make_response(
            jsonify(response_dict),
            404
        )
        return response

# Define a route to delete a restaurant by its ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    # Query the restaurant by its ID
    restaurant = Restaurant.query.get(id)

    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()

        return '', 204
    else:
        # Create a JSON response 
        response_dict = {
            "error": "Restaurant not found"
        }
        response = make_response(
            jsonify(response_dict),
            404
        )
    return response

# Define a route to create a new restaurant-pizza record
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    new_record = request.json

    price = new_record['price']
    pizza_id = new_record['pizza_id']
    restaurant_id = new_record['restaurant_id']

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    if restaurant_pizza:
        # Create a JSON response 
        pizza_info = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }

        response = make_response(
            jsonify(pizza_info),
            201
        )
    else:
        response_dict = {
            "errors": ["Validation errors"]
        }
        response = make_response(
            jsonify(response_dict),
            400
        )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
