# function
def get_valid_input():
    # returns integer or "quit"
    while True:
            userinput = input("Enter stock quantity (or 'quit to exit): ")
    
            if userinput.lower() == "quit":
                return "quit"
    
            if not userinput.isdigit():
                print("Invalid input. Please enter a positive whole number.")
                continue
    
            quantity = int(userinput)
    
            return quantity

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

# main program
total_units = 0

while True:
     result = get_valid_input()

     if result == "quit":
          break

     total_units = process_delivery(total_units, result)

     print(result)
     print(total_units)
