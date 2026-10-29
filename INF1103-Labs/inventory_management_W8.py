

class Product:
    def __init__(self,productid,name,price,stock):
        self.__productid = productid
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self):
        return self.__productid

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self,quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
    