class User:
    def __init__(self, user_id=None, name=None, email=None, password=None, role=None, created_at=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password  # This should be hashed
        self.role = role  # 'admin' or 'customer'
        self.created_at = created_at

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }