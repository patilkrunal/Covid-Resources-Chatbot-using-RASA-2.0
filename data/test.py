
# cities = {"data":["CoVID-19 Testing Lab","Free Food","Fundraisers","Hospitals and Centers","Delivery [Vegetables, Fruits, Groceries, Medicines, etc.]","Police","Government Helpline","Other","Mental well being and Emotional Support","Accommodation and Shelter Homes","Senior Citizen Support","Transportation","Community Kitchen","Ambulance","Fire Brigade","Quarantine Facility","Helpline for Cyclone Amphan","Fever Clinic"]}
# for city in cities["data"]:
#     print("- [" + city + "](location)")


URL = "https://api.postalpincode.in/pincode/"

import requests

PINCODE = str(422101)
# response = requests.get(URL + PINCODE).json()
response = {"data":["CoVID-19 Testing Lab","Free Food","Fundraisers","Hospitals and Centers","Delivery [Vegetables, Fruits, Groceries, Medicines, etc.]","Police","Government Helpline","Other","Mental well being and Emotional Support","Accommodation and Shelter Homes","Senior Citizen Support","Transportation","Community Kitchen","Ambulance","Fire Brigade","Quarantine Facility","Helpline for Cyclone Amphan","Fever Clinic"]}

for p in response["data"]:
    print(p)