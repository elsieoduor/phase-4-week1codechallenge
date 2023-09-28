from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Define a Restaurant class as a database model
class Restaurant(db.Model, SerializerMixin):
    # Set the name of the database table
    __tablename__ = 'restaurants'

    # Define serialization rules for this model
    serialize_rules = ('-restaurant_pizzas.restaurant')

    # Define columns for the 'restaurants' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String)

    # Create a relationship with the 'RestaurantPizza' model, allowing access to related pizza data
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

    def __repr__(self):
        return f'<Restaurant {self.name}, located at {self.address}.'

# Define a Pizza class as a database model
class Pizza(db.Model, SerializerMixin):
    # Set the name of the database table
    __tablename__ = 'pizzas'

    # Define serialization rules for this model
    serialize_rules = ('-restaurant_pizzas.pizza')

    # Define columns for the 'pizzas' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Create a relationship with the 'RestaurantPizza' model, allowing access to related restaurant data
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def __repr__(self):
        return f'<Pizza {self.name}, created at {self.created_at}.'

# Define a RestaurantPizza class as a database model
class RestaurantPizza(db.Model, SerializerMixin):
    # Set the name of the database table
    __tablename__ = 'restaurant_pizzas'

    # Define serialization rules for this model
    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')

    # Define columns for the 'restaurant_pizzas' table
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define foreign key relationships to link this table with 'pizzas' and 'restaurants' tables
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    # Use the @validates decorator to validate the 'price' column
    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError('Invalid price')
        return price

    def __repr__(self):
        return f'<RestaurantPizza price {self.price}, updated at {self.updated_at}.>'
