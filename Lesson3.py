import requests
from pymongo import MongoClient
import json

api_url = 'https://icorating.com/ico/all/load/'
CLIENT = MongoClient('localhost', 27017)
mongobase = client.new_test_base
test_collection = mongobase.new_test_collection

response = requests.get(api_url)

data = json.loads(response.text)

print(api_url)

tmp_icos = []

for iso_work in data["icos"]['data']:
    print(iso_work)
#    print(iso_work["name"])

for iso_work in data["icos"]['data']:
    tmp_icos.append(iso_work)

test_collection.insert_many(tmp_icos)

#class ico_collect:
#    icos = []

#    def __init__(self, url):

#        while True:
