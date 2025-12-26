import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from db.db_connection import db
from dao.user_dao import UserDAO
from dao.product_dao import ProductDAO
from dao.category_dao import CategoryDAO
from dao.order_dao import OrderDAO
from gui.login import LoginWindow


class ECommerceApp:
    def __init__(self):
        # Initialize database connection
        if not db.connect():
            messagebox.showerror("Database Error", "Failed to connect to database!")
            return
        
        # Create tables if they don't exist
        user_dao = UserDAO()
        product_dao = ProductDAO()
        category_dao = CategoryDAO()
        order_dao = OrderDAO()
        
        user_dao.create_table()
        category_dao.create_table()  # Categories need to be created before products
        product_dao.create_table()
        order_dao.create_tables()
        
        # Initialize the login window
        self.root = ctk.CTk()
        self.root.title("E-Commerce Management System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Initialize login window
        LoginWindow(self.root)
        
        # Start the application
        self.root.mainloop()


if __name__ == "__main__":
    app = ECommerceApp()