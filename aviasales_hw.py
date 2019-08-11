from pprint import pprint
import requests
import json
import re
import pymorphy2

def iata_sity(sity_name):
    def get_words(requ):
        words = re.findall("[а-яА-Я]{3,}", requ)
        return words

    def get_sity(words):
        def get_country_imp(country):
#            link = f'https://htmlweb.ru/service/api.php?inflect={country}&json'
##            link = f'https://ws3.morpher.ru/russian/declension?s={country}&format=json'
#            link = f'http://pyphrasy.herokuapp.com/inflect?pharse={country}%8C&forms=gent,plur&forms=datv'
#            req = requests.get(link)
#            print(req.text)
#            data = json.loads(req.text)
#            return data['0']
##            return data['0']
            country_morph = pymorphy2.MorphAnalyzer().parse(country)[0]
            return country_morph.normal_form

        def get_capital(country):
            service = 'https://www.travelpayouts.com/widgets_suggest_params?q='
            country = get_country_imp(country).lower()
#№            print(country)
            link = f'{service}{country}'
            req = requests.get(link)
            data = json.loads(req.text)
            if 'capital' in data.keys():
                return (data['capital']['iata'])
            else:
                return ''

        sities = []
        for i in words:
            capital = get_capital(i)
            if capital:
#                sities.append(data['capital']['iata'])
                sities.append(capital)
            else:
                service = 'https://www.travelpayouts.com/widgets_suggest_params?q='
                req_str = f'Из {i} в {i}'
                link = f'{service}{req_str}'
                req = requests.get(link)
                data = json.loads(req.text)
                if 'origin' in data.keys():
                    sities.append(data['origin']['iata'])
 #           print(sities)
        return sities

    service = 'https://www.travelpayouts.com/widgets_suggest_params?q='
    link = f'{service}{sity_name}'
    req = requests.get(link)
    data = json.loads(req.text)
    if 'origin' not in data.keys():
        sities = get_words(sity_name)
        sity_req = get_sity(sities)
        return sity_req[:2]
    else:
        return [data['origin']['iata'], data['destination']['iata']]

fly_req = 'Из Кубы в Москву'

service = 'http://min-prices.aviasales.ru/calendar_preload?'
itoas = iata_sity(fly_req)
fromCity = itoas[0]
toCity = itoas[1]
#link = f'{service}origin={fromCity}&destination={toCity}&one_way=true'
link = f'{service}origin={fromCity}&destination={toCity}'
req = requests.get(link)
data = json.loads(req.text)
for i in data['best_prices']:
    print(i['value'],i['origin'],i['depart_date'],i['destination'],i['return_date'],i['gate'])