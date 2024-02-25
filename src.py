from pprint import pprint

from data import Receiving
from data1 import DBManager


def interaction():
    print("Программа вывода информации о компаниях и их вакансиях\n"
          "Компании о которых можно получить информацию:\n"
          "1C-Рарус\n"
          "Наука-Связь\n"
          "Kept (Кэпт)\n"
          "NielsenIQ\n"
          "СофтБаланс\n"
          "КОРУС Консалтинг\n"
          "Спектрум, Группа компаний\n"
          "АльфаСтрахование\n"
          "Медицина\n"
          "Nestle\n"
          "Дождитесь заполнение таблиц employers и vacancies")
    x = Receiving()
    x.data_employers()
    x.data_vacancies()

    while True:
        criteria = int(input("Продолжить работу - 1 Вход - 12"))
        y = DBManager()
        if criteria == 1:
            criteria = int(input('Получает список всех компаний и количество вакансий у каждой компании. - 1\n'
                                 'Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию. - 2\n'
                                 'Получает среднюю зарплату по вакансиям.- 3\n'
                                 'Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.- 4\n'
                                 'Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например Инженер - 5\n'))
            if criteria == 1:
                t = y.get_companies_and_vacancies_count()
                pprint(t)
            if criteria == 2:
                q = y.get_all_vacancies()
                pprint(q)
            if criteria == 3:
                a = y.get_avg_salary()
                print(round(a, 2))
            if criteria == 4:
                e = y.get_vacancies_with_higher_salary()
                pprint(e)
            if criteria == 5:
                key = input('Введите ключевое слово например: Инженер\n')
                r = y.get_vacancies_with_keyword(key)
                pprint(r)
            else:
                pass
        if criteria == 12:
            break
