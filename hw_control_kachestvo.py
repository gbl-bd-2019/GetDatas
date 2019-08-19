from bs4 import BeautifulSoup as bs
import requests
import json
import datetime

from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['control_kachestvo']
ckdb = db.control_kachestvo

# =======================================================
# =========== ЧАСТЬ ПЕРВАЯ: РОСКОНТРОЛЬ =================
# =======================================================

def rc_get_cat_urls():
    html = requests.get('https://roscontrol.com/category/produkti/').text
    parsed_html = bs(html, 'html.parser')
    categories = parsed_html.findAll(class_="testlab-category")
    categories = categories[0].findAll(class_="catalog__category-item util-hover-shadow")
    cat_urls = []
    for i in categories:
        cat_urls.append('https://roscontrol.com'+i["href"])
    return cat_urls

def rc_get_subcat_urls(cat_urls):
    subcat_urls = []
    for i in cat_urls:
        html = requests.get(i).text
        parsed_html = bs(html, 'html.parser')
        categories = parsed_html.findAll(class_="testlab-category")
        if categories:
            categories = categories[0].findAll(class_="catalog__category-item util-hover-shadow")
            for j in categories:
                subcat_urls.append('https://roscontrol.com'+j["href"])
        else:
            subcat_urls.append(i)
    return subcat_urls

def rc_get_prod_pages(subcat_url):
    pages = []
    html = requests.get(subcat_url).text
    parsed_html = bs(html, 'html.parser')
    categories = parsed_html.findAll(class_="AJAX_root")
    categories = categories[0].findChild().findNextSibling().findAll('a')
    for i in categories[1:-1]:
        pages.append('https://roscontrol.com'+i['href'])
    return pages

def rc_get_prod_data(subcat_urls):
    prod_data = []
    for sc in subcat_urls:
        pages = [sc] + rc_get_prod_pages(sc)
        print(sc)

        for pg in pages:
            html = requests.get(pg).text
            parsed_html = bs(html, 'html.parser')
            categories = parsed_html.findAll(class_="AJAX_root")
            categories = categories[0].findChild().findChild().findChild()
            if categories.getText() == 'В данном разделе пока нет товаров':
                categories = None
            while categories:
                url_mod = categories.findChild()
                name_rate_mod = url_mod.findChild().findChild().findNextSibling().findChild().findChild()
                rate = name_rate_mod.findChild().getText()
                if not rate:
                    rate = name_rate_mod.findChild().findNextSibling().getText()
                    if rate:
                        rate = '0'
                if rate == '?':
                    rate = -1
                else:
                    rate = int(rate)
                pd_item = {
                    'name': name_rate_mod.findNextSibling().findChild().getText(),
                    'rate': rate,
                    'url':  'https://roscontrol.com'+url_mod['href']
                }
                prod_data.append(pd_item)
                categories = categories.findNextSibling();
    return prod_data

# =======================================================
# =========== ЧАСТЬ ВТОРАЯ: РОСКОНТРОЛЬ =================
# =======================================================

def rk_get_json_products():
    data = requests.get('https://rskrf.ru/api/getproducts').text
# что-то ошибка возникает... Из текста ошибки ощущение, что проблема с кодировкой, но толком понять не смог...
    # with open('roskachestvo_products.txt', 'w') as f:
    #     f.write(data)

    # with open("roskachestvo_products.txt", "r") as file:
    #     data = file.read()

    data = json.loads(data)
    return data


def rk_get_product_categories():
    data = requests.get('https://rskrf.ru/api/getcategories').text

    categs = json.loads(data)
    prod_nom = ['8', '28']
    cat_pp = []
    for pn in prod_nom:
        prods = categs['categories'][pn]
        prod_pit = prods['categories']
        for i in prod_pit:
            cat_pp.append(i)
            sub = prod_pit[i].get('categories')
            if sub:
                p_prod_pit = prod_pit[i]['categories']
                for j in p_prod_pit:
                    cat_pp.append(j)
                    sub = p_prod_pit[j].get('categories')
                    if sub:
                        p_p_prod_pit = p_prod_pit[j]['categories']
                        for k in p_p_prod_pit:
                            cat_pp.append(k)
    return cat_pp

def rk_get_prod_data(data, categs):
    prod_data = []
    for product in data:
        if str(product['category']) in categs:
            pd_item = {
                'name': product['name'],
                'rate': round(float(product['points'])*20),
                'url': 'https://rskrf.ru/'+product['url']
            }
            prod_data.append(pd_item)
    return prod_data

def get_prod_data():
    print('====== ЧАСТЬ ПЕРВАЯ: РОСКОНТРОЛЬ =========')

    cats_url = rc_get_cat_urls()
    subcats_url = rc_get_subcat_urls(cats_url)
    prods_data_rc = rc_get_prod_data(subcats_url)

    print('====== ЧАСТЬ ПЕРВАЯ: РОСКАЧЕСТВО =========')

    prods_data_rk = rk_get_prod_data(rk_get_json_products(), rk_get_product_categories())

    prods_data = prods_data_rc + prods_data_rk
    return prods_data

def activ_urs():
    urls = []
    prods = ckdb.find()
    for i in prods:
        urls.append(i['url'])
    return urls


start = datetime.datetime.now()

#============== Получение данных о продуктах ===================
prod_data = get_prod_data()
#============== Добавление продуктов в базу ===================
ckdb.insert_many(prod_data)

finish = datetime.datetime.now()

good_prods = ckdb.find({'rate': {'$gt': 75}})


for i in good_prods:
    print(i)

delta = finish - start
print(delta.seconds)

# Почему не получается список? Как надо?
#urls.append(i['url'] for i in good_prods)
