"""Lab 8 - Section 7.2: polymorphism through the Product abstraction."""
from inventory_management_W10 import (Inventory, Product, Supplier,
                              PhysicalProduct, DigitalProduct)

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

inventory = Inventory()
inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.1))
inventory.add_product(DigitalProduct("D001", "Python eBook", 25.00, 100, supplier, 15.5))
inventory.add_product(PhysicalProduct("P002", "Mouse", 20.00, 50, supplier, 0.2))

# One loop, one type (Product). No isinstance(), no separate physical/digital loops.
print("=== Polymorphic loop over Product references ===")
product: Product
for product in inventory.get_products():
    print(f"[{type(product).__name__}]")
    product.display_information()
    print(product.get_fulfilment_info())
    print()