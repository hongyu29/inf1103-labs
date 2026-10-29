

class Product:
    def __init__(self,productid,name,price,stock):
        self.__productid = productid
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self):
        return self.__productid

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self,quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}")


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if the ID already exists."""
        if self.search_product(product.get_id()) is not None:
            return False
        self.__products.append(product)
        return True
 
    def search_product(self, product_id):
        """Return the Product with the given ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_id().lower() == product_id.lower():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

# ---------- Menu actions (user input lives here) ----------
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
 
    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return
 
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        product = Product(product_id, name, price, stock)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
 
    inventory.add_product(product)
    print("Product added successfully!")
 
 
def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
 
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        new_stock = int(input("New Stock Quantity: "))
        product.update_stock(new_stock)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    print("Stock updated successfully!")
 
 
def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
 
    print("Product Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
 
    inventory = load_inventory()
 
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")
 
    while True:
        choice = input("\nEnter option: ").strip()
 
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()


    