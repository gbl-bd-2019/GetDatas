from zeep import Client
from datetime import timedelta, datetime
from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['curxes_l4']
ldb = db.curxes_l4

def curs_max_min(curs_val):
    max = [0, '']
    min = [1000, '']
    for i in curs_val:
        if float(i['curs']) > max[0]:
            max[0] = float(i['curs'])
            max[1] = i['date']
        if float(i['curs']) < min[0]:
            min[0] = float(i['curs'])
            min[1] = i['date']
    return [min, max]

def get_curses(str_date_start, str_date_finish):
    url='https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
    client = Client(url)
    st_date = datetime.strptime(str_date_start, '%Y-%m-%d')
    fin_date = datetime.strptime(str_date_finish, '%Y-%m-%d')
    st_date = datetime.date(st_date)
    fin_date = datetime.date(fin_date)
    curses = []
    for i in range((fin_date - st_date).days + 1):
        in_date = st_date + timedelta(i)
        money = client.service.GetCursOnDate(str(in_date))
        list_money = money._value_1._value_1
        for item in list_money:
            for v in item.values():
                if v.VchCode == 'USD':
                    curs = item['ValuteCursOnDate']['Vcurs']
                    curses.append({
                        'date': str(in_date),
                        'curs': str(curs)
                    })
    return curses

def out_str(inp_delta):
    delr = float(inp_delta[0][0]) - float(inp_delta[1][0])
    if delr < 0:
        delr = -delr
    st_date = datetime.strptime(inp_delta[0][1], '%Y-%m-%d')
    fin_date = datetime.strptime(inp_delta[1][1], '%Y-%m-%d')
    st_date = datetime.date(st_date)
    fin_date = datetime.date(fin_date)
    if st_date > fin_date:
        valt = 'доллары'
    if st_date < fin_date:
        valt = 'рубли'
    return f'¬ыгодно было купить {valt} {str(inp_delta[0][1])} и продать {inp_delta[1][1]}, заработав по {delr} с доллара'

curses = get_curses('2019-06-18', '2019-08-24')
ldb.insert_many(curses)  # к пункту  1

delta = curs_max_min(curses) # к пункту 2

print(out_str(delta)) # к пункту 3
