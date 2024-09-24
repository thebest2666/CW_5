import requests

from src.DBManager import DBManager
from src.Employer import Employer
from src.Employer_HH import Employer_HH
from src.Vacancy import Vacancy
from src.config import conns
from src.settings import DEFAULT_EMPLOYERS_LIST


def user_interaction():
    """
    Функция взаимодействия с пользователем
    """
    params = conns()
    db = DBManager(**params)

    hh_api = Employer_HH()

    hh_employers = []
    for i in DEFAULT_EMPLOYERS_LIST:
        hh_employers.append(hh_api.info_employer(i))

    employers_list = Employer.cast_to_object_employers(hh_employers)
    vacancies_list = []
    for i in hh_employers:
        response = requests.get(url=i["vacancies"])
        vacancies_list.extend(Vacancy.cast_to_object_vacancies(response.json()))
    db.save_employers(employers_list)
    db.save_vacancies(vacancies_list)

    print("Выберите один из пунктов меню")
    user_menu = input(
        """[1] Вывести список всех компаний и количество вакансий у каждой компании
    [2] Вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    [3] Вывести среднюю зарплату по вакансиям
    [4] Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
    [5] Вывести список всех вакансий, в названии которых содержатся переданные в метод слова, например python\n
    """
    )
    if user_menu == "1":
        data = db.get_companies_and_vacancies_count()
        data_string_list = [
            f"Работодатель: {d[1]}\nКоличество вакансий: {d[2]}" for d in data
        ]
        result = "\n\n".join(data_string_list)
        print(result)
    elif user_menu == "2":
        data = db.get_all_vacancies()
        data_all = [
            (f'Компания: {d[4]}\n Вакансия: {d[0]}\n, Минимальная зп: {d[1]}\n, Максимальная зп: {d[2]}\n,'
             f' Ссылка на вакансию: {d[3]}\n,') for d in data
        ]
        result = "\n\n".join(data_all)
        print(result)
    elif user_menu == "3":
        data = db.get_avg_salary()
        data_avg =[
            f"Средняя заработная плата составляет {d[0]}" for d in data
        ]
        result = "\n\n".join(data_avg)
        print(result)
    elif user_menu == "4":
        data = db.get_vacancies_with_higher_salary()
        data_vacancies_with_higher_salary = [
            f"{d[0]}" for d in data
        ]
        result = "\n\n".join(data_vacancies_with_higher_salary)
        print(result)
    elif user_menu == "5":
        user_filter = input("ВВедите ключевые слова для фильтрации вакансий\n")
        data = db.get_vacancies_with_keyword(user_filter)
        data_vacancies_with_keyword = [
            f"{d[0]}\n" for d in data
        ]
        result = "\n\n".join(data_vacancies_with_keyword)
        print(result)
    else:
        print("Ошибка ввода")
