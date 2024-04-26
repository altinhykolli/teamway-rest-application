# Alt Coffee Shop Application

Welcome to the Alt Coffee Shop Application! This application is designed to manage employees and shifts at Alt Coffee Shop.

## Getting Started

To run this application locally, follow these steps:

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/altinhykolli/teamway-rest-application
    ```

2. **Install Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```

3. **Testing**

    To run the tests, execute the following command:

    ```bash
    python test.py
    ```

4. **Set Up MongoDB**: 
    - Install MongoDB on your system if you haven't already.
    - Start MongoDB server locally.

5. **Seed the Database**: 
    ```bash
    python seed.py
    ```

6. **Run the Application**: 
    ```bash
    python app.py
    ```

7. **Access the Application**: 
    Open your web browser and navigate to `http://localhost:5000`.

## Application Structure

- `app.py`: Flask application file containing the main application logic.
- `seed.py`: Script to seed the MongoDB database with initial employee data.
- `test.py`: Unit tests for testing various functionalities of the application.
- `templates/`: HTML templates for rendering the web pages.
- `static/`: Static files such as images and CSS stylesheets.

## Technologies Used

Flask: Web framework for building the application.
MongoDB: NoSQL database for storing employee data.
Flask-PyMongo: Flask extension for interacting with MongoDB.