import requests
from pymongo import MongoClient

api_url = 'https://icorating.com/ico/all/load/'
CLIENT = MongoClient('localhost', 27017)
mongobase = client.new_test_base
test_collection = mongobase.new_test_collection

class ico_collect:
    icos = []

    def __init__(self, url):

        while True:
            