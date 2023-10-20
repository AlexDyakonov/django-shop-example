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
    
    POSTGRES_DB=your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_pass
    POSTGRES_HOST=localhost # your host, default localhost
    POSTGRES_PORT=5432 # your port, default 5432

    SECRET_KEY=your_key

    COINBASE_API_KEY=your_key
    COINBASE_WEBHOOK_SECRET=your_secret

    EMAIL_HOST=your_host
    EMAIL_HOST_USER=your_user
    EMAIL_HOST_PASSWORD=your_pass

    NUMBER_OF_PRODUCTS_ON_MAIN_PAGE=your_number

    ALLOWED_HOST=your_host
    SCRF_SUBDOMAIN=*.your_domain
    DJANGO_SETTINGS_MODULE=shop.settings

    NGINX_EXTERNAL_PORT=80 # your port, default 80
    NGINX_EXTERNAL_SSL_PORT=443 # your port, default 443

## How to Deploy the Website on a Server Using Docker

Follow these steps to deploy your website using Docker:

1. Clone the Repository:

   ```bash
   git clone https://github.com/AlexDyakonov/django-shop-example.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-shop-example/shop/
   ```

3. Build the Docker containers:

   ```bash
   docker-compose build
   ```

4. Start the Docker containers:

   ```bash
   docker-compose up -d
   ```

5. To stop the Docker containers:

   ```bash
   docker-compose down
   ```
