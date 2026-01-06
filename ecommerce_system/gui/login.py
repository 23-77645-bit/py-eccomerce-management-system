import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from ..dao.user_dao import UserDAO
from .admin_dashboard import AdminDashboard
from .customer_dashboard import CustomerDashboard


class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.user_dao = UserDAO()
        
        # Create login frame
        self.login_frame = ctk.CTkFrame(parent)
        self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Title
        self.label = ctk.CTkLabel(self.login_frame, text="E-Commerce Login", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        # Email entry
        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)
        
        # Login button
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        # Register button
        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.show_register)
        self.register_button.pack(pady=5)
        
        # Bind Enter key to login
        parent.bind('<Return>', lambda event: self.login())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        user = self.user_dao.authenticate_user(email, password)
        if user:
            # Close login window and open dashboard based on user role
            self.login_frame.destroy()
            
            if user.role == "admin":
                AdminDashboard(self.parent, user)
            else:
                CustomerDashboard(self.parent, user)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def show_register(self):
        # Create registration frame
        self.login_frame.destroy()
        self.register_frame = ctk.CTkFrame(self.parent)
        self.register_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        # Title
        self.label = ctk.CTkLabel(self.register_frame, text="User Registration", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        # Name entry
        self.name_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Full Name")
        self.name_entry.pack(pady=5)
        
        # Email entry
        self.email_entry_reg = ctk.CTkEntry(self.register_frame, placeholder_text="Email")
        self.email_entry_reg.pack(pady=5)
        
        # Password entry
        self.password_entry_reg = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.password_entry_reg.pack(pady=5)
        
        # Confirm password entry
        self.confirm_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=5)
        
        # Register button
        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(pady=10)
        
        # Back to login button
        self.back_button = ctk.CTkButton(self.register_frame, text="Back to Login", 
                                         command=self.show_login)
        self.back_button.pack(pady=5)

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry_reg.get().strip()
        password = self.password_entry_reg.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        if not name or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        # Check if user already exists
        existing_user = self.user_dao.get_user_by_email(email)
        if existing_user:
            messagebox.showerror("Error", "User with this email already exists")
            return
        
        # Create new user
        from ..models.user import User
        new_user = User(name=name, email=email, password=password, role='customer')
        
        if self.user_dao.create_user(new_user):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    def show_login(self):
        # Destroy register frame and show login
        self.register_frame.destroy()
        self.__init__(self.parent)