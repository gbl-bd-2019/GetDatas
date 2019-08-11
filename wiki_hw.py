from pprint import pprint
from lxml import html
import requests
import re

def get_link(topic):
    link='https://ru.wikipedia.org/wiki/'+topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html = requests.get(link).text
    return html

def get_other_page(link):
    html = requests.get(link).text
    return html

def get_topic_text(topic, start):
    if start:
        html_content = get_topic_page(topic)
    else:
        html_content = get_other_page(topic)
    words = re.findall("[а-яА-Я]{3,}",html_content)
    #text = ' '.join(words)
    return words

# text = get_topic_text('Дерево')
# print(len(text))
# print(text[0:1000])

def get_common_words(topic, start):
    words_list = get_topic_text(topic, start)
    rate={}
    for word in words_list:
        if word in rate:
            rate[word]+=1
        else:
            rate[word]=1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x: -x[1])
    return rate_list

def write_words(words_dict, f_name):
#    with open(rf'D:\{f_name}.txt', "w") as file:
    with open(rf'{f_name}.txt', "w") as file:
        for line in words_dict:
            file.write(str(line) + '\n')

def get_urls_and_names(topic):
    urls = []
    page = html.fromstring(get_topic_page(topic))
    page = page.xpath('//*[@id="Ссылки"]')
    page = page[0].getparent()
    page = page.getnext()
    page = page.getnext()
    page = page.getnext()
    page = page.getchildren()
    for elems in page:
        print(elems.getchildren()[0].text)
        urls.append([elems.getchildren()[0].text, elems.getchildren()[0].get('href')])
    return urls

#print(get_urls_and_names('Дерево'))

#wikw_page = 'Россия'
wikw_page = 'Дерево'
dict1 = get_common_words(wikw_page, True)
#dict2 = get_common_words('https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BD%D1%8C_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%B0', False)
#pprint(dict1)
print(wikw_page)
write_words(dict1, wikw_page)
#print('другое')
#write_words(dict2, 'Другое')

other_urls = get_urls_and_names(wikw_page)
for other in other_urls:
    dict2 = get_common_words(other[1], False)
    print(other[0])
    write_words(dict2, other[0])
