import requests
from bs4 import BeautifulSoup


# class Page:
#     def __init__(self):
#         self.text = ""


def parse_subject(subject_name, subject_id):
    # page = Page()
    # with open("index.txt", encoding="utf-8") as f:
    #     page.text = f.read()
    url = "https://olimpiada.ru/article/1045"
    page = requests.get(url)
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
        # группируем олимпиады из одного раздела по номеру в перечне
        d = {}
        for elem in data:
            name, number, profile, subject, level = elem
            if number not in d:
                d[number] = [name, number, profile, subject, level]
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
parse_subject("Экономика", "econ")
# print(ref)
# # print(ref.find_all_next())
# res = ref.find("table", class_="note_table")
# print(res)
# soup.find_next_sibling(id=subject_id)
# print(soup.findAll("a"))
# table = soup.select_one(f"a:-soup-contains(id='geog')")
# print(table)