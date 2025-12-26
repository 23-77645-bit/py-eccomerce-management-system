from db.db_connection import db
from models.order import Order, OrderItem
from datetime import datetime


class OrderDAO:
    def create_tables(self):
        """Create the orders and order_items tables if they don't exist"""
        # Create orders table
        orders_query = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status ENUM('pending', 'paid', 'shipped', 'delivered') DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        
        # Create order_items table
        order_items_query = """
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """
        
        success1 = db.execute_query(orders_query)
        success2 = db.execute_query(order_items_query)
        return success1 and success2

    def create_order(self, user_id, total_amount, order_items):
        """Create a new order with its items"""
        try:
            # Start transaction
            db.connection.start_transaction()
            
            # Create the order
            order_query = """
            INSERT INTO orders (user_id, total_amount, status) 
            VALUES (%s, %s, 'pending')
            """
            db.execute_query(order_query, (user_id, total_amount))
            
            # Get the newly created order ID
            order_id = db.connection.insert_id()
            
            # Create order items
            for item in order_items:
                item_query = """
                INSERT INTO order_items (order_id, product_id, quantity, price) 
                VALUES (%s, %s, %s, %s)
                """
                db.execute_query(item_query, (order_id, item['product_id'], 
                                            item['quantity'], item['price']))
                
                # Update product stock
                update_stock_query = """
                UPDATE products SET stock = stock - %s WHERE id = %s
                """
                db.execute_query(update_stock_query, (item['quantity'], item['product_id']))
            
            # Commit transaction
            db.connection.commit()
            return order_id
            
        except Exception as e:
            # Rollback transaction on error
            db.connection.rollback()
            print(f"Error creating order: {e}")
            return None

    def get_order_by_id(self, order_id):
        """Get an order by ID"""
        query = "SELECT id, user_id, total_amount, status, order_date FROM orders WHERE id = %s"
        result = db.fetch_one(query, (order_id,))
        
        if result:
            return Order(
                order_id=result[0],
                user_id=result[1],
                total_amount=result[2],
                status=result[3],
                order_date=result[4]
            )
        return None

    def get_orders_by_user(self, user_id):
        """Get all orders for a specific user"""
        query = "SELECT id, user_id, total_amount, status, order_date FROM orders WHERE user_id = %s ORDER BY order_date DESC"
        results = db.fetch_all(query, (user_id,))
        
        orders = []
        for result in results:
            orders.append(Order(
                order_id=result[0],
                user_id=result[1],
                total_amount=result[2],
                status=result[3],
                order_date=result[4]
            ))
        return orders

    def get_all_orders(self):
        """Get all orders"""
        query = "SELECT id, user_id, total_amount, status, order_date FROM orders ORDER BY order_date DESC"
        results = db.fetch_all(query)
        
        orders = []
        for result in results:
            orders.append(Order(
                order_id=result[0],
                user_id=result[1],
                total_amount=result[2],
                status=result[3],
                order_date=result[4]
            ))
        return orders

    def update_order_status(self, order_id, status):
        """Update order status"""
        query = "UPDATE orders SET status = %s WHERE id = %s"
        return db.execute_query(query, (status, order_id))

    def get_order_items(self, order_id):
        """Get all items for a specific order"""
        query = "SELECT id, order_id, product_id, quantity, price FROM order_items WHERE order_id = %s"
        results = db.fetch_all(query, (order_id,))
        
        items = []
        for result in results:
            items.append(OrderItem(
                item_id=result[0],
                order_id=result[1],
                product_id=result[2],
                quantity=result[3],
                price=result[4]
            ))
        return items

    def get_sales_report(self):
        """Get sales report data"""
        query = """
        SELECT 
            DATE(order_date) as date, 
            COUNT(*) as orders_count, 
            SUM(total_amount) as total_revenue
        FROM orders 
        WHERE status IN ('paid', 'shipped', 'delivered')
        GROUP BY DATE(order_date)
        ORDER BY date DESC
        LIMIT 30
        """
        return db.fetch_all(query)

    def get_top_selling_products(self):
        """Get top selling products"""
        query = """
        SELECT 
            p.name,
            SUM(oi.quantity) as total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status IN ('paid', 'shipped', 'delivered')
        GROUP BY p.id, p.name
        ORDER BY total_sold DESC
        LIMIT 10
        """
        return db.fetch_all(query)