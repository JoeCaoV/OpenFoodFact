# coding: utf-8
"""Module requests required to use the API"""
import requests

class Api:
    """contain the methods to request the API"""
    @staticmethod
    def get_products(category):
        """return the name of the first 15 products from the given category
        obtained from the API
        """
        url = "https://fr.openfoodfacts.org/category/" + category + ".json"
        request = requests.get(url)
        json = request.json()
        products = []
        ite = 0
        quant = 15
        while ite < quant:
            try:
                #checking if the product has a nutriscore
                if json["products"][ite]['nutriments']['nutrition-score-fr']:
                    products.append(json["products"][ite])
            except KeyError:
                quant += 1
            ite += 1
        return products

    @staticmethod
    def get_alternative(product_code):
        """get a alternative product with a better nutri_score
        reuse EVERY category of the original products to find
        a similar product then check if the nutriscore is better
        """
        url_prod = "https://fr.openfoodfacts.org/api/v0/produit/" + str(product_code) + ".json"
        request = requests.get(url_prod)
        product = request.json()["product"]
        url = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms=" +\
              "" + product["categories"] + "&sort_by=unique_scans_n&page_size=40&json=1"
        request = requests.get(url)
        json = request.json()
        for i in range(len(json['products'])):
            try:
                alt_score = int(json['products'][i]['nutriments']['nutrition-score-fr'])
                prod_score = int(product['nutriments']['nutrition-score-fr'])
                if alt_score < prod_score:
                    return json['products'][i]
            except KeyError:
                pass
        return False
