import requests
import json

headers = {
    "X-Token": "4279874232",
}

global_prices = [
    {
        "lwin_fk": 123,
        "price": 12.0,
        "date": None
    },
    {
        "lwin_fk": 456,
        "price": 15.0,
        "date": None
    },
    {
        "lwin_fk": 789,
        "price": 18.0,
        "date": None
    }
]

time_interval = {
  "TimeInterval": {
    "Time": "2018-12-18T13:37:13.2951437Z",
    "model_type": "svm"
  }
}

offers = {"WineDeals":[
  {
    "offer": {
      "id": "1",
      "supplierName": "Supplier Navn1",
      "supplierEmail": "supplier_dummy@rarewine.dk",
      "supplierId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    "linkedWine": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "linkedWineLwin": 123,
    "originalOfferText": "2 Vin 3 stk ",
    "producer": "Producer",
    "wineName": "Vin Navn",
    "quantity": 3,
    "year": 2003,
    "price": 2000,
    "currency": "€",
    "isOWC": False,
    "isOC": False,
    "isIB": False,
    "bottlesPerCase": 1,
    "bottleSize": "standard",
    "bottleSizeNumerical": 750,
    "note": None,
    "region": "Bordeaux",
    "subRegion": "Saint Emilion",
    "colour": "Red",
    "type": "Still",
    "id": "786234129",
    "createdAt": "2019-12-18T13:37:13.2951437Z"
  },
  {
    "offer": {
      "id": "2",
      "supplierName": "Supplier Navn2",
      "supplierEmail": "supplier_dummy@rarewine.dk",
      "supplierId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    "linkedWine": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "linkedWineLwin": 456,
    "originalOfferText": "2 Vin 3 stk ",
    "producer": "Producer",
    "wineName": "Vin Navn",
    "quantity": 3,
    "year": 2003,
    "price": 2000,
    "currency": "€",
    "isOWC": False,
    "isOC": False,
    "isIB": False,
    "bottlesPerCase": 1,
    "bottleSize": "standard",
    "bottleSizeNumerical": 750,
    "note": None,
    "region": "Bordeaux",
    "subRegion": "Saint Emilion",
    "colour": "Red",
    "type": "Still",
    "id": "092841092",
    "createdAt": "2019-12-18T13:37:13.2951437Z"
  },
  {
    "offer": {
      "id": "3",
      "supplierName": "Supplier Navn3",
      "supplierEmail": "supplier_dummy@rarewine.dk",
      "supplierId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    "linkedWine": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "linkedWineLwin": 789,
    "originalOfferText": "2 Vin 3 stk ",
    "producer": "Producer",
    "wineName": "Vin Navn",
    "quantity": 3,
    "year": 2003,
    "price": 2000,
    "currency": "€",
    "isOWC": False,
    "isOC": False,
    "isIB": False,
    "bottlesPerCase": 1,
    "bottleSize": "standard",
    "bottleSizeNumerical": 750,
    "note": None,
    "region": "Bordeaux",
    "subRegion": "Saint Emilion",
    "colour": "Red",
    "type": "Still",
    "id": "48927940",
    "createdAt": "2019-12-18T13:37:13.2951437Z"
  },
  {
    "offer": {
      "id": "4",
      "supplierName": "Supplier Navn4",
      "supplierEmail": "supplier_dummy@rarewine.dk",
      "supplierId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    "linkedWine": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "linkedWineLwin": 592,
    "originalOfferText": "2 Vin 3 stk ",
    "producer": "Producer",
    "wineName": "Vin Navn",
    "quantity": 3,
    "year": 2003,
    "price": 2000,
    "currency": "€",
    "isOWC": False,
    "isOC": False,
    "isIB": False,
    "bottlesPerCase": 1,
    "bottleSize": "standard",
    "bottleSizeNumerical": 750,
    "note": None,
    "region": "Bordeaux",
    "subRegion": "Saint Emilion",
    "colour": "Red",
    "type": "Still",
    "id": "6583",
    "createdAt": "2019-12-18T13:37:13.2951437Z"
  }
],
"model_type":"svm"
}

transactions = '''Vendor Id,Posting Group,No_,LWIN No_,Description,Unit of Measure,Quantity,Direct Unit Cost,Amount,Variant Code,Posting Date,Purchase Initials,id
701,VIN,107979,1082555,Some vendor 1,750ml,1,3700,3700,1,2019-01-02 00.00.00.000,XX,786234129
701,VIN,107979,1082555,Some vendor 2,750ml,15,3700,55500,2,2019-01-02 00.00.00.000,XX,48927940
575,SPIRITUS,106465,1398548,Some other vendor,750ml,1,48820,48820,3,2019-01-07 00.00.00.000,YY,6583'''

def test_get_recommendation():
  response = requests.get('http://127.0.0.1:49500/recommendation', headers = {"X-Token": "23984728947"})
  assert int(response.status_code) == 200
  print(response.text)

def test_get_wine():
  response = requests.get('http://127.0.0.1:49500/wine/6583', headers = {"X-Token": "23984728947"})
  assert int(response.status_code) == 200
  print(response.text)