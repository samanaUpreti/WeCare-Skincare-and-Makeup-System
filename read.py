"""read.py

Handles loading product data from a text file.

Functions:
- load_products(): Reads product data from the 'products.txt' file.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.txt")
INVOICE_FOLDER = os.path.join(BASE_DIR, "invoices")

if not os.path.exists(INVOICE_FOLDER):
    os.makedirs(INVOICE_FOLDER)

def load_products():
    products = {}
    if not os.path.exists(PRODUCT_FILE):
        return products

    with open(PRODUCT_FILE, "r") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line:
                continue

            parts = clean_line.split(",")
            if len(parts) != 5:
                continue

            name, brand, qty, cost, country = parts
            products[name] = {
                "brand": brand,
                "quantity": int(qty),
                "cost_price": float(cost),
                "country": country
            }
    return products