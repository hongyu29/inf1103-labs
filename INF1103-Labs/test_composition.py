"""Lab 8 - Section 4.3: test the Order <-> OrderLine composition."""
from inventory_management_W10 import Supplier, PhysicalProduct, DigitalProduct, Order

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.1)
ebook = DigitalProduct("D001", "Python eBook", 25.00, 100, supplier, 15.5)

# Order 1: two products, created through add_order_line()
order1 = Order("O001")
order1.add_order_line(laptop, 1)
order1.add_order_line(ebook, 3)
order1.display_information()
print("Expected total: 1275.00")

# Order 2: the SAME laptop product
order2 = Order("O002")
order2.add_order_line(laptop, 2)
print()
order2.display_information()

# Predict first: how many OrderLine objects and Product objects?
line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("\nSame Product object in both lines:", line1.get_product() is line2.get_product())
print("Same OrderLine object in both orders:", line1 is line2)
print("id(line1) =", id(line1), "| id(line2) =", id(line2))
print("id(product in line1) =", id(line1.get_product()),
      "| id(product in line2) =", id(line2.get_product()))

# Remove a line through the Order (the line is discarded with it)
order1.remove_order_line("D001")
print("\nAfter removing the eBook line from order 1:")
order1.display_information()
print("The eBook product itself still exists:", ebook.get_name())