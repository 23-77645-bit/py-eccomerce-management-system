import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO


class AnalyticsDashboard:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.order_dao = OrderDAO()
        self.product_dao = ProductDAO()
        
        # Configure parent window
        self.parent.title(f"Analytics Dashboard - {user.name}")
        self.parent.geometry("1000x700")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Create navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame)
        self.nav_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        # Navigation buttons
        self.sales_btn = ctk.CTkButton(self.nav_frame, text="Sales Overview", command=self.show_sales)
        self.sales_btn.pack(side="left", padx=5)
        
        self.products_btn = ctk.CTkButton(self.nav_frame, text="Top Products", command=self.show_top_products)
        self.products_btn.pack(side="left", padx=5)
        
        self.back_btn = ctk.CTkButton(self.nav_frame, text="Back to Admin", command=self.go_back)
        self.back_btn.pack(side="right", padx=5)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show initial view (sales overview)
        self.show_sales()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_sales(self):
        """Show the sales overview with charts"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Sales Analytics", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Create a frame for the charts
        charts_frame = ctk.CTkFrame(self.content_frame)
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get sales data
        sales_data = self.order_dao.get_sales_report()
        
        if not sales_data:
            no_data_label = ctk.CTkLabel(charts_frame, text="No sales data available", 
                                         font=ctk.CTkFont(size=14))
            no_data_label.pack(pady=50)
            return
        
        # Prepare data for plotting
        dates = [row[0] for row in sales_data]
        orders_count = [row[1] for row in sales_data]
        revenue = [float(row[2]) for row in sales_data]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot orders count
        ax1.plot(dates, orders_count, marker='o', color='blue', label='Orders Count')
        ax1.set_title('Daily Orders Count')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Number of Orders')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot revenue
        ax2.plot(dates, revenue, marker='s', color='green', label='Revenue')
        ax2.set_title('Daily Revenue')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Revenue ($)')
        ax2.grid(True)
        ax2.tick_params(axis='x', rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed the plot in the tkinter frame
        canvas = FigureCanvasTkAgg(fig, charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Summary statistics
        summary_frame = ctk.CTkFrame(self.content_frame)
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        total_orders = sum(orders_count)
        total_revenue = sum(revenue)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        ctk.CTkLabel(summary_frame, text=f"Total Orders: {total_orders}", 
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)
        ctk.CTkLabel(summary_frame, text=f"Total Revenue: ${total_revenue:.2f}", 
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)
        ctk.CTkLabel(summary_frame, text=f"Avg. Order Value: ${avg_order_value:.2f}", 
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)

    def show_top_products(self):
        """Show the top selling products chart"""
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="Top Selling Products", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Create a frame for the chart
        chart_frame = ctk.CTkFrame(self.content_frame)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get top selling products data
        top_products = self.order_dao.get_top_selling_products()
        
        if not top_products:
            no_data_label = ctk.CTkLabel(chart_frame, text="No product data available", 
                                         font=ctk.CTkFont(size=14))
            no_data_label.pack(pady=50)
            return
        
        # Prepare data for plotting
        product_names = [row[0] for row in top_products]
        quantities_sold = [row[1] for row in top_products]
        
        # Create figure for bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create horizontal bar chart
        bars = ax.barh(product_names, quantities_sold, color='orange')
        ax.set_title('Top Selling Products')
        ax.set_xlabel('Quantity Sold')
        ax.set_ylabel('Product Name')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, quantities_sold):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{value}', 
                    ha='left', va='center', fontweight='bold')
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed the plot in the tkinter frame
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def go_back(self):
        """Go back to admin dashboard"""
        # Import here to avoid circular imports
        from gui.admin_dashboard import AdminDashboard
        self.main_frame.destroy()
        AdminDashboard(self.parent, self.user)