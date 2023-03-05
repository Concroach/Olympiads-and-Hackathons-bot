import requests
from bs4 import BeautifulSoup
import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
}

    # запрос
#url = "https://www.хакатоны.рф/"
#response = requests.get(url, headers=headers)

    # сохраняем html
#with open("page_content.html", "w", encoding="utf-8") as file:
#     file.write(response.text)

 #   # открываем html
with open ('page_content.html', 'r', encoding="utf-8") as file:
    src = file.read()
    
    # находим все хакатоны // hackathons - список из html кода каждого хакатона
soup = BeautifulSoup(src, 'html.parser')
hackathons = soup.find_all('div', class_='t776')

    # названия хакатонов 
info_hackathons = []
count_of_hackathons = 0

    # перебираем каждый хакатон
for hackathon in hackathons:
    lines = []
        # ищем div с названием хакатона
    name_of_hack = hackathon.find('div', class_='t776__title').find('div')
        # если имя есть, забираем текст и добавляем в список
    if name_of_hack:
        name = name_of_hack.text
    false_names = ['ХАКАТОН ДЛЯ ПРОГРАММИСТОВ-РОБОТОТЕХНИКОВ «РОСНЕФТИ»!', 'HackWagon22', 'Tender Hack Москва', 'Всероссийский хакатон', 'FIT - M 2022', 'PRO_НАНО', 'Югорский хакатон «ХАНТАТОН – 2022»',
                   'Приборостроение – 2023', 'Культурно-образовательный хакатон «История будущего»', 'Hackathon </beCoder> 2022', 'Data Fusion Contest 2023', '2022']
    if name in false_names:
        continue
    
    info_hackathons.append({})
    
    description = hackathon.find('div', class_='t776__descr')
    if description:
        for element in description:
            text = element.get_text(separator="\n")
            if text.strip():
                lines.append(text.strip())
                
    place = lines[0]
    
    info_hackathons[count_of_hackathons].update({'name': name, 'place': place})
    
    lines = lines[1:]
    lines = '\n'.join(lines)
    lines = lines.split('\n')
    lines = [t.strip() for t in lines if t.strip()]
    if count_of_hackathons == 0 or count_of_hackathons == 1:
        lines[lines.index('Редактировать:')] = 'Регистрация:'
    for i in range(0, len(lines) - 1, 2):
        key = lines[i].strip(':')
        value = lines[i + 1]
        info_hackathons[count_of_hackathons].update({key: value})
        
    count_of_hackathons += 1

#print(info_hackathons)
# Create a dictionary to convert month names to numbers
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

reg_dates = []

for event in info_hackathons:
    try:
        reg_date_str = event['Регистрация']
        
        words = reg_date_str.split()
        
        day = None
        month = None
        
        for word in words:
            if word.isdigit() and (len(word) == 1 or len(word) == 2):
                day = int(word)
            elif word in month_dict:
                month = month_dict[word]
            if day is not None and month is not None:
                reg_date = datetime.date(year=2023, month=month, day=day)
                reg_dates.append(reg_date)
    except:
        reg_dates.append(datetime.date(year=2000, month=1, day=1))
        
today = datetime.date.today()
for i in range(len(info_hackathons)):
    if reg_dates[i] < today:
        if len(info_hackathons) > i:
            del info_hackathons[i]

print(info_hackathons)