# django-shop-example

Welcome to the repository for the **django-shop-example** Django project! This project is a full-fledged e-commerce website that includes various features such as product management, customer management, shopping carts, cryptocurrency payments, email notifications, and English localization.

## Project Features

1. **Product, Customer, and Cart Models:** I have created data models for products, customers, and shopping carts to manage information about products, customers, and cart contents.

2. **Cryptocurrency Payments with Coinbase Commerce:** I integrated Coinbase Commerce to process cryptocurrency payments, allowing users to make purchases using various cryptocurrencies.

3. **Email Notifications:** I configured email notifications using SMTP to inform users about orders, order status changes, and other important events.

4. **English Localization:** To enhance accessibility for English-speaking users, I added English localization.

## Setting up Environment variables

Create a file .env in the root directory of the project and specify the necessary environment variables in it. Include the Django secret key, database settings, parameters forsending email notifications, and other configuration parameters.

**Example of the .env file:**    
    
    DB_NAME=db_name
    DB_USER=db_username
    DB_PASSWORD=db_password
    DB_HOST=db_hostname
    DB_PORT=5432
    SECRET_KEY=django_secret_key
    COINBASE_API_KEY=coinbase_secret_key
    COINBASE_WEBHOOK_SECRET=coinbase_webhook_secret
    EMAIL_HOST=YOUR.SMTP.DOMAIN
    EMAIL_HOST_USER=your_email@SMTP.DOMAIN
    EMAIL_HOST_PASSWORD=email_host_password
    NUMBER_OF_PRODUCTS_ON_MAIN_PAGE=int_number_of_products_on_page

<!-- ## How to Deploy the Website on a Server Using Docker

Follow these steps to deploy your website using Docker:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AlexDyakonov/django-shop-example.git

2. **To be continued:** -->