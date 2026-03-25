# database.py
# Implemented by Mohammad Faqrullah Bin Raba'ee
# (105058)

# Data follows the attributes: userID, password, name
USERS_DB = {
    "cashiers": {
        "C001": {"password": "pay123", "name": "John Doe"},
        "C002": {"password": "scan456", "name": "Sarah Smith"}
    },
    "admins": {
        "A001": {"password": "adminroot", "name": "Alice Johnson"},
        "A002": {"password": "supersecure", "name": "Bob Builder"}
    }
}

PRODUCTS_DB = {
    "101": {
        "name": "Coffee (Latte)",
        "price": 5.50,
        "stock": 100
    },
    "102": {
        "name": "Blueberry Muffin",
        "price": 3.50,
        "stock": 50
    },
    "103": {
        "name": "Bottled Water",
        "price": 1.50,
        "stock": 200
    },
    "104": {
        "name": "Avocado Toast",
        "price": 8.00,
        "stock": 30
    },
    "105": {
        "name": "Egg (10s)",
        "price": 8.00,
        "stock": 100
    },
    "106": {
        "name": "Tom Yum Paste",
        "price": 4.50,
        "stock": 50
    },
    "107": {
        "name": "Fish Ball (30s)",
        "price": 9.50,
        "stock": 200
    },
    "108": {
        "name": "Sesame Sauce",
        "price": 6.59,
        "stock": 100
    },
    "109": {
        "name": "Sugar (1KG)",
        "price": 6.20,
        "stock": 80
    }
}

COUPONS_DB = {
    "SAVE10": 0.10,  # 10% discount
    "OFF20": 0.20, # 20% discount
    "OFF15": 0.15, # 15% discount
}

SALES_HISTORY = {
    "TXN-1766600949": {
        "items": [
            {"name": "Coffee (Latte)", "qty": 6, "price": 5.50},
            {"name": "Blueberry Muffin", "qty": 5, "price": 3.50}
        ],
        "subtotal": 50.50,
        "discount": 0.0,
        "total": 50.50
    }
}

