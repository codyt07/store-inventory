from models import (Base, price_cleaner_db_initializer, session, engine, Product)
from datetime import date, datetime
import time

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
                \nEnter A To Return To Main Menu
                \rEnter B To Go Back To Product ID Screen
                \rCommand: ''')
        if selection.lower() == "a":
            menu()
        elif selection.lower() == "b":
            view_summary()
        else: 
            input('''\nValid input not Entered
                    \rPress Enter to return main Menu''')
            menu()
    except AttributeError:
        input('''\n*- Invalid Product Was Entered -*
                \rPress Enter to Try again...''')
        view_summary()

def update_product(update_id):
    to_update = session.query(Product).filter(
        Product.id == update_id).first()
    updating = True
    while updating == True:
        print(f'Updating: {to_update.name}')
        command = input('''\nEnter Command From The List
                        \rEnter A To Update the Product Name
                        \rEnter B To Update Products Price
                        \rEnter C To Update Product Quantity
                        \rEnter D To Update Products Date
                        \rEnter E To Delete Product
                        \rEnter F To Cancel and Return to Main Menu
                        \rCommand: ''')
        if command.lower() == 'a':
            new_name = True
            while new_name:
                update_name = input(f'''\nCurrent Name Is: {to_update.name}
                            \rEnter A New Name: ''')
                selection = input(f'''\nConfirming New Name: {update_name}?
                                \rEnter A To Confirm
                                \rEnter B To Retype name
                                \rEnter C to Go Back To Product Modification Menu
                                \rCommand: ''')
                if selection.lower() == 'a':
                    to_update.name = update_name
                    session.commit()
                    new_name = False
                    print('''\nProduct Name Updated! 
                            \rReturning Back to Sub Menu''')
                    time.sleep(1.5)
                elif selection.lower() == 'b':
                    pass
                elif selection.lower() == 'c':
                    new_name = False

        elif command.lower() == 'b':
            new_price = True
            while new_price:
                product_price = input(f'''\nCurrent Price: {to_update.price/ 100}
                            \rPlease Enter A New Price Below
                            \r** Do Not Use a Currency Symbol **
                            \rNew Price: ''')
                update_price = price_checker(product_price)
                confirm = input(f'''\nConfirming: {update_price / 100}?
                                \rEnter A To Confirm
                                \rEnter B To Enter a New Price
                                \rEnter C to Go Back To Product Modification Menu
                                \rCommand: ''')
                if confirm.lower() == 'a':
                    to_update.price = update_price
                    session.commit()
                    new_price = False
                    print('''\n Product Price Updated!
                            \rReturning Back To Sub Menu''')
                    time.sleep(1.5)

                elif confirm.lower() == 'b':
                    pass
                elif confirm.lower() == 'c':
                    new_price = False
        
        elif command.lower() == 'c':
            pass
        elif command.lower() == 'd':
            pass
        elif command.lower() == 'e':
            pass
        elif command.lower() == 'f':
            updating = False
            print("Returning to Main Menu")
            menu()


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
    id_list = []
    print("Checking for prior entries...\n")
    checking = session.query(Product).filter(Product.name.like('%' + product_name_check + '%')).all()
    question = False
    for returns in checking:
        print(f'\r{returns.id} - {returns.name}')
        id_list.append(returns.id)
        question = True
    while question == True:
        if question == True:
            proceed= input('''\nMatching item located in database.
                        \rEnter A to Add New Item
                        \rEnter B to Update An Item
                        \rEnter Q to Go Back to Main Menu
                        \rCommand: ''')
            if proceed.lower() == "a":
                question = False
            elif proceed.lower() == "b":
                update_id = input(f'''\nProduct IDs: {id_list}
                        \rEnter Product ID To Update: ''')
                question = False
                update_product(update_id)
                
            elif proceed.lower() == 'q':
                print("\nReturning to Main Menu")
                question = False
                menu()
            else:
                input('''Valid Command Not Entered. 
                \rPress Enter to Try Again''')
    return product_name_check

def date_checker(product_date):
    time_error = True
    while time_error:
        try:
            product_date_obj = datetime.strptime(product_date, '%m-%d-%Y')
            time_error = False
            return product_date_obj
        except ValueError:
            product_date = input('''\nIncorrect date entered.
                            \rPlease Enter a new date in the Following Format
                            \rMM-DD-YYYY Example: 05-06-2018
                            \rEnter New Date: ''')

def confirmation(verified_product, price_verified, quantity_verified, date_verified):
    date = date_verified.strftime('%m-%d-%y')
    confirm = input(f'''\n*** Confirmation ***
            \rProduct Name: {verified_product.title()}
            \rPrice: {price_verified / 100}
            \rQuantity: {quantity_verified}
            \rDate: {date}
            \nEnter A to confirm
            \rEnter B to cancel and return back to the main menu
            \rCommand: ''')
    loop = True
    while loop == True:
        if confirm.lower() == "a":
            new_product = Product(name=verified_product.title(), price=price_verified, quantity=quantity_verified, updated=date_verified)
            session.add(new_product)
            session.commit()
            print(f'Product: {verified_product.title()} Added to the Database!')
            time.sleep(1.5)
            menu()
        elif confirm.lower() == 'b':
            print('\nReturn to Main Menu')
            loop = False
            menu()
        else:
            confirm = input(f'\nInvalid input \rEnter A Command:')

def add_product():
    print("\nAdd Product")
    product_name_check = input("Enter Product Name: ")
    verified_product = duplicate_checker(product_name_check)
    product_price = input("Enter Product Price Without Currency Symbol: ")
    price_verified = price_checker(product_price)
    product_quantity = input('Enter Product Quantity: ')
    quantity_verified = quantity_checker(product_quantity)
    product_date = input('Enter Date (MM-DD-YYYY) (10-27-2021): ')
    date_verified = date_checker(product_date)
    confirmation(verified_product, price_verified, quantity_verified, date_verified)

def menu():
    selection = input('''\n*** Cody's Store Inventory Manager ***
            \rPlease Select from the Menu Below
            \rEnter V to view a single product
            \rEnter A to add a product
            \rEnter B to backup the database
            \rEnter Q to Exit the Program
            \rEnter Command: ''')

    if selection.lower() == "v":
        view_summary()
    elif selection.lower() == "a":
        add_product()
    elif selection.lower() == "b":
        pass
    elif selection.lower() == 'q':
        print('Thank you for using this program!')
        exit()
    else:
        input('''\n*** A Valid Command Was Not Entered ***
                \rPress Enter To Try Again...''')
        menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()
