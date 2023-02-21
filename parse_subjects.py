from bs4 import BeautifulSoup
import requests


# class Page:
#     def __init__(self):
#         self.text = ""


url = "https://olimpiada.ru/article/1045"
page = requests.get(url)
if page:
    # with open("index.txt", "w", encoding="utf-8") as f:
    #     f.write(page.text)
    # soup = BeautifulSoup(page.text, "lxml")
    # print(soup.find("table", class_="note_table"))
    # page = Page()
    # with open("index.txt", encoding="utf-8") as f:
    #     page.text = f.read()
    soup = BeautifulSoup(page.text, "lxml")
    html_subjects = soup.find("table", class_="note_table")  # таблица с названиями предметов (html-строки)
    subjects_names = []  # сами названия и их id(для дальнейшего поиска)
    for elem in html_subjects.findAll("a"):
        subjects_names.append((elem.text, elem.get("href")[1:]))
    with open("list_of_subjects.txt", "w", encoding="utf-8") as f:
        for subject_name in subjects_names:
            f.write(subject_name[0] + ";" + subject_name[1] + "\n")
else:
    print(page.status_code, page.reason)