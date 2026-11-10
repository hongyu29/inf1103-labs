import json
import os
from abc import ABC, abstractmethod

DATA_DIR = os.environ.get("DATA_DIR", ".")
FILENAME = os.path.join(DATA_DIR, "inventory.json")

# ---------- Interface ----------
 
class CanBeShipped(ABC):
    """Interface-style contract: anything that can be shipped must be able
    to calculate its shipping cost."""
 
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        pass

# ---------- Supplier (association with Product) ----------

class Supplier:
    """Who supplies a product. Created independently of any Product."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])


class Product(ABC):
    def __init__(self, productid: str, name: str, price: float, stock: int,
                 supplier: Supplier):
        self.__product_id = productid
        self.__name = name
        self.__price = price
        self.__stock = stock
        # Association: Product only holds a reference; it does not own the Supplier.
        self.__supplier: Supplier = supplier

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self,quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print("   ", end="")
        self.__supplier.display_information()

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }
   
    @abstractmethod
    def get_fulfilment_info(self):
        """Describe how this product is fulfilled (subclasses must implement)."""
        pass

    @classmethod
    def from_dict(cls, data, supplier: Supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier)

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

    def to_list(self):
        """Plain-data form of the inventory, used for saving."""
        return [product.to_dict() for product in self.__products]

class PhysicalProduct(Product, CanBeShipped):

    # Single class inheritance (Product) plus one interface (CanBeShipped).
    BASE_SHIPPING = 5.00
    RATE_PER_KG = 2.50

    def __init__(self, productid: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(productid, name, price, stock, supplier)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"   Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Flat base fee plus a per-kg rate."""
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data, supplier: Supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["weight"])

class DigitalProduct(Product):

    def __init__(self, productid: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(productid, name, price, stock, supplier)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"  Download Size: {self.__download_size} MB")
    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data, supplier: Supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["download_size"])

# Maps the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data, suppliers: dict):
    """Create the right Product subclass from saved data.

    `suppliers` caches Supplier objects by ID so products saved with the same
    supplier share one Supplier object after loading."""
    supplier_data = data["supplier"]
    supplier_id = supplier_data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier.from_dict(supplier_data)
    return PRODUCT_TYPES[data["type"]].from_dict(data, suppliers[supplier_id])

# ---------- File handling ----------

def load_inventory():
    inventory = Inventory()
    if not os.path.exists(FILENAME):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory
 
    print("inventory.json found.")
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        suppliers = {}
        for item in data:
            inventory.add_product(product_from_dict(item, suppliers))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("Could not read inventory.json. Starting with an empty inventory.")
        return Inventory()
    return inventory
 
 
def save_inventory(inventory):
    with open(FILENAME, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    print("Inventory saved successfully to inventory.json.")

# ---------- Menu actions (user input lives here) ----------

def add_product(inventory):
    print("\nAdd New Product")
    print("Product type:")
    print("1. Physical")
    print("2. Digital")
    type_choice = input("Choose type (1/2): ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return
 
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
 
    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return
 
    name = input("Product Name: ").strip()

    print("Supplier details:")
    supplier_id = input("Supplier ID: ").strip()
    supplier_name = input("Supplier Name: ").strip()
    supplier_email = input("Supplier Contact Email: ").strip()
    if not (supplier_id and supplier_name and supplier_email):
        print("All supplier details are required.")
        return
    # The Supplier is created independently, then handed to the Product.
    supplier = Supplier(supplier_id, supplier_name, supplier_email)

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            size = float(input("Download size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, supplier, size)
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
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("-" * 48)
    if isinstance(product, CanBeShipped):
        print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")
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