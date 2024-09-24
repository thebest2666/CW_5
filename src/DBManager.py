import psycopg2
from src.Vacancy import Vacancy


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        Функция инициализации класса DBManager
        """
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

    def create_table(self):
        """
        Функция, которая создает таблицы
        """
        cur = self.conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            url TEXT NOT NULL,
            company_id INT REFERENCES companies(id)
        );
        """
        )
        self.conn.commit()

    def save_employers(self, company_id):
        """
        Функция для добавления компаний в таблицу
        """
        cur = self.conn.cursor()
        for e in company_id:
            cur.execute(f"SELECT * FROM companies WHERE id = {e.id}")
            if cur.fetchall():
                continue
            cur.execute(
                """
                            INSERT INTO companies (id, name)
                            VALUES (%s, %s) 
                            
                     """,
                (e.id, e.name),
            )
        self.conn.commit()

    def save_vacancies(self, vacancies: list[Vacancy]):
        """
        Функция для записи вакансий в таблицу
        """
        cur = self.conn.cursor()
        for v in vacancies:
            cur.execute(f"SELECT * FROM vacancies WHERE id = {v.id}")
            if cur.fetchall():
                continue
            cur.execute(
                """
                    INSERT INTO vacancies (id, name, salary_min, salary_max, url, company_id)
                    VALUES (%s, %s, %s, %s, %s, %s)             
             """,
                (v.id, v.name, v.salary_min, v.salary_max, v.url, v.company_id),
            )
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """
        Функция, которая получает список всех компаний и количество вакансий у каждой компании
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT companies.id, companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.id
        """
        )
        return cur.fetchall()

    def get_all_vacancies(self):
        """
        Функция, которая получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT c.name, c.salary_min, c.salary_max, c.url, company.name
            FROM vacancies AS c
            JOIN companies AS company ON company.id = c.company_id  
        """
        )
        return cur.fetchall()

    def get_avg_salary(self):
        """
        Функция, которая получает среднюю зарплату по вакансиям
        """
        cur = self.conn.cursor()
        cur.execute(
            """
                    SELECT
                    ROUND(AVG(
                    CASE 
                        WHEN c.salary_min IS NOT NULL  AND c.salary_max IS NOT NULL THEN (c.salary_min + c.salary_max) / 2
                        WHEN c.salary_min IS NOT NULL THEN c.salary_max
                        WHEN c.salary_max IS NOT NULL THEN c.salary_min
                        ELSE 0
                    END
                    ), 2)    
                    FROM vacancies AS c
        """
        )
        return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """
        Функция, которая получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT name
            FROM vacancies AS c
            WHERE (c.salary_min + c.salary_max) > (%s)
        """,
            self.get_avg_salary(),
        )
        return cur.fetchall()

    def get_vacancies_with_keyword(self, user_filter: str) -> list:
        """
        Функция, которая получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например python
        """
        cur = self.conn.cursor()
        user_filter = f'%{user_filter}%'
        cur.execute(
            """
                    SELECT name
                    FROM vacancies 
                    WHERE name ILIKE %s 
                """,
            (user_filter,)
        )
        return cur.fetchall()
