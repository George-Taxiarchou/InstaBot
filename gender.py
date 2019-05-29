import json
from urllib.request import urlopen
import csv

#BE CAREFULL ONLY 200 REQUESTS PER DAY BROS

def Gender(name):
    apiKey = "5cee5a06e4b2045e555aa2f2" #Your API Key
    apiUrl = "https://genderapi.io/api/?name=" + name + "&key=" + apiKey
    result = urlopen(apiUrl).read().decode('utf-8')
    getGender = json.loads(result)
    return getGender["gender"]
