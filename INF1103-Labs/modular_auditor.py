failed_attempts = 0  # tracked globally so get_valid_input() can update it
 
 
# function
def get_valid_input():
    # returns integer or "quit"
    global failed_attempts
 
    while True:
        userinput = input("Enter stock quantity (or 'quit' to exit): ")
 
        if userinput.lower() == "quit":
            return "quit"
 
        if not userinput.isdigit():
            print("Invalid input. Please enter a positive whole number.")
            failed_attempts += 1
            continue
 
        quantity = int(userinput)
 
        return quantity
 
 
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total
 
 
def calculate_tax(amount):
    tax = amount * 0.10
    return tax
 
 
def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
 
 
# main program
total_units = 0
deliveries_processed = 0
 
while True:
    result = get_valid_input()
 
    if result == "quit":
        break
 
    total_units = process_delivery(total_units, result)
 
    tax = calculate_tax(result)
 
    deliveries_processed += 1
 
    print("Delivery:", result)
    print("Tax (10%):", tax)
 
generate_report(deliveries_processed, failed_attempts)
