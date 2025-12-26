import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO


class CartWindow:
    def __init__(self, parent, user, cart, order_dao, product_dao, callback):
        self.parent = parent
        self.user = user
        self.cart = cart
        self.order_dao = order_dao
        self.product_dao = product_dao
        self.callback = callback
        
        # Configure parent window
        self.parent.title("Shopping Cart")
        self.parent.geometry("600x500")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(self.main_frame, text="Your Shopping Cart", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Cart items list
        cart_frame = ctk.CTkFrame(self.main_frame)
        cart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a frame with canvas and scrollbar for cart items
        canvas_frame = ctk.CTkFrame(cart_frame)
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
        
        # Total and checkout frame
        total_frame = ctk.CTkFrame(self.main_frame)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        self.total_label = ctk.CTkLabel(total_frame, text="Total: $0.00", 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.total_label.pack(side="left", padx=10)
        
        checkout_btn = ctk.CTkButton(total_frame, text="Checkout", command=self.checkout)
        checkout_btn.pack(side="right", padx=10)
        
        # Load cart items
        self.load_cart_items()

    def load_cart_items(self):
        """Load and display cart items"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.cart:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Your cart is empty!",
                                       font=ctk.CTkFont(size=14))
            empty_label.pack(pady=50)
            return
        
        total = 0.0
        for i, item in enumerate(self.cart):
            product = item['product']
            quantity = item['quantity']
            item_total = product.price * quantity
            total += item_total
            
            # Create item frame
            item_frame = ctk.CTkFrame(self.scrollable_frame)
            item_frame.pack(fill="x", padx=5, pady=5)
            
            # Item details
            details_frame = ctk.CTkFrame(item_frame)
            details_frame.pack(fill="x", padx=5, pady=5)
            
            name_label = ctk.CTkLabel(details_frame, text=product.name, 
                                      font=ctk.CTkFont(size=12, weight="bold"))
            name_label.pack(anchor="w", padx=5)
            
            price_label = ctk.CTkLabel(details_frame, text=f"${product.price:.2f} x {quantity} = ${item_total:.2f}")
            price_label.pack(anchor="w", padx=5)
            
            # Quantity and remove buttons
            buttons_frame = ctk.CTkFrame(item_frame)
            buttons_frame.pack(fill="x", padx=5, pady=5)
            
            # Update quantity
            ctk.CTkLabel(buttons_frame, text="Quantity:").pack(side="left", padx=5)
            quantity_var = tk.StringVar(value=str(quantity))
            quantity_entry = ctk.CTkEntry(buttons_frame, width=50, textvariable=quantity_var)
            quantity_entry.pack(side="left", padx=5)
            
            update_btn = ctk.CTkButton(
                buttons_frame, 
                text="Update", 
                width=60,
                command=lambda idx=i, qv=quantity_var: self.update_quantity(idx, qv)
            )
            update_btn.pack(side="left", padx=5)
            
            # Remove button
            remove_btn = ctk.CTkButton(
                buttons_frame, 
                text="Remove", 
                width=60,
                command=lambda idx=i: self.remove_from_cart(idx)
            )
            remove_btn.pack(side="left", padx=5)
        
        # Update total
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def update_quantity(self, index, quantity_var):
        """Update the quantity of an item in the cart"""
        try:
            new_quantity = int(quantity_var.get())
            if new_quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0")
                return
            
            product = self.cart[index]['product']
            if new_quantity > product.stock:
                messagebox.showerror("Error", f"Only {product.stock} {product.name} in stock!")
                return
            
            self.cart[index]['quantity'] = new_quantity
            self.load_cart_items()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def remove_from_cart(self, index):
        """Remove an item from the cart"""
        del self.cart[index]
        self.load_cart_items()

    def checkout(self):
        """Process the checkout"""
        if not self.cart:
            messagebox.showerror("Error", "Your cart is empty!")
            return
        
        # Check if all items have sufficient stock
        for item in self.cart:
            product = item['product']
            if item['quantity'] > product.stock:
                messagebox.showerror("Error", f"Insufficient stock for {product.name}")
                return
        
        # Calculate total
        total = sum(item['product'].price * item['quantity'] for item in self.cart)
        
        # Prepare order items
        order_items = []
        for item in self.cart:
            order_items.append({
                'product_id': item['product'].id,
                'quantity': item['quantity'],
                'price': item['product'].price
            })
        
        # Create order
        order_id = self.order_dao.create_order(self.user.id, total, order_items)
        
        if order_id:
            messagebox.showinfo("Success", f"Order #{order_id} placed successfully!")
            self.cart.clear()  # Clear the cart after successful order
            self.parent.destroy()  # Close the cart window
            if self.callback:
                self.callback()  # Call the callback function
        else:
            messagebox.showerror("Error", "Failed to place order. Please try again.")