inventory = 0
failed_entry = 0

while True:
    quantity = input("Enter stock quantity (or 'quit to exit): ")

    if quantity.lower() == "quit":
        break

    elif not quantity.isdigit():
        print("Error: Please enter a valid integer.")
        failed_entry += 1
        continue

    quantity = int(quantity)

    if quantity < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entry += 1
        continue

       
    inventory += quantity

    if inventory > 500:
        print("Alert: Inventory exceeds 500 units.")
        break


print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entry)