import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from dao.user_dao import UserDAO
from dao.product_dao import ProductDAO
from dao.category_dao import CategoryDAO
from dao.order_dao import OrderDAO
from gui.analytics import AnalyticsDashboard


class AdminDashboard:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.user_dao = UserDAO()
        self.product_dao = ProductDAO()
        self.category_dao = CategoryDAO()
        self.order_dao = OrderDAO()
        
        # Configure parent window
        self.parent.title(f"Admin Dashboard - {user.name}")
        self.parent.geometry("800x600")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Create navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame)
        self.nav_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        # Navigation buttons
        self.users_btn = ctk.CTkButton(self.nav_frame, text="Manage Users", command=self.show_users)
        self.users_btn.pack(side="left", padx=5)
        
        self.products_btn = ctk.CTkButton(self.nav_frame, text="Manage Products", command=self.show_products)
        self.products_btn.pack(side="left", padx=5)
        
        self.categories_btn = ctk.CTkButton(self.nav_frame, text="Manage Categories", command=self.show_categories)
        self.categories_btn.pack(side="left", padx=5)
        
        self.orders_btn = ctk.CTkButton(self.nav_frame, text="View Orders", command=self.show_orders)
        self.orders_btn.pack(side="left", padx=5)
        
        self.analytics_btn = ctk.CTkButton(self.nav_frame, text="Analytics", command=self.show_analytics)
        self.analytics_btn.pack(side="left", padx=5)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show initial view (users)
        self.show_users()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_users(self):
        """Show the user management view"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Manage Users", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Create user form
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Name entry
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.user_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Full Name")
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email entry
        ctk.CTkLabel(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.user_email_entry = ctk.CTkEntry(form_frame, placeholder_text="Email")
        self.user_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Password entry
        ctk.CTkLabel(form_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.user_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Password", show="*")
        self.user_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Role selection
        ctk.CTkLabel(form_frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.user_role_var = ctk.StringVar(value="customer")
        role_combo = ctk.CTkComboBox(form_frame, values=["admin", "customer"], variable=self.user_role_var)
        role_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Add user button
        add_user_btn = ctk.CTkButton(form_frame, text="Add User", command=self.add_user)
        add_user_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Users list
        users_frame = ctk.CTkFrame(self.content_frame)
        users_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox for users
        self.users_listbox = tk.Listbox(users_frame)
        self.users_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for user operations
        buttons_frame = ctk.CTkFrame(users_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        delete_user_btn = ctk.CTkButton(buttons_frame, text="Delete User", command=self.delete_user)
        delete_user_btn.pack(side="left", padx=5)
        
        # Load users
        self.load_users()

    def load_users(self):
        """Load and display all users"""
        self.users_listbox.delete(0, tk.END)
        users = self.user_dao.get_all_users()
        for user in users:
            self.users_listbox.insert(tk.END, f"{user.id}: {user.name} ({user.email}) - {user.role}")

    def add_user(self):
        """Add a new user"""
        name = self.user_name_entry.get().strip()
        email = self.user_email_entry.get().strip()
        password = self.user_password_entry.get().strip()
        role = self.user_role_var.get()
        
        if not name or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Check if user already exists
        existing_user = self.user_dao.get_user_by_email(email)
        if existing_user:
            messagebox.showerror("Error", "User with this email already exists")
            return
        
        from models.user import User
        new_user = User(name=name, email=email, password=password, role=role)
        
        if self.user_dao.create_user(new_user):
            messagebox.showinfo("Success", "User added successfully!")
            self.user_name_entry.delete(0, tk.END)
            self.user_email_entry.delete(0, tk.END)
            self.user_password_entry.delete(0, tk.END)
            self.load_users()
        else:
            messagebox.showerror("Error", "Failed to add user")

    def delete_user(self):
        """Delete selected user"""
        selection = self.users_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a user to delete")
            return
        
        user_info = self.users_listbox.get(selection[0])
        user_id = int(user_info.split(":")[0])
        
        # Don't allow deleting own account
        if user_id == self.user.id:
            messagebox.showerror("Error", "Cannot delete your own account")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            if self.user_dao.delete_user(user_id):
                messagebox.showinfo("Success", "User deleted successfully!")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to delete user")

    def show_products(self):
        """Show the product management view"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Manage Products", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Create product form
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Product details
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.prod_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Product Name")
        self.prod_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.prod_desc_entry = ctk.CTkEntry(form_frame, placeholder_text="Description")
        self.prod_desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.prod_price_entry = ctk.CTkEntry(form_frame, placeholder_text="Price")
        self.prod_price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Stock:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.prod_stock_entry = ctk.CTkEntry(form_frame, placeholder_text="Stock Quantity")
        self.prod_stock_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Category selection
        ctk.CTkLabel(form_frame, text="Category:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        categories = self.category_dao.get_all_categories()
        category_names = [cat[1] for cat in categories]  # Get category names
        self.prod_category_var = ctk.StringVar()
        self.prod_category_combo = ctk.CTkComboBox(form_frame, values=category_names, variable=self.prod_category_var)
        self.prod_category_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # Add product button
        add_prod_btn = ctk.CTkButton(form_frame, text="Add Product", command=self.add_product)
        add_prod_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Products list
        products_frame = ctk.CTkFrame(self.content_frame)
        products_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox for products
        self.products_listbox = tk.Listbox(products_frame)
        self.products_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for product operations
        buttons_frame = ctk.CTkFrame(products_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        delete_prod_btn = ctk.CTkButton(buttons_frame, text="Delete Product", command=self.delete_product)
        delete_prod_btn.pack(side="left", padx=5)
        
        # Load products
        self.load_products()

    def load_products(self):
        """Load and display all products"""
        self.products_listbox.delete(0, tk.END)
        products = self.product_dao.get_all_products()
        for product in products:
            self.products_listbox.insert(tk.END, f"{product.id}: {product.name} - ${product.price} ({product.stock} in stock)")

    def add_product(self):
        """Add a new product"""
        name = self.prod_name_entry.get().strip()
        description = self.prod_desc_entry.get().strip()
        try:
            price = float(self.prod_price_entry.get().strip())
            stock = int(self.prod_stock_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Price and stock must be valid numbers")
            return
        
        if not name:
            messagebox.showerror("Error", "Product name is required")
            return
        
        # Get category ID
        category_name = self.prod_category_var.get()
        categories = self.category_dao.get_all_categories()
        category_id = None
        for cat in categories:
            if cat[1] == category_name:
                category_id = cat[0]
                break
        
        from models.product import Product
        new_product = Product(name=name, description=description, price=price, 
                              stock=stock, category_id=category_id)
        
        if self.product_dao.create_product(new_product):
            messagebox.showinfo("Success", "Product added successfully!")
            self.prod_name_entry.delete(0, tk.END)
            self.prod_desc_entry.delete(0, tk.END)
            self.prod_price_entry.delete(0, tk.END)
            self.prod_stock_entry.delete(0, tk.END)
            self.load_products()
        else:
            messagebox.showerror("Error", "Failed to add product")

    def delete_product(self):
        """Delete selected product"""
        selection = self.products_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to delete")
            return
        
        prod_info = self.products_listbox.get(selection[0])
        prod_id = int(prod_info.split(":")[0])
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            if self.product_dao.delete_product(prod_id):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()
            else:
                messagebox.showerror("Error", "Failed to delete product")

    def show_categories(self):
        """Show the category management view"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Manage Categories", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Create category form
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Category details
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cat_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Category Name")
        self.cat_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cat_desc_entry = ctk.CTkEntry(form_frame, placeholder_text="Description")
        self.cat_desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Add category button
        add_cat_btn = ctk.CTkButton(form_frame, text="Add Category", command=self.add_category)
        add_cat_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Categories list
        categories_frame = ctk.CTkFrame(self.content_frame)
        categories_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox for categories
        self.categories_listbox = tk.Listbox(categories_frame)
        self.categories_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for category operations
        buttons_frame = ctk.CTkFrame(categories_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        delete_cat_btn = ctk.CTkButton(buttons_frame, text="Delete Category", command=self.delete_category)
        delete_cat_btn.pack(side="left", padx=5)
        
        # Load categories
        self.load_categories()

    def load_categories(self):
        """Load and display all categories"""
        self.categories_listbox.delete(0, tk.END)
        categories = self.category_dao.get_all_categories()
        for cat in categories:
            self.categories_listbox.insert(tk.END, f"{cat[0]}: {cat[1]}")

    def add_category(self):
        """Add a new category"""
        name = self.cat_name_entry.get().strip()
        description = self.cat_desc_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Category name is required")
            return
        
        if self.category_dao.create_category(name, description):
            messagebox.showinfo("Success", "Category added successfully!")
            self.cat_name_entry.delete(0, tk.END)
            self.cat_desc_entry.delete(0, tk.END)
            self.load_categories()
        else:
            messagebox.showerror("Error", "Failed to add category")

    def delete_category(self):
        """Delete selected category"""
        selection = self.categories_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a category to delete")
            return
        
        cat_info = self.categories_listbox.get(selection[0])
        cat_id = int(cat_info.split(":")[0])
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
            if self.category_dao.delete_category(cat_id):
                messagebox.showinfo("Success", "Category deleted successfully!")
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to delete category")

    def show_orders(self):
        """Show the orders view"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="All Orders", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Orders list
        orders_frame = ctk.CTkFrame(self.content_frame)
        orders_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox for orders
        self.orders_listbox = tk.Listbox(orders_frame)
        self.orders_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for order operations
        buttons_frame = ctk.CTkFrame(orders_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Status update buttons
        self.status_var = ctk.StringVar(value="pending")
        status_combo = ctk.CTkComboBox(buttons_frame, values=["pending", "paid", "shipped", "delivered"], 
                                       variable=self.status_var)
        status_combo.pack(side="left", padx=5)
        
        update_status_btn = ctk.CTkButton(buttons_frame, text="Update Status", command=self.update_order_status)
        update_status_btn.pack(side="left", padx=5)
        
        # Load orders
        self.load_orders()

    def load_orders(self):
        """Load and display all orders"""
        self.orders_listbox.delete(0, tk.END)
        orders = self.order_dao.get_all_orders()
        for order in orders:
            self.orders_listbox.insert(tk.END, f"{order.id}: User {order.user_id} - ${order.total_amount} - {order.status}")

    def update_order_status(self):
        """Update the status of selected order"""
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an order to update")
            return
        
        order_info = self.orders_listbox.get(selection[0])
        order_id = int(order_info.split(":")[0])
        new_status = self.status_var.get()
        
        if self.order_dao.update_order_status(order_id, new_status):
            messagebox.showinfo("Success", "Order status updated successfully!")
            self.load_orders()
        else:
            messagebox.showerror("Error", "Failed to update order status")

    def show_analytics(self):
        """Open the analytics dashboard"""
        # Clear the current frame and open analytics
        self.main_frame.destroy()
        AnalyticsDashboard(self.parent, self.user)