"""operation.py

Contains the main operations for the skin care product system.

Functions:
- display_products(products): Prints the list of products.
- sell_products(products): Manages the product selling flow.
- restock_products(products): Manages the product restocking flow.
- generate_invoice(customer, sold_items, total): Creates an invoice file.
"""

import datetime
import os
from write import save_products

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_FOLDER = os.path.join(BASE_DIR, "invoices")


def _section_title(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def _divider():
    print("-" * 72)


def _money(value):
    return f"Rs {value:.2f}"


def _find_product_key(products, user_input):
    query = user_input.strip().lower()
    for name in products:
        if name.lower() == query:
            return name
    return None

def display_products(products):
    _section_title("Available Products")
    if not products:
        print("No products available in inventory.")
        return
    print(f"{'Product':<20} {'Brand':<16} {'Qty':<8} {'Selling Price':<15} {'Country'}")
    _divider()
    for name, info in sorted(products.items()):
        sell_price = info["cost_price"] * 2
        print(
            f"{name:<20} {info['brand']:<16} {info['quantity']:<8} "
            f"{_money(sell_price):<15} {info['country']}"
        )

def generate_invoice(customer, sold_items, total):
    os.makedirs(INVOICE_FOLDER, exist_ok=True)
    now = datetime.datetime.now()
    safe_customer = customer.replace(" ", "_") or "UnknownCustomer"
    filename = os.path.join(INVOICE_FOLDER, f"Sale_{safe_customer}_{now.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(filename, "w") as file:
        file.write(f"Customer Name: {customer}\nDate: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write(f"{'Product':<20} {'Brand':<15} {'Qty Paid':<10} {'Qty Free':<10} {'Unit Price':<12} {'Total'}\n")
        for item in sold_items:
            file.write(f"{item['name']:<20} {item['brand']:<15} {item['paid_qty']:<10} {item['free_qty']:<10} {item['price']:<12.2f} {item['total']:.2f}\n")
        file.write(f"\nTotal Amount: Rs {total:.2f}\n")
    print(f"\nSales invoice saved as: {filename}")

def sell_products(products):
    _section_title("Purchase Products")
    customer = input("Enter customer name: ").strip()
    if not customer:
        print("Customer name cannot be empty.")
        return

    display_products(products)
    cart = []
    total = 0

    while True:
        product_name = input("\nEnter product name to buy (or type 'done' to finish): ").strip()
        if product_name.lower() == "done":
            break
        matched_product = _find_product_key(products, product_name)
        if not matched_product:
            print("Product not found.")
            continue
        try:
            qty = int(input("Enter quantity to buy: "))
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        available = products[matched_product]["quantity"]
        free = qty // 3
        total_items = qty + free
        if total_items > available:
            print(f"Not enough stock. Available: {available}")
            continue
        price = products[matched_product]["cost_price"] * 2
        item_total = price * qty
        total += item_total
        cart.append({
            "name": matched_product,
            "brand": products[matched_product]["brand"],
            "paid_qty": qty,
            "free_qty": free,
            "price": price,
            "total": item_total
        })
        products[matched_product]["quantity"] -= total_items
        print(
            f"Added to cart: {matched_product} | Paid: {qty} | Free: {free} | "
            f"Subtotal: {_money(item_total)}"
        )

    if cart:
        _section_title("Purchase Summary")
        print(f"Customer: {customer}")
        _divider()
        print(f"{'Product':<20} {'Brand':<16} {'Paid Qty':<10} {'Free Qty':<10} {'Total'}")
        _divider()
        for item in cart:
            print(
                f"{item['name']:<20} {item['brand']:<16} {item['paid_qty']:<10} "
                f"{item['free_qty']:<10} {_money(item['total'])}"
            )
        _divider()
        print(f"Grand Total: {_money(total)}")
        generate_invoice(customer, cart, total)
        save_products(products)
    else:
        print("No items purchased.")

def restock_products(products):
    _section_title("Restock Products")
    vendor = input("Enter vendor/supplier name: ").strip()
    if not vendor:
        print("Vendor name cannot be empty.")
        return

    display_products(products)
    restocked_items = []
    total = 0

    while True:
        name = input("\nEnter product name to restock (or type 'done'): ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("Product name cannot be empty.")
            continue

        existing_name = _find_product_key(products, name)
        brand = input("Enter brand name: ").strip()
        if not brand and not existing_name:
            print("Brand name cannot be empty for a new product.")
            continue
        try:
            qty = int(input("Enter quantity to add: "))
            cost = float(input("Enter cost price per item: "))
            if qty <= 0 or cost < 0:
                print("Quantity must be greater than zero and cost cannot be negative.")
                continue
        except ValueError:
            print("Invalid input.")
            continue
        country = input("Enter country of origin: ").strip()
        if not country and not existing_name:
            print("Country cannot be empty for a new product.")
            continue

        if existing_name:
            products[existing_name]["quantity"] += qty
            products[existing_name]["cost_price"] = cost  # update if changed
            if brand:
                products[existing_name]["brand"] = brand
            if country:
                products[existing_name]["country"] = country
        else:
            products[name] = {
                "brand": brand,
                "quantity": qty,
                "cost_price": cost,
                "country": country
            }

        restocked_items.append({
            "name": name,
            "brand": brand,
            "qty": qty,
            "cost": cost,
            "total": cost * qty
        })
        total += cost * qty
        print(f"Restocked {qty} units of {name} at {_money(cost)} each.")

    now = datetime.datetime.now()
    os.makedirs(INVOICE_FOLDER, exist_ok=True)
    safe_vendor = vendor.replace(" ", "_") or "UnknownVendor"
    filename = os.path.join(INVOICE_FOLDER, f"Restock_{safe_vendor}_{now.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(filename, "w") as file:
        file.write(f"Supplier: {vendor}\nDate: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write(f"{'Product':<20} {'Brand':<15} {'Qty':<5} {'Rate':<10} {'Total'}\n")
        for item in restocked_items:
            file.write(f"{item['name']:<20} {item['brand']:<15} {item['qty']:<5} {item['cost']:<10.2f} {item['total']:.2f}\n")
        file.write(f"\nTotal Restock Amount: Rs {total:.2f}\n")

    save_products(products)
    if restocked_items:
        _section_title("Restock Summary")
        print(f"Supplier: {vendor}")
        _divider()
        print(f"{'Product':<20} {'Brand':<16} {'Qty':<8} {'Cost':<14} {'Total'}")
        _divider()
        for item in restocked_items:
            print(
                f"{item['name']:<20} {item['brand']:<16} {item['qty']:<8} "
                f"{_money(item['cost']):<14} {_money(item['total'])}"
            )
        _divider()
        print(f"Total Restock Amount: {_money(total)}")
        print(f"Restock invoice saved as: {filename}")
    else:
        print("No items were restocked.")
