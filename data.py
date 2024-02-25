from abc import ABC, abstractmethod

import psycopg2
import requests


class AbstractJobAPI(ABC):

    @abstractmethod
    def get_data(self):
        pass


class SiteAPIHH(AbstractJobAPI):
    """Подключение и передача параметров ресурсу hh.ru"""

    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    def get_data(self) -> dict:
        req = requests.get(self.url, self.params)
        if req.status_code == 200:
            data = req.json()
            req.close()
            return data
        else:
            raise Exception("Ошибка: Запрос не выполнен.")


class Receiving:
    """Получение информации и запись в БД"""

    def __init__(self, database='north', user='postgres', host='localhost', password=None, port=None):
        self.url_employers = 'https://api.hh.ru/employers/'
        self.url_vacancies = 'https://api.hh.ru/vacancies'
        self.conn = psycopg2.connect(database=database, user=user, host=host, password=password, port=port)
        self.cur = self.conn.cursor()
        self.id_employers = [172, 15, 201, 257, 343, 675, 370, 362, 330, 688]

    def data_employers(self) -> None:
        """Получение информации о кампании и заполнение таблицы employers"""

        try:
            self.cur.execute(
                'CREATE TABLE employers (id_employers INT PRIMARY KEY, name_employers VARCHAR, open_vacancies INT, employers_url VARCHAR)')
            for id_employer in self.id_employers:
                url = (self.url_employers + str(id_employer))
                site_employers = SiteAPIHH(url)
                x = site_employers.get_data()
                self.cur.execute(
                    'INSERT INTO employers (id_employers, name_employers, open_vacancies, employers_url) VALUES (%s, %s, %s, %s)',
                    (id_employer, x['name'], x['open_vacancies'], x['alternate_url']))
            self.conn.commit()
            print('Таблица employers заполнена!')
        except Exception:
            print('Таблица employers создана!')

    def data_vacancies(self) -> None:
        """Получение информации о вакансии и заполнение таблицы vacancies"""
        try:
            self.cur.execute(
                'CREATE TABLE vacancies (id_employers VARCHAR, name_vacancy VARCHAR, salary INT, vacancies_url VARCHAR)')
            for id_employer in self.id_employers:
                for page in range(0, 20):
                    params_vacancies = {'employer_id': {id_employer}, 'per_page': 100, 'page': page}
                    site_vacancies = SiteAPIHH(self.url_vacancies, params_vacancies)
                    data_vacancies = site_vacancies.get_data()['items']
                    for data_vacancy in data_vacancies:
                        name_vacancy = data_vacancy['name']
                        alternate_url = data_vacancy['alternate_url']
                        if data_vacancy['salary'] is None:
                            salary = None
                        else:
                            salary = data_vacancy['salary']['from']

                        self.cur.execute(
                            'INSERT INTO vacancies (id_employers, name_vacancy, salary, vacancies_url) VALUES (%s, %s, %s, %s)',
                            (id_employer, name_vacancy, salary, alternate_url))
                        self.conn.commit()
            print('Таблица vacancies заполнена!')
        except Exception:
            print('Таблица vacancies создана!')
