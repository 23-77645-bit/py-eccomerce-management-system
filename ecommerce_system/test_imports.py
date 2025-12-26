"""
Test script to verify that all modules can be imported without errors
"""
def test_imports():
    try:
        print("Testing imports...")
        
        # Test database connection
        from db.db_connection import db
        print("✓ Database connection imported")
        
        # Test DAO modules
        from dao.user_dao import UserDAO
        from dao.product_dao import ProductDAO
        from dao.category_dao import CategoryDAO
        from dao.order_dao import OrderDAO
        print("✓ DAO modules imported")
        
        # Test model modules
        from models.user import User
        from models.product import Product
        from models.order import Order, OrderItem
        print("✓ Model modules imported")
        
        # Test utility modules
        from utils.security import hash_password, verify_password
        from utils.validators import validate_email, validate_password
        print("✓ Utility modules imported")
        
        # Test GUI modules
        # Note: We're not testing GUI imports since they require tkinter
        
        print("\nAll imports successful! The application structure is correct.")
        print("Note: The application requires a GUI environment with tkinter to run properly.")
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_imports()