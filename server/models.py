from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
  __tablename__ = 'restaurants'
  serialize_rules = ('-restaurant_pizzas.restaurant')

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)
  address = db.Column(db.String)

  restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

  def __repr__(self):
        return f'<Restaurant {self.name}, located at {self.address}.>'

class Pizza (db.Model, SerializerMixin):
  __tablename__='pizzas'
  serialize_rules = ('-restaurant_pizzas.pizza')

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  ingredients = db.Column(db.String)
  created_at = db.Column(db.DateTime, server_default = db.func.now())
  updated_at = db.Column(db.DateTime, onupdate=db.func.now())

  restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

  def __repr__(self):
        return f'<Pizza {self.name}, created at {self.created_at}.>'

class RestaurantPizza(db.Model, SerializerMixin):
  __tablename__='restaurant_pizzas'
  serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')

  id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, server_default = db.func.now())
  updated_at = db.Column(db.DateTime, onupdate=db.func.now())

  pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

  @validates('price')
  def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError('Invalid price')
        return price

  def __repr__(self):
        return f'<RestaurantPizza price {self.price}, updated at {self.updated_at}.>'