"""Lab 8 - Section 2.2: test the Supplier <-> Product association."""
from inventory_management_W10 import Supplier, PhysicalProduct, DigitalProduct
 
# 1. Create a Supplier on its own
supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
 
# 2. Create a PhysicalProduct and a DigitalProduct using that Supplier
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.1)
ebook = DigitalProduct("D001", "Python eBook", 25.00, 100, supplier, 15.5)
 
# 3. Display supplier information through each Product
print("--- Supplier info via each product ---")
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()
 
# 4. Separate objects: both products refer to the SAME Supplier object
print("\nSame Supplier object?", laptop.get_supplier() is ebook.get_supplier() is supplier)
 
# Predict first: what happens after `del supplier`?
del supplier
print("\n--- After `del supplier` ---")
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()
print("Products still work:")
laptop.display_information()
ebook.display_information()