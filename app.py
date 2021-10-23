import models

def view_summary():
    id_list = []
    for id_list_maker in models.session.query(models.Product):
        id_list.append(id_list_maker.id)
    product_selection = input(f'''\nPlease Enter the Product ID To View Product
            \rProduct IDs: {id_list}
            \rEnter ID: ''')
    try:
        view_product = models.session.query(models.Product).filter(
            models.Product.id == product_selection).first()
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

def add_product():
    pass

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

    elif selection.upper() == "A":
        pass
    elif selection.upper() == "B":
        pass
    else:
        input('''\n*** A Valid Command Was Not Entered ***
                \rPress Enter To Try Again...''')
        menu()


if __name__ == '__main__':
    models.Base.metadata.create_all(models.engine)
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
