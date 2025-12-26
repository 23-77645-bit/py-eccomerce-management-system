from db.db_connection import db
from models.product import Product


class ProductDAO:
    def create_table(self):
        """Create the products table if it doesn't exist"""
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL DEFAULT 0,
            image VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        )
        """
        return db.execute_query(query)

    def create_product(self, product):
        """Create a new product"""
        query = """
        INSERT INTO products (category_id, name, description, price, stock, image) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (product.category_id, product.name, product.description, 
                  product.price, product.stock, product.image)
        return db.execute_query(query, params)

    def get_product_by_id(self, product_id):
        """Get a product by ID"""
        query = "SELECT id, category_id, name, description, price, stock, image, created_at FROM products WHERE id = %s"
        result = db.fetch_one(query, (product_id,))
        
        if result:
            return Product(
                product_id=result[0],
                category_id=result[1],
                name=result[2],
                description=result[3],
                price=result[4],
                stock=result[5],
                image=result[6],
                created_at=result[7]
            )
        return None

    def get_all_products(self):
        """Get all products"""
        query = "SELECT id, category_id, name, description, price, stock, image, created_at FROM products"
        results = db.fetch_all(query)
        
        products = []
        for result in results:
            products.append(Product(
                product_id=result[0],
                category_id=result[1],
                name=result[2],
                description=result[3],
                price=result[4],
                stock=result[5],
                image=result[6],
                created_at=result[7]
            ))
        return products

    def get_products_by_category(self, category_id):
        """Get products by category ID"""
        query = "SELECT id, category_id, name, description, price, stock, image, created_at FROM products WHERE category_id = %s"
        results = db.fetch_all(query, (category_id,))
        
        products = []
        for result in results:
            products.append(Product(
                product_id=result[0],
                category_id=result[1],
                name=result[2],
                description=result[3],
                price=result[4],
                stock=result[5],
                image=result[6],
                created_at=result[7]
            ))
        return products

    def get_products_by_name(self, name):
        """Get products by name (partial match)"""
        query = "SELECT id, category_id, name, description, price, stock, image, created_at FROM products WHERE name LIKE %s"
        results = db.fetch_all(query, (f"%{name}%",))
        
        products = []
        for result in results:
            products.append(Product(
                product_id=result[0],
                category_id=result[1],
                name=result[2],
                description=result[3],
                price=result[4],
                stock=result[5],
                image=result[6],
                created_at=result[7]
            ))
        return products

    def update_product(self, product):
        """Update a product"""
        query = """
        UPDATE products 
        SET category_id = %s, name = %s, description = %s, price = %s, stock = %s, image = %s 
        WHERE id = %s
        """
        params = (product.category_id, product.name, product.description, 
                  product.price, product.stock, product.image, product.id)
        return db.execute_query(query, params)

    def delete_product(self, product_id):
        """Delete a product"""
        query = "DELETE FROM products WHERE id = %s"
        return db.execute_query(query, (product_id,))

    def update_stock(self, product_id, new_stock):
        """Update product stock"""
        query = "UPDATE products SET stock = %s WHERE id = %s"
        return db.execute_query(query, (new_stock, product_id))