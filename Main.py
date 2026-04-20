from read import load_products
from write import save_products
from operation import display_products, sell_products, restock_products


def print_banner():
    print("\n" + "=" * 72)
    print(" " * 17 + "WECARE SKINCARE AND MAKEUP SYSTEM")
    print("=" * 72)
    print("Manage products, sales, restocking, and inventory records with ease.")
    print("-" * 72)


def print_menu():
    print("\nMain Menu")
    print("1. Display Products")
    print("2. Purchase Products")
    print("3. Restock Products")
    print("4. Add New Product")
    print("5. Exit")


def prompt_choice():
    return input("\nSelect an option [1-5]: ").strip()


def add_new_product(products):
    print("\n" + "-" * 72)
    print("Add New Product")
    print("-" * 72)
    name = input("Enter new product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    if name in products:
        print("Product already exists. Use the restock option to add quantity.")
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
    print(f"\n{name} was added successfully.")

def main():
    products = load_products()
    while True:
        print_banner()
        print_menu()
        choice = prompt_choice()
        if choice == "1":
            display_products(products)
        elif choice == "2":
            sell_products(products)
        elif choice == "3":
            restock_products(products)
        elif choice == "4":
            add_new_product(products)
        elif choice == "5":
            print("\nThank you for using WeCare. Goodbye.")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
