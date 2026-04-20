from read import load_products
from write import save_products
from operation import display_products, sell_products, restock_products

def add_new_product(products):
    name = input("Enter new product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    if name in products:
        print("Product already exists. Use restock option to add quantity.")
        return
    brand = input("Enter brand name: ").strip()
    if not brand:
        print("Brand name cannot be empty.")
        return
    try:
        qty = int(input("Enter quantity: "))
        cost = float(input("Enter cost price per item: "))
        if qty < 0 or cost < 0:
            print("Quantity and cost must be non-negative.")
            return
    except ValueError:
        print("Invalid input.")
        return
    country = input("Enter country of origin: ").strip()
    if not country:
        print("Country cannot be empty.")
        return

    products[name] = {
        "brand": brand,
        "quantity": qty,
        "cost_price": cost,
        "country": country
    }
    save_products(products)
    print(f"Product '{name}' added successfully.")

def main():
    products = load_products()
    while True:
        print("\n--- Skin Care Product Sale System ---")
        print("1. Display Products")
        print("2. Purchase Products")
        print("3. Restock Products")
        print("4. Add New Product")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            display_products(products)
        elif choice == "2":
            sell_products(products)
        elif choice == "3":
            restock_products(products)
        elif choice == "4":
            add_new_product(products)
        elif choice == "5":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
