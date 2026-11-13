"""Lab 8 - Section 3.2: test the Inventory <-> Product aggregation."""
from inventory_management_W10 import Inventory, Supplier, PhysicalProduct

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

# 1. Create a Product BEFORE any Inventory exists
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.1)
print("Product exists before any inventory:", laptop.get_name())

# 2. Add it to Inventory A
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(laptop)
print("\nInventory A after add:")
inventory_a.display_all()

# 3. Remove it from Inventory A - the Product must still be usable
removed = inventory_a.remove_product("P001")
print("\nInventory A after remove:")
inventory_a.display_all()
print("find_product('P001') in A ->", inventory_a.find_product("P001"))
print("Removed product is the same object:", removed is laptop)
print("Product still works:")
laptop.update_stock(8)
laptop.display_information()

# 4. Add the SAME Product object to Inventory B
inventory_b.add_product(laptop)
print("\nInventory B after transfer:")
inventory_b.display_all()
print("Same object in B:", inventory_b.find_product("P001") is laptop)

# 5. Empty an inventory - products are not destroyed
inventory_b.remove_product("P001")
print("\nInventory B emptied, product still alive:", laptop.get_name(),
      "| stock", laptop.get_stock())