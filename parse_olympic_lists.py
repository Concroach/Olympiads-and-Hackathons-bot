import requests
from bs4 import BeautifulSoup
import cfscrape


class Page:
    def __init__(self):
        self.text = ""


def parse_subject(subject_name, subject_id):
    # page = Page()
    # with open("index.txt", encoding="utf-8") as f:
    #     page.text = f.read()
    url = "https://olimpiada.ru/article/1045"
    scraper = cfscrape.create_scraper(delay=5)
    page = scraper.get(url)
    # page = requests.get(url)
    if page:
        soup = BeautifulSoup(page.text, "lxml")
        ref = soup.select("a#" + subject_id)[0]  # нужный заголок
        table = ref.find_next("table", class_="note_table")  # Нужная таблица
        # данные из таблицы (название, номер из перечня, профиль, предмет, уровень)
        data = []
        for line in table.find_all("tr"):
            data.append([])
            for value in line.find_all("td"):
                data[-1].append(value.text.strip())
            # на отдельной странице олимпиады ищем классы участия и ссылку на сайт
            link = line.findAll("a", class_="slim_dec",href=True)
            if len(link):
                href_value = link[0].get("href")
                olymp_url = "https://olimpiada.ru" + href_value
                olymp_page = requests.get(olymp_url)
                # olymp_page = Page()
                # with open("olymp.txt", encoding="utf-8") as f:
                #     olymp_page.text = f.read()
                if olymp_page:
                    # with open("olymp.txt", "w", encoding="utf-8") as f:
                    #     f.write(olymp_page.text)
                    #                 print(href_value)
                    # olymp_page = Page()
                    # with open("olymp.txt", encoding="utf-8") as f:
                    #     olymp_page.text = f.read()
                    soup_olymp = BeautifulSoup(olymp_page.text, "lxml")

                    # классы участия
                    classes = soup_olymp.find("span", class_="classes_types_a").text
                    data[-1].append(classes.strip())

                    # ссылка на сайт
                    all_contacts = soup_olymp.findAll("span", class_="bold timetableH2")
                    for contact in all_contacts:
                        if contact.text == "Контакты":
                            site = contact.find_next("a", class_="color").get("href")
                            data[-1].append(site.strip()) 
                else:
                    print(olymp_page.status_code, olymp_page.reason)
                # print(href_value)
                # olymp_page = Page()
                # with open("olymp.txt", encoding="utf-8") as f:
                #     olymp_page.text = f.read()
                # soup_olymp = BeautifulSoup(olymp_page.text, "lxml")
                # classes = soup_olymp.find("span", class_="classes_types_a").text
                # data[-1].append(classes.strip())
                
            else:
                data[-1].append("Класс")
                data[-1].append("Ссылка на сайт")
        # группируем олимпиады из одного раздела по номеру в перечне
        d = {}
        for elem in data:
            name, number, profile, subject, level, olymp_classes, site = elem
            if number not in d:
                d[number] = [name, number, profile, subject, level, olymp_classes, site]
            else:
                d[number][2] += ', ' + profile  # добавляем профиль
                if subject not in d[number][3]:
                    d[number][3] += ', ' + subject
        # переносим словарь в массив
        grouped_data = []
        for _, val in d.items():
            grouped_data.append(val)
        # обрабатываем профили и предметы. Если строка получается слишком длинной, меняем её на более общую фразу
        for elem in grouped_data:
            if len(elem[2]) > 30:  # профилей много -> Многопрофильная
                elem[2] = "Многопрофильная"
            if len(elem[3]) > 30:  # предметов много -> Межпредметная
                elem[3] = "Межпредметная"
        # записываем обработанные данные в файл
        with open(f"olymps_info/{subject_name}.txt", "w", encoding="utf-8") as f:
            for elem in grouped_data:
                f.write(";".join(elem) + "\n")
    else:
        print(page.status_code, page.reason)


# в функции первый параметр - название предмета, второй - id предмета в html коде
parse_subject("Информатика", "iikt")
# print(ref)
# # print(ref.find_all_next())
# res = ref.find("table", class_="note_table")
# print(res)
# soup.find_next_sibling(id=subject_id)
# print(soup.findAll("a"))
# table = soup.select_one(f"a:-soup-contains(id='geog')")
# print(table)