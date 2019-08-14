from bs4 import BeautifulSoup as bs
import requests
import re

html = requests.get('https://ru.inshaker.com/cocktails?random_page=6&pagination=random&respond_with=body').text
parsed_html = bs(html, 'html.parser')

coctais = parsed_html.findAll(class_="cocktail-item")

print('Часть первая. Вывод всех коктейлей.')
print()

for i in coctais:
    print(i.findChild().getText())
    components = i.findChild().findNextSibling().findAll('a')
    print(', '.join(j.getText() for j in components))
    print('https://ru.inshaker.com'+i.findChild()['href'])

print('==============================')
print('Часть вторая. Вывод только тех, в составе которых или джин, или бурбон, или виски.')
print()

for i in coctais:
    components = i.findChild().findNextSibling().findAll('a')
    s = ', '.join(j.getText() for j in components)
    regs = re.compile('джин|бурбон|виски|Джин|Бурбон|Вискип')
#    print(s)
    if regs.search(s):
        print(i.findChild().getText())
        print(', '.join(j.getText() for j in components))
        print('https://ru.inshaker.com'+i.findChild()['href'])