import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.txt")


def save_products(products):
    with open(PRODUCT_FILE, "w") as file:
        for name, info in products.items():
            line = f"{name},{info['brand']},{info['quantity']},{info['cost_price']},{info['country']}\n"
            file.write(line)