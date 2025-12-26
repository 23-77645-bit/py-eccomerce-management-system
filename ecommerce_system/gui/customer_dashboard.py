import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from dao.user_dao import UserDAO
from dao.product_dao import ProductDAO
from dao.category_dao import CategoryDAO
from dao.order_dao import OrderDAO
from gui.cart import CartWindow


class CustomerDashboard:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.user_dao = UserDAO()
        self.product_dao = ProductDAO()
        self.category_dao = CategoryDAO()
        self.order_dao = OrderDAO()
        self.cart = []  # Cart items
        
        # Configure parent window
        self.parent.title(f"Customer Dashboard - {user.name}")
        self.parent.geometry("900x700")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Create navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame)
        self.nav_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        # Navigation buttons
        self.products_btn = ctk.CTkButton(self.nav_frame, text="Browse Products", command=self.show_products)
        self.products_btn.pack(side="left", padx=5)
        
        self.cart_btn = ctk.CTkButton(self.nav_frame, text="View Cart", command=self.show_cart)
        self.cart_btn.pack(side="left", padx=5)
        
        self.orders_btn = ctk.CTkButton(self.nav_frame, text="My Orders", command=self.show_orders)
        self.orders_btn.pack(side="left", padx=5)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show initial view (products)
        self.show_products()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_products(self):
        """Show the products browsing view"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Browse Products", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Search and filter frame
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Search
        ctk.CTkLabel(filter_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search products...")
        self.search_entry.pack(side="left", padx=5)
        search_btn = ctk.CTkButton(filter_frame, text="Search", command=self.search_products)
        search_btn.pack(side="left", padx=5)
        
        # Category filter
        ctk.CTkLabel(filter_frame, text="Category:").pack(side="left", padx=(20, 5))
        categories = self.category_dao.get_all_categories()
        category_names = ["All"] + [cat[1] for cat in categories]  # Add "All" option
        self.category_var = ctk.StringVar(value="All")
        category_combo = ctk.CTkComboBox(filter_frame, values=category_names, variable=self.category_var)
        category_combo.pack(side="left", padx=5)
        category_combo.bind("<Configure>", lambda e: self.filter_products())
        
        # Products list
        products_frame = ctk.CTkFrame(self.content_frame)
        products_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a frame with canvas and scrollbar for products
        canvas_frame = ctk.CTkFrame(products_frame)
        canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(canvas_frame)
        scrollbar = ctk.CTkScrollbar(canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load products
        self.load_products()

    def load_products(self):
        """Load and display all products"""
        # Clear existing product widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        products = self.product_dao.get_all_products()
        self.display_products(products)

    def display_products(self, products):
        """Display products in the scrollable frame"""
        # Clear existing product widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Display products in a grid
        row_frame = None
        col_count = 0
        
        for i, product in enumerate(products):
            if col_count == 0:  # Start a new row every 3 products
                row_frame = ctk.CTkFrame(self.scrollable_frame)
                row_frame.pack(fill="x", padx=5, pady=5)
                col_count = 0
            
            # Create product card
            product_frame = ctk.CTkFrame(row_frame)
            product_frame.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            
            # Product image if available
            if product.image and product.image != "No image selected":
                try:
                    from PIL import Image, ImageTk
                    # Load and resize image
                    img = Image.open(product.image)
                    img = img.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Store reference to prevent garbage collection
                    img_label = ctk.CTkLabel(product_frame, image=photo, text="")
                    img_label.image = photo  # Keep a reference
                    img_label.pack(pady=5)
                except Exception:
                    # If image loading fails, show a placeholder
                    img_label = ctk.CTkLabel(product_frame, text="No Image", height=100)
                    img_label.pack(pady=5)
            else:
                img_label = ctk.CTkLabel(product_frame, text="No Image", height=100)
                img_label.pack(pady=5)
            
            # Product details
            name_label = ctk.CTkLabel(product_frame, text=product.name, 
                                      font=ctk.CTkFont(size=14, weight="bold"))
            name_label.pack(pady=5)
            
            desc_label = ctk.CTkLabel(product_frame, text=product.description or "No description", 
                                      wraplength=150)
            desc_label.pack(pady=2)
            
            price_label = ctk.CTkLabel(product_frame, text=f"${product.price:.2f}")
            price_label.pack(pady=2)
            
            stock_label = ctk.CTkLabel(product_frame, text=f"In Stock: {product.stock}")
            stock_label.pack(pady=2)
            
            # Add to cart button
            add_to_cart_btn = ctk.CTkButton(
                product_frame, 
                text="Add to Cart", 
                command=lambda p=product: self.add_to_cart(p)
            )
            add_to_cart_btn.pack(pady=5)
            
            col_count += 1
            if col_count >= 3:  # 3 products per row
                col_count = 0

    def search_products(self):
        """Search products by name"""
        search_term = self.search_entry.get().strip()
        if search_term:
            products = self.product_dao.get_products_by_name(search_term)
        else:
            products = self.product_dao.get_all_products()
        
        self.display_products(products)

    def filter_products(self):
        """Filter products by category"""
        selected_category = self.category_var.get()
        if selected_category == "All" or not selected_category:
            products = self.product_dao.get_all_products()
        else:
            # Get category ID by name
            categories = self.category_dao.get_all_categories()
            category_id = None
            for cat in categories:
                if cat[1] == selected_category:
                    category_id = cat[0]
                    break
            
            if category_id:
                products = self.product_dao.get_products_by_category(category_id)
            else:
                products = []
        
        self.display_products(products)

    def add_to_cart(self, product):
        """Add a product to the cart"""
        if product.stock <= 0:
            messagebox.showerror("Error", f"{product.name} is out of stock!")
            return
        
        # Check if product is already in cart
        for item in self.cart:
            if item['product'].id == product.id:
                # Ask for quantity
                quantity = tk.simpledialog.askinteger(
                    "Quantity", 
                    f"How many {product.name} would you like to add?", 
                    minvalue=1, 
                    maxvalue=product.stock - item['quantity']
                )
                if quantity:
                    item['quantity'] += quantity
                    messagebox.showinfo("Success", f"Added {quantity} more {product.name} to cart!")
                return
        
        # Ask for quantity
        quantity = tk.simpledialog.askinteger(
            "Quantity", 
            f"How many {product.name} would you like to add?", 
            minvalue=1, 
            maxvalue=product.stock
        )
        if quantity:
            self.cart.append({
                'product': product,
                'quantity': quantity
            })
            messagebox.showinfo("Success", f"Added {quantity} {product.name} to cart!")

    def show_cart(self):
        """Show the shopping cart"""
        # Create a new window for the cart
        cart_window = ctk.CTkToplevel(self.parent)
        cart_window.title("Shopping Cart")
        cart_window.geometry("600x500")
        
        CartWindow(cart_window, self.user, self.cart, self.order_dao, self.product_dao, self.cart_updated)

    def cart_updated(self):
        """Callback when cart is updated"""
        # This function is called when the cart window is closed
        pass

    def show_orders(self):
        """Show the user's order history"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="My Order History", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Orders list
        orders_frame = ctk.CTkFrame(self.content_frame)
        orders_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox for orders
        self.orders_listbox = tk.Listbox(orders_frame)
        self.orders_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Order details text area
        details_frame = ctk.CTkFrame(orders_frame)
        details_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(details_frame, text="Order Details:").pack(anchor="w", padx=5)
        self.order_details_text = tk.Text(details_frame, height=8)
        self.order_details_text.pack(fill="x", padx=5, pady=5)
        
        # Load orders
        self.load_orders()

    def load_orders(self):
        """Load and display user's orders"""
        self.orders_listbox.delete(0, tk.END)
        orders = self.order_dao.get_orders_by_user(self.user.id)
        for order in orders:
            self.orders_listbox.insert(tk.END, f"{order.id}: ${order.total_amount:.2f} - {order.status}")
        
        # Bind selection event
        self.orders_listbox.bind('<<ListboxSelect>>', self.show_order_details)

    def show_order_details(self, event):
        """Show details of selected order"""
        selection = self.orders_listbox.curselection()
        if not selection:
            return
        
        order_info = self.orders_listbox.get(selection[0])
        order_id = int(order_info.split(":")[0])
        
        # Clear previous details
        self.order_details_text.delete(1.0, tk.END)
        
        # Get order items
        order_items = self.order_dao.get_order_items(order_id)
        
        # Display order items
        details = f"Order #{order_id} Details:\n\n"
        for item in order_items:
            # Get product name
            product = self.product_dao.get_product_by_id(item.product_id)
            product_name = product.name if product else "Unknown Product"
            details += f"- {product_name}: {item.quantity} x ${item.price:.2f} = ${item.quantity * item.price:.2f}\n"
        
        self.order_details_text.insert(tk.END, details)