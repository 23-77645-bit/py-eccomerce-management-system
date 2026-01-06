from ..db.db_connection import db
from ..models.user import User
from ..utils.security import hash_password, verify_password


class UserDAO:
    def create_table(self):
        """Create the users table if it doesn't exist"""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'customer') DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        return db.execute_query(query)

    def create_user(self, user):
        """Create a new user"""
        # Hash the password before storing
        hashed_password = hash_password(user.password)
        
        query = """
        INSERT INTO users (name, email, password, role) 
        VALUES (%s, %s, %s, %s)
        """
        params = (user.name, user.email, hashed_password, user.role)
        return db.execute_query(query, params)

    def get_user_by_email(self, email):
        """Get a user by email"""
        query = "SELECT id, name, email, password, role, created_at FROM users WHERE email = %s"
        result = db.fetch_one(query, (email,))
        
        if result:
            return User(
                user_id=result[0],
                name=result[1],
                email=result[2],
                password=result[3],
                role=result[4],
                created_at=result[5]
            )
        return None

    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        query = "SELECT id, name, email, password, role, created_at FROM users WHERE id = %s"
        result = db.fetch_one(query, (user_id,))
        
        if result:
            return User(
                user_id=result[0],
                name=result[1],
                email=result[2],
                password=result[3],
                role=result[4],
                created_at=result[5]
            )
        return None

    def get_all_users(self):
        """Get all users"""
        query = "SELECT id, name, email, password, role, created_at FROM users"
        results = db.fetch_all(query)
        
        users = []
        for result in results:
            users.append(User(
                user_id=result[0],
                name=result[1],
                email=result[2],
                password=result[3],
                role=result[4],
                created_at=result[5]
            ))
        return users

    def update_user(self, user):
        """Update a user"""
        query = """
        UPDATE users 
        SET name = %s, email = %s, role = %s 
        WHERE id = %s
        """
        params = (user.name, user.email, user.role, user.id)
        return db.execute_query(query, params)

    def delete_user(self, user_id):
        """Delete a user"""
        query = "DELETE FROM users WHERE id = %s"
        return db.execute_query(query, (user_id,))

    def authenticate_user(self, email, password):
        """Authenticate a user by email and password"""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.password):
            # Create a new user object without the password for security
            return User(
                user_id=user.id,
                name=user.name,
                email=user.email,
                password=None,  # Don't return the password
                role=user.role,
                created_at=user.created_at
            )
        return None