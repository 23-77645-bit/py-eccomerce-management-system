from db.db_connection import db


class CategoryDAO:
    def create_table(self):
        """Create the categories table if it doesn't exist"""
        query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        )
        """
        return db.execute_query(query)

    def create_category(self, name, description=None):
        """Create a new category"""
        query = """
        INSERT INTO categories (name, description) 
        VALUES (%s, %s)
        """
        params = (name, description)
        return db.execute_query(query, params)

    def get_category_by_id(self, category_id):
        """Get a category by ID"""
        query = "SELECT id, name, description FROM categories WHERE id = %s"
        result = db.fetch_one(query, (category_id,))
        return result  # Return tuple (id, name, description)

    def get_all_categories(self):
        """Get all categories"""
        query = "SELECT id, name, description FROM categories"
        results = db.fetch_all(query)
        return results  # Return list of tuples [(id, name, description), ...]

    def update_category(self, category_id, name, description=None):
        """Update a category"""
        query = """
        UPDATE categories 
        SET name = %s, description = %s 
        WHERE id = %s
        """
        params = (name, description, category_id)
        return db.execute_query(query, params)

    def delete_category(self, category_id):
        """Delete a category"""
        query = "DELETE FROM categories WHERE id = %s"
        return db.execute_query(query, (category_id,))