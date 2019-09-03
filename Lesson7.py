import matplotlib.pyplot as plt
import csv
# import datetime.date
# from datetime import datetime
import datetime

regions = set()
names = set()
with open('opendata.csv','r') as f:
    reader=csv.DictReader(f)
    field_names = reader.fieldnames
    for row in reader:
        regions.add(row['region'])
        names.add(row['name'])

# regdort = list(regions).sort()

regions = sorted(regions)
names = sorted(names)

# print(regions)
# print(regions[-1])

nom1 = 1
for i in regions:
    print(nom1, i)
    nom1 = nom1 + 1
sel_reg = int(input('Выберите регион (введите число): ')) - 1

nom1 = 1
for i in names:
    print(nom1, i)
    nom1 = nom1 + 1
sel_name = int(input('Выберите интересующие данные (введите число): ')) - 1

# print(regions[sel_reg], names[sel_name])

dates = []
with open('opendata.csv','r') as f:
    reader=csv.DictReader(f)
    field_names = reader.fieldnames
    for row in reader:
        if (row['name'] == names[sel_name] and
            row['region'] == regions[sel_reg]):
                dates.append(datetime.datetime.strptime(row['date'], '%Y-%m-%d').date())

# print(dates)

# d_min = '01.01.2016'
print(f"Возможный диапазон дат: {dates[0].strftime('%d.%m.%y')} - {dates[-1].strftime('%d.%m.%y')}")
sel_dates = input('введите интересующий диапазон в формате ДД.ММ.ГГ - ДД.ММ.ГГ: ')
d_min = sel_dates[:8]
d_max = sel_dates[11:]

# print(d_min, d_max)

g_d_min = datetime.datetime.strptime(d_min,'%d.%m.%y').date()
g_d_max = datetime.datetime.strptime(d_max,'%d.%m.%y').date()

#
# print(regions)
# print(names)

print(regions[sel_reg] + ', ' + names[sel_name])
with open('opendata.csv','r') as f:
    reader=csv.DictReader(f)
    field_names = reader.fieldnames
    print(field_names)
    money = []
    date = []
    # graph = []

    for row in reader:
        g_date = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
        if (row['name'] == names[sel_name] and
            row['region'] == regions[sel_reg] and
            (g_date > g_d_min and g_date < g_d_max)):
            # graph.append([row['date'], row['value']])
            print(row['date'] + ': ' + row['value'])
            date.append(row['date'])
            money.append(int(row['value']))


# print(datetime.date())
# print(datetime.datetime.strptime(date[0],'%Y-%m-%d').date())
# print(date(datetime.strptime(date[0],'%Y-%m-%d')))
# print(graph[1])

plt.plot(date,money)
# plt.plot(graph[0], graph[1])
plt.show()