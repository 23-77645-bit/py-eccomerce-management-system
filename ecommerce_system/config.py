import os

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Password for MySQL root user
    'database': 'ecommerce_db',
    'charset': 'utf8mb4'
}

# Application Configuration
APP_NAME = "E-Commerce Management System"
VERSION = "1.0.0"

# Paths
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
IMAGES_PATH = os.path.join(ASSETS_PATH, 'images')