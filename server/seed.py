from app import app, db, Restaurant, RestaurantPizza, Pizza
def create_sample_data():
    with app.app_context():
        db.create_all()

        restaurant1 = Restaurant(name="Dominoes", address="Embakasi")
        restaurant2 = Restaurant(name="Pizza Hut", address="Mombasa Rd")

   
        pizza1 = Pizza(name="Hawaiian", ingredients="Sauce, Cheese, Pineapple")
        pizza2 = Pizza(name="BBQ", ingredients="Sauce, Cheese, Streak")


        db.session.add(restaurant1)
        db.session.add(restaurant2)
        db.session.add(pizza1)
        db.session.add(pizza2)


        restaurant_pizza1 = RestaurantPizza(price=20, pizza=pizza1, restaurant=restaurant1)
        restaurant_pizza2 = RestaurantPizza(price=10, pizza=pizza2, restaurant=restaurant2)


        db.session.add(restaurant_pizza1)
        db.session.add(restaurant_pizza2)

        db.session.commit()
