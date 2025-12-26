class Order:
    def __init__(self, order_id=None, user_id=None, total_amount=None, status=None, order_date=None):
        self.id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status  # 'pending', 'paid', 'shipped', 'delivered'
        self.order_date = order_date

    def __str__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount}, status='{self.status}')"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'order_date': self.order_date
        }


class OrderItem:
    def __init__(self, item_id=None, order_id=None, product_id=None, quantity=None, price=None):
        self.id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})"

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }