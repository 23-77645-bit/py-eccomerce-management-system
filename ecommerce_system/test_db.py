"""
Test script to verify database connection and table creation
"""
def test_db():
    try:
        print("Testing database connection and table creation...")
        
        # Import database components
        from db.db_connection import db
        from dao.user_dao import UserDAO
        from dao.product_dao import ProductDAO
        from dao.category_dao import CategoryDAO
        from dao.order_dao import OrderDAO
        
        # Try to connect to database
        if not db.connect():
            print("✗ Database connection failed")
            print("Note: Make sure MySQL server is running and credentials in config.py are correct")
            return False
        
        print("✓ Database connection successful")
        
        # Create DAO instances
        user_dao = UserDAO()
        product_dao = ProductDAO()
        category_dao = CategoryDAO()
        order_dao = OrderDAO()
        
        # Create tables
        user_dao.create_table()
        category_dao.create_table()
        product_dao.create_table()
        order_dao.create_tables()
        
        print("✓ All tables created successfully")
        
        # Close database connection
        db.disconnect()
        
        print("\nDatabase test completed successfully!")
        print("Note: The actual database tables have been created in your MySQL server.")
        
    except Exception as e:
        print(f"Database test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_db()