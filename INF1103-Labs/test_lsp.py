"""Lab 8 - Section 6: Liskov Substitution Principle tests."""
from inventory_management_W10 import (Inventory, Product, Supplier,
                              PhysicalProduct, DigitalProduct)


# 6.2 A function written only against the Product abstraction
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


# Behaviour every Product is expected to support, checked via Product only
def restock_and_report(product: Product, new_quantity: int) -> None:
    product.update_stock(new_quantity)
    assert product.get_stock() == new_quantity
    print(f"{product.get_name()}: stock is now {product.get_stock()}")


supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.1)
ebook = DigitalProduct("D001", "Python eBook", 25.00, 100, supplier, 15.5)

print("=== show_product_details with both subclasses ===")
show_product_details(laptop)
show_product_details(ebook)

print("\n=== Both types in one Inventory, normal operations ===")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(ebook)
inventory.display_all()

found = inventory.find_product("D001")
print("find_product('D001') ->", found.get_name() if found else None)

print("\n=== update_stock behaves the same for both (parent's expectation) ===")
for item in (laptop, ebook):
    restock_and_report(item, 42)

removed = inventory.remove_product("P001")
print("\nremove_product('P001') ->", removed.get_name() if removed else None)

# 6.3 Diagnose: the teammate's DigitalProduct breaks LSP
print("\n=== Diagnose: a subclass that rejects update_stock ===")


class BadDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


bad = BadDigitalProduct("D002", "Bad eBook", 10.00, 5, supplier, 1.0)
try:
    restock_and_report(bad, 42)   # code written for ANY Product
except NotImplementedError as e:
    print("LSP broken - calling code written for Product failed:", e)