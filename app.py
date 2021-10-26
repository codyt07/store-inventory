from models import (Base, session, engine, Product)
from datetime import datetime

def view_summary():
    id_list = []
    for id_list_maker in session.query(Product):
        id_list.append(id_list_maker.id)
    product_selection = input(f'''\nPlease Enter the Product ID To View Product
            \rProduct IDs: {id_list}
            \rEnter ID: ''')
    try:
        view_product = session.query(Product).filter(
            Product.id == product_selection).first()
        selection = input(f'''\nProduct Information for Product ID {product_selection}
                \r* Product Name: {view_product.name}
                \r* Product Price: ${view_product.price / 100}
                \r* Product Quantity: {view_product.quantity}
                \r* Information Last Updated: {view_product.updated}
                \nEnter 1 To Return To Main Menu
                \rEnter 2 To Go Back To Product ID Screen
                \rCommand: ''')
        if selection == "1":
            menu()
        elif selection == "2":
            view_summary()
        else: 
            input('''\nValid input not Entered
                    \rPress Enter to return main Menu''')
            menu()
    except AttributeError:
        input('''\n*- Invalid Product Was Entered -*
                \rPress Enter to Try again...''')
        view_summary()

def price_checker(product_price):
    price_error = True
    while price_error:
        try:
            product_price_check = float(product_price)
        except ValueError:
            product_price = input('''\n** Invalid Price Was Entered **
                                    \rDo not use a Currency Symbol(e.g $)
                                    \rNew Entry: ''')
        else:
            price_error = False
            return int(product_price_check * 100)

def quantity_checker(product_quantity):
    quantity_error = True
    while quantity_error:
        try:
            num_check = float(product_quantity)
        except ValueError:
            product_quantity = input('''\n ** Invalid Quantity Entered **
                                    \r Please Enter A New Number for Quantity
                                    \rNew Entry: ''')
        else:
            quantity_error = False
            return float(num_check)

def duplicate_checker(product_name_check):
    print("Checking for prior entries....")
    checking = session.query(Product).filter(Product.name.like('%' + product_name_check + '%')).all()
    question = False
    for returns in checking:
        print(f'\n{returns.name}')
        question = True
    while question == True:
        if question == True:
            proceed= input('''\nMatching item located in database.
                        \rEnter A to Continue
                        \rEnter B to Exit
                        \rCommand: ''')
            if proceed.lower() == "a":
                pass
                question = False
            elif proceed.lower() == "b":
                print("\nReturning to Main Menu")
                question = False
                menu()
            else:
                input('''Valid Command Not Entered. 
                \rPress Enter to Try Again''')
                
def date_checker(product_date):
    time_error = True
    while time_error:
        try:
            product_date_obj = datetime.strptime(product_date, '%d-%m-%Y')
            time_error = False
            return product_date_obj
        except ValueError:
            product_date = input('''\nIncorrect date entered.
                            \rPlease Enter a new date in the Following Format
                            \rMM-DD-YYYY Example: 05-06-2018
                            \rEnter New Date: ''')


def add_product():
    print("\nAdd Product")
    product_name_check = input("Enter Product Name: ")
    duplicate_checker(product_name_check)
    product_price = input("Enter Product Price Without Currency Symbol: ")
    price_verified = price_checker(product_price)
    print(price_verified)
    product_quantity = input('Enter Product Quantity: ')
    quantity_verified = quantity_checker(product_quantity)
    print(quantity_verified)
    product_date = input('Enter Date (MM-DD-YYYY) (2018-01-15): ')
    date_checker(product_date)
    print("** Adding product to Database! **")  

def menu():
    selection = input('''\n*** Cody's Store Inventory Manager ***
            \rPlease Select from the Menu Below
            \rEnter V to view a single product
            \rEnter A to add a product
            \rEnter B to backup the database
            \rEnter N to view all products summary
            \rEnter Command: ''')

    if selection.lower() == "v":
        view_summary()
    elif selection.lower() == "a":
        add_product()
    elif selection.upper() == "B":
        pass
    else:
        input('''\n*** A Valid Command Was Not Entered ***
                \rPress Enter To Try Again...''')
        menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()


# def price_cleaner_db_initializer(row):
#     price_to_clean = row[1]
#     without_sign = price_to_clean.replace("$", "")
#     try:
#         without_sign_float = float(without_sign)
#     except ValueError:
#         input('''\n ** An invalid number was entered **'
#                 \rPlease Enter a valid number with or without the currency symbol
#                 \rExample: 10.99
#                 \rPress Enter To Try Again/Continue...
#                 \r''')
#     else:
#         return int(without_sign_float * 100)
