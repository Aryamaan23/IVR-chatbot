from opencage.geocoder import OpenCageGeocode
from geopy.geocoders import Nominatim
import random
import sys
import math
import pandas as pd
from faker import Faker
fake = Faker()

fake.name()


key ='d908ec2a841244e0892ac9b12db8a453' # get api key from:  https://opencagedata.com
geocoder = OpenCageGeocode(key)
cities = ["kaithal", "Alahabad", "mumbai", "chennai", "delhi", "lucknow", "panipat", "hisar", "ranchi", "jaipur", "rohtak", "kolkata", "bangalore", "hyderabad", "raipur", "ghaziabad", "indore", "bhopal" ]
a = random.choice(cities)
b= "India"
x=a,b
print(x)
ab=x[0]
abc=x[1]
print(ab)
print(abc)
#df = pd.DataFrame({a,b})
#df.to_csv(index=False)
#print(df)
query =f'{ab},{abc}'
print(query)
results =geocoder.geocode(query)

#print (results)
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print(lat)
print(lng)

 
#results =geocoder.geocode(query)
geolocator = Nominatim(user_agent="IVR-CHATBOT")
location = geolocator.reverse(f"{lat},{lng}")
a=fake.address()
print(a)
days = random.randint(4, 10)
print(f"Your order is ready to dispatch from {a} "+ "and will be delivered to your address which is " +location.address + f" within {days} days")

