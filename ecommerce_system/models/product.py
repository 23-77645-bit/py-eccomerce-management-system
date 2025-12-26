class Product:
    def __init__(self, product_id=None, category_id=None, name=None, description=None, 
                 price=None, stock=None, image=None, created_at=None):
        self.id = product_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.created_at = created_at

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})"

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image': self.image,
            'created_at': self.created_at
        }