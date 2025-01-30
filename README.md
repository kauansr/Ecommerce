# Ecommerce

This is an e-commerce platform built using **Python** (with Django and Django REST Framework) for the backend, **JavaScript** (with React.js) for the frontend, and **PostgreSQL** as the database. It uses **JWT** (JSON Web Token) for user authentication and includes several key features such as product ratings, search filters, and a shopping cart system. However, please note that this version does not include notifications, email integration, payment system, or shipping cost calculation.

## Technologies Used

- **Backend**: Python, Django, Django REST Framework (DRF)
- **Frontend**: JavaScript, React.js
- **Database**: PostgreSQL
- **API Requests**: Axios
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: TestCase (Django test)

## Features

- **Product Listing**: Display a catalog of available products.
- **Product Detail Page**: Show detailed information about a selected product, including ratings.
- **Shopping Cart**: Users can add products to the cart and review them.
- **Checkout**: Users can review their cart and proceed with checkout (no payment system yet).
- **Product Ratings**: Users can rate products and see the average ratings.
- **Search Filters**: Users can filter products based on categories, price range, and other criteria.
- **JWT Authentication**: Secure user login and session management using JSON Web Tokens.

## Features Not Included

- **Notifications**: There is no notification system in this version.
- **Email Integration**: The platform does not send any email notifications at this time.
- **Payment System**: There is no payment gateway integrated. Orders cannot be completed through payments.
- **Shipping Cost Calculation**: Shipping fees are not calculated or integrated into the checkout process.

## Installation for Windows

### Backend (Django + DRF)

1. Clone the repository:
   ```bash
   git clone https://github.com/kauansr/Ecommerce.git
    ```

2. Follow the instructions:
    ```bash

    cd Ecommerce

    python -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

    Create a .env file in the root directory of the project and add the following:

    DEBUG=True
    SECRET_KEY=your_secret_key
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port

    Change the .env data with your postgreSQL credentials

    cd backend

    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver
   ```

### Frontend (React.js)

1. Follow the instructions:

    ```bash
    cd frontend

    npm install

    npm start
    ```