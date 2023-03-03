import requests
from bs4 import BeautifulSoup
import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
}

    # запрос
url = "https://www.хакатоны.рф/"
response = requests.get(url, headers=headers)

    # сохраняем html
with open("page_content.html", "w", encoding="utf-8") as file:
     file.write(response.text)

    # открываем html
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
    info_hackathons.append({})
        # ищем div с названием хакатона
    name_of_hack = hackathon.find('div', class_='t776__title').find('div')
        # если имя есть, забираем текст и добавляем в список
    if name_of_hack:
        name = name_of_hack.text
        #names_of_hackathons.append(name)
    
    
        # ищем div с описанием
    '''place_of_hackathon = hackathon.find('div', class_='t776__descr').find('br')
    if place_of_hackathon:
        place = place_of_hackathon.previous_sibling
        if place is not None:
            place = place.strip()'''
            
    description = hackathon.find('div', class_='t776__descr')
    if description:
        for element in description:
            text = element.get_text(separator="\n")
            if text.strip():
                lines.append(text.strip())
                
    place = lines[0]
    info_hackathons[count_of_hackathons].update({'name': name, 'place': place})
    
    lines = lines[1:]
    for i in range(0, len(lines) - 1, 2):
        key = lines[i].strip(':')
        value = lines[i + 1]
        info_hackathons[count_of_hackathons].update({key: value})
        
    count_of_hackathons += 1
    
print(info_hackathons)
