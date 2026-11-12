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
    def calculate_shipping_cost(self) -> float:
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
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        # Association: Product only holds a reference; it does not own the Supplier.
        self.__supplier: Supplier = supplier

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print("   ", end="")
        self.__supplier.display_information()

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }
   
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Describe how this product is fulfilled (subclasses must implement)."""
        pass

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "Product":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier)

class Inventory:

    # Aggregation: the Inventory groups existing Product objects but does not
    # create them or control their lifecycle. It stores the base type Product,
    # so it can hold PhysicalProduct and DigitalProduct alike.
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product reference from this inventory.

        The Product itself is not destroyed: it is returned so the caller can
        keep using it or add it to another Inventory. Returns None if there
        is no match."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with the given ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_id().lower() == product_id.lower():
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def to_list(self) -> list[dict]:
        """Plain-data form of the inventory, used for saving."""
        return [product.to_dict() for product in self.__products]

class PhysicalProduct(Product, CanBeShipped):

    # Single class inheritance (Product) plus one interface (CanBeShipped).
    BASE_SHIPPING = 5.00
    RATE_PER_KG = 2.50

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"   Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Flat base fee plus a per-kg rate."""
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["weight"])

class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"  Download Size: {self.__download_size} MB")
    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["download_size"])

# ---------- Orders (composition: Order owns its OrderLines) ----------

class OrderLine:
    """One product and quantity inside a single Order.

    Not meant to be created outside Order: Order.add_order_line() builds it.
    It refers to a Product (association) but does not own that Product."""

    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"   {self.__product.get_name()} | "
              f"${self.__product.get_price():.2f} x {self.__quantity} | "
              f"Subtotal: ${self.calculate_subtotal():.2f}")


class Order:
    """Creates and manages its own OrderLine objects (composition)."""

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        """A copy of the list, so callers cannot add or remove lines directly."""
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """The Order creates the OrderLine itself; none is passed in."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and so discard) the line for the given product ID."""
        for line in self.__order_lines:
            if line.get_product().get_id().lower() == product_id.lower():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("   No order lines.")
        for line in self.__order_lines:
            line.display_information()
        print(f"   Total: ${self.calculate_total():.2f}")

# Maps the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[Product]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    """Create the right Product subclass from saved data.

    `suppliers` caches Supplier objects by ID so products saved with the same
    supplier share one Supplier object after loading."""
    supplier_data = data["supplier"]
    supplier_id = supplier_data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier.from_dict(supplier_data)
    return PRODUCT_TYPES[data["type"]].from_dict(data, suppliers[supplier_id])

# ---------- File handling ----------

def load_inventory() -> Inventory:
    inventory = Inventory()
    if not os.path.exists(FILENAME):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory
 
    print("inventory.json found.")
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        suppliers: dict[str, Supplier] = {}
        for item in data:
            inventory.add_product(product_from_dict(item, suppliers))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("Could not read inventory.json. Starting with an empty inventory.")
        return Inventory()
    return inventory
 
 
def save_inventory(inventory: Inventory) -> None:
    with open(FILENAME, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    print("Inventory saved successfully to inventory.json.")

# ---------- Menu actions (user input lives here) ----------

def add_product(inventory: Inventory) -> None:
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
 
    if inventory.find_product(product_id):
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

    product: Product
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
 
def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
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
 
 
def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.remove_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(f"Removed '{product.get_name()}' from the inventory.")

def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
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
 
def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
 
    inventory = load_inventory()
 
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Save Inventory")
    print("7. Exit")
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
            remove_product(inventory)
        elif choice == "6":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()