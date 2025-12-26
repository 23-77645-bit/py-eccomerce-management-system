import re


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength (at least 8 characters)"""
    return len(password) >= 8


def validate_name(name):
    """Validate name (at least 2 characters, only letters, spaces, hyphens)"""
    if len(name) < 2:
        return False
    pattern = r'^[a-zA-Z\s\-]+$'
    return re.match(pattern, name) is not None


def validate_phone(phone):
    """Validate phone number (basic validation)"""
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None


def validate_price(price):
    """Validate price (positive number)"""
    try:
        price = float(price)
        return price >= 0
    except (ValueError, TypeError):
        return False


def validate_stock(stock):
    """Validate stock quantity (non-negative integer)"""
    try:
        stock = int(stock)
        return stock >= 0
    except (ValueError, TypeError):
        return False