# Database Setup for E-Commerce Management System

## Overview
This project uses MariaDB/MySQL database to store e-commerce data. The database configuration is already set up in `config.py`.

## Database Configuration
- Host: localhost
- User: root
- Password: password (as configured in config.py)
- Database: ecommerce_db
- Charset: utf8mb4

## Database Schema
The following tables are created automatically:
- users: Stores user information (customers and admins)
- categories: Product categories
- products: Product information
- orders: Order records
- order_items: Items within each order

## Running the Application
1. Make sure MariaDB/MySQL service is running:
   ```bash
   service mariadb start
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the database initialization script (if needed):
   ```bash
   python test_db.py
   ```

4. Run the main application:
   ```bash
   python main.py
   ```

## Troubleshooting
- If you get "Access denied" errors, make sure the database user credentials in `config.py` match your database setup
- If tables don't exist, run `python test_db.py` to create them
- If the database service isn't running, start it with `service mariadb start`