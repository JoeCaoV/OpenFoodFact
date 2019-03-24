#!/usr/bin/env python3
# coding: utf-8
"""import the classes required and CONSTANTS var"""
from classes.display import Display
from classes.database import Database
from classes.api import Api
from config import CATEGORIES
#!/usr/bin/env python3
# coding: utf-8
class Main():
    """This class run the whole programm"""

    def __init__(self):
        """Start the programm by rendered the "home" menu
        1 to check the changeable products
        2 to check the saved alternative products
        """
        display = Display()
        next = False
        while not next:
            next = True
            choice = display.display_input()
            if choice == "1":
                self.select_category(display)
            elif choice == "2":
                self.select_saved_categories(display)
            else:
                print('Incorrect choice, please try again.')
                next = False

    def select_category(self, display):
        """if user choose 1 at the "home" menu
        display categories of changeable products and
        ask for a choice
        """
        display.display_categories()
        #Input phase to choose next step
        next = False
        while not next:
            next = True
            choice = display.display_input()
            if choice == "home":
                self.__init__()
            try:
                if int(choice) - 1 in range(len(CATEGORIES)):
                    self.select_product(display, CATEGORIES[int(choice) - 1])
            except ValueError:
                print('Incorrect choice, please try again.')
                next = False

    def select_product(self, display, category):
        """Once the user choose a caterogy for changeable products
        display 15 products of it and ask for a choice
        """
        api = Api()
        database = Database()
        products = database.get_products(category[0])
        #if there is no products saved yet, ask to the API then save them
        if not products:
            products = api.get_products(category[1])
            for product in products:
                data = (product['product_name'], product['id'], product['url'],
                        product['nutriments']['nutrition-score-fr'], category[0])
                database.insert_product(data)

        products = database.get_products(category[0])
        display.display_products(products)
        next = False
        #Input phase to choose next step
        while not next:
            next = True
            choice = display.display_input()
            if choice == "home":
                self.__init__()
            try:
                if int(choice) - 1 in range(len(products)):
                    self.select_alternative(display, products[int(choice) - 1], api, database)
            except:
                print('Incorrect choice, please try again')
                next = False

    def select_alternative(self, display, product, api, database):
        """Display the alternative food for the chosen product
        if user chose so, save it then back to "home" menu
        if no alternative food thanks, return to "home" menu
        """
        alternative = api.get_alternative(product[2])
        if alternative:
            display.display_alternative(product, alternative)
            choice = display.display_input()
            if choice == "home":
                self.__init__()
            elif choice == "1":
                data = (alternative['product_name'], alternative['id'], alternative['url'],
                        alternative['nutriments']['nutrition-score-fr'], product[0])
                database.insert_alternative(data)
                self.__init__()
        else:
            print("Désolé, aucun produit de substition trouvé pour cet article"
                  "retour à l'accueil")
            self.__init__()

    def select_saved_categories(self, display):
        """Display the categories of the saved product if there is some
        user must choose a category
        """
        database = Database()
        categories = database.get_saved_categories()
        if categories:
            display.display_saved_categories(categories)
            #Input phase to choose next step
            next = False
            while not next:
                next = True
                choice = display.display_input()
                if choice == "home":
                    self.__init__()
                try:
                    if int(choice) - 1 in range(len(categories)):
                        self.select_saved_products(display, categories[int(choice) - 1], database)
                except ValueError:
                    print('Incorrect choice, please try again')
                    next = False
        else:
            print("Désolé vous n'avez pas encore enregistré de produit alternatif")
            print("Retour au menu de départ")
            self.__init__()

    def select_saved_products(self, display, category, database):
        """Display the product with a registred alternative"""
        products = database.get_saved_products(category[0])
        display.display_saved_products(products)
        #Input phase to choose next step
        next = False
        while not next:
            next = True
            choice = display.display_input()
            if choice == "home":
                self.__init__()
            try:
                if int(choice) - 1 in range(len(products)):
                    self.select_saved_alternative(display, products[int(choice) - 1], database)
            except ValueError:
                print('Incorrect choice, please try again')
                next = False

    def select_saved_alternative(self, display, product, database):
        """display the alternative product and compare him
        to the original product
        """
        alternative = database.get_saved_alternative(product)
        display.display_saved_alternative(product, alternative)
        #Input phase to choose next step
        next = False
        while not next:
            choice = input("Tapez 'Home' pour revenir à l'écran d'accueil")
            if choice == "home":
                next = True
                self.__init__()
            else:
                print('Choix incorrect, veuillez réessayer.')


if __name__ == "__main__":
    MAIN = Main()
