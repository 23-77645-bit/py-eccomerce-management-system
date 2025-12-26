# E-Commerce Management System

A desktop-based E-Commerce Management System using Python with GUI that allows:

- Admins to manage products, categories, users, and reports
- Customers to browse products, manage cart, and place orders
- Sales tracking & analytics for business insights

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| GUI | CustomTkinter (modern) / Tkinter |
| Database | MySQL |
| Security | bcrypt (password hashing) |
| Charts | Matplotlib |
| Reports | PDF / Excel |
| Architecture | MVC / DAO Pattern |

## 👥 User Roles

### 🔐 Admin
- Manage users (Admin / Customer)
- Add, update, delete products
- Manage categories
- View all orders
- View sales analytics & reports

### 🛒 Customer
- Register & login
- Browse products by category
- Search products
- Add to cart
- Checkout & place orders
- View order history

## 📦 Core Modules & Features

### 1️⃣ Authentication Module
- Secure login & registration
- bcrypt password hashing
- Role-based access control

### 2️⃣ Product & Category Management
- Add / edit / delete products
- Stock quantity tracking
- Product image support
- Category filtering

### 3️⃣ Shopping Cart Module
- Add/remove products
- Update quantity
- Auto price calculation

### 4️⃣ Order Management
- Order placement
- Order status (Pending, Paid, Shipped)
- Order history

### 5️⃣ Payment (Simulation)
- Cash on Delivery / Dummy payment
- No real gateway (school-safe)

### 6️⃣ Sales Analytics Dashboard
- Daily / monthly sales
- Best-selling products
- Revenue summary
- Charts using Matplotlib

## 🗄 Database Design (Core Tables)

- **users**: id, name, email, password, role, created_at
- **categories**: id, name, description
- **products**: id, category_id, name, description, price, stock, image, created_at
- **orders**: id, user_id, total_amount, status, order_date
- **order_items**: id, order_id, product_id, quantity, price

## 🖥 GUI Screens

- Login / Register Window
- Admin Dashboard
- Product Management Screen
- Category Management Screen
- Product Listing Screen
- Cart Window
- Checkout Window
- Order History Screen
- Sales Analytics Dashboard

## 📁 Project Structure

```
ecommerce_system/
│
├── main.py
├── config.py
│
├── db/
│   └── db_connection.py
│
├── dao/
│   ├── user_dao.py
│   ├── product_dao.py
│   ├── order_dao.py
│   └── category_dao.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   └── order.py
│
├── gui/
│   ├── login.py
│   ├── admin_dashboard.py
│   ├── customer_dashboard.py
│   ├── cart.py
│   └── analytics.py
│
├── utils/
│   ├── security.py
│   └── validators.py
│
└── assets/
    └── images/
```

## 🚀 How to Run

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your MySQL database in `config.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'ecommerce_db',
       'charset': 'utf8mb4'
   }
   ```

3. Make sure your MySQL server is running.

4. Run the application:
   ```
   python main.py
   ```

## 📈 Advanced Features (Optional – High Grades)

- ✅ Product image upload
- ✅ Export sales report (PDF / Excel)
- ✅ Search & filter products
- ✅ Order invoice generation
- ✅ Low-stock alerts
- ✅ Activity logs

## 🎓 Why This Project Scores High

- Real-world business logic
- Strong database relationships
- Secure authentication
- Clean architecture
- Analytics & reporting
- Scalable design