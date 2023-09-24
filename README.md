
# Pizza Restaurants

Pizza Restaurants

## Description

This Flask API project is designed to manage a Pizza Restaurant domain, including Restaurants, Pizzas, and their associations through the RestaurantPizza model. Below, you will find information on how to run the project, the database models, validations, and the available API routes.
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)


## Getting Started

Before running the API, follow these steps to set up the project:

### Prerequisites

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (for database migrations)

### Installation

1. Clone this repository to your local machine:

   ```bash
   $ git clone https://github.com/yourusername/yourproject.git
   $ cd yourproject
   ```

2. Create a virtual environment and activate it (optional but recommended):

   ```bash
   $ python -m venv venv
   $ source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   $ pip install -r requirements.txt
   ```

4. Initialize the database and run migrations:

   ```bash
   $ flask db init
   $ flask db migrate
   $ flask db upgrade
   ```

5. Start the Flask server:

   ```bash
   $ flask run
   ```

Now, your Flask server should be up and running.

## Models

In this project, we have the following database models:

- **Restaurant**: Represents a pizza restaurant.
  - Attributes:
    - `id`: Integer (Primary Key)
    - `name`: String (Max Length: 50, Unique)
    - `address`: String

- **Pizza**: Represents a type of pizza.
  - Attributes:
    - `id`: Integer (Primary Key)
    - `name`: String
    - `ingredients`: String

- **RestaurantPizza**: Represents the association between a Restaurant and a Pizza, along with pricing information.
  - Attributes:
    - `id`: Integer (Primary Key)
    - `price`: Integer (Validation: Must be between 1 and 30)
    - `pizza_id`: Integer (Foreign Key to Pizza)
    - `restaurant_id`: Integer (Foreign Key to Restaurant)

## Validations

We have implemented the following validations in the project:

- **Restaurant Model**:
  - `name` must be less than 50 characters in length.
  - `name` must be unique.

- **RestaurantPizza Model**:
  - `price` must be between 1 and 30.

## API Routes

The API provides the following routes with the specified functionality:

- **GET /restaurants**:
  - Returns a list of restaurants in the following format:

    ```json
    [
      {
        "id": 1,
        "name": "Dominion Pizza",
        "address": "Good Italian, Ngong Road, 5th Avenue"
      },
      {
        "id": 2,
        "name": "Pizza Hut",
        "address": "Westgate Mall, Mwanzi Road, Nrb 100"
      }
    ]
    ```

- **GET /restaurants/:id**:
  - Returns restaurant details along with associated pizzas (if the restaurant exists) in the following format:

    ```json
    {
      "id": 1,
      "name": "Dominion Pizza",
      "address": "Good Italian, Ngong Road, 5th Avenue",
      "pizzas": [
        {
          "id": 1,
          "name": "Cheese",
          "ingredients": "Dough, Tomato Sauce, Cheese"
        },
        {
          "id": 2,
          "name": "Pepperoni",
          "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
        }
      ]
    }
    ```

  - If the restaurant does not exist, it returns the following JSON data along with the appropriate HTTP status code:

    ```json
    {
      "error": "Restaurant not found"
    }
    ```

- **DELETE /restaurants/:id**:
  - Deletes a restaurant and associated restaurant-pizza relationships (if the restaurant exists).
  - Returns an empty response body along with the appropriate HTTP status code.
  - If the restaurant does not exist, it returns the following JSON data along with the appropriate HTTP status code:

    ```json
    {
      "error": "Restaurant not found"
    }
    ```

- **GET /pizzas**:
  - Returns a list of pizza types in the following format:

    ```json
    [
      {
        "id": 1,
        "name": "Cheese",
        "ingredients": "Dough, Tomato Sauce, Cheese"
      },
      {
        "id": 2,
        "name": "Pepperoni",
        "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
      }
    ]
    ```

- **POST /restaurant_pizzas**:
  - Creates a new RestaurantPizza associated with an existing Pizza and Restaurant.
  - Accepts an object with the following properties in the request body:

    ```json
    {
      "price": 5,
      "pizza_id": 1,
      "restaurant_id": 3
    }
    ```

  - If the RestaurantPizza is created successfully, it sends back a response with data related to the Pizza:

    ```json
    {
      "id": 1,
      "name": "Cheese",
      "ingredients": "Dough, Tomato Sauce, Cheese"
    }
    ```

  - If the RestaurantPizza is not created successfully (e.g., due to validation errors), it returns the following JSON data along with the appropriate HTTP status code:

    ```json
    {
      "errors": ["Validation errors"]
    }
    ```

## Testing the Endpoints

You can test the API endpoints using your preferred method, such as Postman or `curl`. Make sure the Flask server is running, and refer to the API route descriptions above for the expected request and response formats.


## Acknowledgments

This project was created as part of a Flask code challenge. Thank you for exploring this Flask API project, and happy coding!# Flask Code Challenge - Pizza Restaurants

## License

Specify the license under which your project is distributed. Include a link to the license file if available.

```markdown
This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.
```

## Contributing

If you want to encourage contributions from other developers, provide guidelines on how they can contribute to your project. Mention the process for submitting pull requests and any coding standards they should follow.
