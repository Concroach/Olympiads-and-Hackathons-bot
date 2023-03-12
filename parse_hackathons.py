import requests
from bs4 import BeautifulSoup
import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
}

    # запрос
# url = "https://www.хакатоны.рф/"
# response = requests.get(url, headers=headers)

#     # сохраняем html
# with open("page_content.html", "w", encoding="utf-8") as file:
#     file.write(response.text)

 #   # открываем html
with open ('page_content.html', 'r', encoding="utf-8") as file:
    src = file.read()
    
    # находим все хакатоны // hackathons - список из html кода каждого хакатона
soup = BeautifulSoup(src, 'html.parser')
hackathons = soup.find_all('div', class_='t776__textwrapper')

info_hackathons = [] # список словарей с информацией о хакатонах
count_of_hackathons = 0 # число хакатонов

for hackathon in hackathons:
    info_hackathons.append({})
    lines = []
    # название хакатона
    name_of_hack = hackathon.find('div', class_='t776__title').find('div')
    if name_of_hack:
        name = name_of_hack.text
    # описание хакатона
    description = hackathon.find('div', class_='t776__descr')
    if description:
        for element in description:
            text = element.get_text(separator="\n")
            if text.strip():
                lines.append(text.strip())
    # место проведения
    place = lines[0]
    
    # добавляем в словарь название и место
    info_hackathons[count_of_hackathons].update({'name': name, 'place': place})
    
    # добавляем всю дргую инфу
    lines = lines[1:]
    lines = '\n'.join(lines)
    lines = lines.split('\n')
    lines = [t.strip() for t in lines if t.strip()]
    try:
        lines[lines.index('Редактировать:')] = 'Регистрация:'
    except:
        pass
    for i in range(0, len(lines) - 1, 2):
        key = lines[i].strip(':')
        value = lines[i + 1]
        info_hackathons[count_of_hackathons].update({key: value})
        
    count_of_hackathons += 1


month_dict = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}

# получаем даты проведения хакатонов
reg_dates = []
for event in info_hackathons:
    try:
        reg_date_str = event['Хакатон']
        reg_date_str = reg_date_str.replace("г.", "").replace("–", " ").replace("г", "").replace("с", "").replace("-", " ").strip().split()
        
        day = reg_date_str[0]
        for word in reg_date_str:
            if word in month_dict:
                month = month_dict[word]
                break
        year = reg_date_str[-1]
        if day is not None and month is not None:
            reg_date = datetime.date(year=int(year), month=int(month), day=int(day))
            reg_dates.append(reg_date)
    except Exception as ex:
        reg_dates.append(datetime.date(year=2000, month=1, day=1))
        
# получаем количество хакатонов, которые начинаются не менее, чем через 2 недели
id_hack = []
today = datetime.date.today()
for i in range(len(info_hackathons)):
    if reg_dates[i] - datetime.timedelta(days=14) > today:
        id_hack.append(i)
        
for i in info_hackathons[:len(id_hack)]:
    print(i)
