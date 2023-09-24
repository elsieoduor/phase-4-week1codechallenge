from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def list_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_info = []
    
    for restaurant in restaurants:
        restaurant_info.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        })
    
    response = make_response(
        jsonify(restaurant_info),
        200
    )
    return response

@app.route('/pizzas', methods=['GET'])
def list_pizzas():
    pizzas = Pizza.query.all()
    pizza_info = []
    
    for pizza in pizzas:
        pizza_info.append({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        })
    
    response = make_response(
        jsonify(pizza_info),
        200
    )
    return response

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if restaurant:
        pizza_info = []
        for pizza in restaurant.pizzas:
            pizza_info.append({
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            })
        
        restaurant_info = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizza_info
        }
        
        response = make_response(
            jsonify(restaurant_info),
            200
        )
    else:
        response_dict = {
            "error": "Restaurant not found"
        }
        response = make_response(
            jsonify(response_dict),
            404
        )
    return response

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()

        return '', 204
    else:
        response_dict = {
            "error": "Restaurant not found"
        }
        response = make_response(
            jsonify(response_dict),
            404
        )
    return response

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
