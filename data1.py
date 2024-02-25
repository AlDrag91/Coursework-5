import psycopg2


class DBManager:
    def __init__(self, database='north', user='postgres', host='localhost', password=None, port=None):
        self.conn = psycopg2.connect(database=database, user=user, host=host, password=password, port=port)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("SELECT name_employers, open_vacancies FROM employers;")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
                 названия вакансии и зарплаты и ссылки на вакансию."""
        self.cur.execute("SELECT name_employers, name_vacancy, salary, vacancies_url FROM vacancies, employers;")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.cur.execute("SELECT AVG(salary) FROM vacancies;")
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT name_employers, name_vacancy, salary, vacancies_url FROM vacancies, employers WHERE salary > %s;",
                         (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        self.cur.execute(
            "SELECT name_employers, name_vacancy, salary, vacancies_url FROM vacancies, employers WHERE name_vacancy ILIKE %s;",
            ('%' + keyword + '%',))
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.conn.close()


