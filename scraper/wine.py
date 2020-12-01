#Wine class for necessary data from Rarewine dataset
class Wine:
    def __init__(self, name, price,year, lwin):
        self.name = name
        self.price = price
        self.year = year
        self.lwin = lwin

#Wine class containing the necessary infomation for the dataset consisting of extracted data from the web
class ExtractedWine:
    def __init__(self, name, original_name, lwin, original_year, year, wine_offer_price,price):
        self.name = name
        self.original_name = original_name
        self.lwin = lwin
        self.original_year = original_year
        self.year = year
        self.wine_offer_price = wine_offer_price
        self.price = price
 