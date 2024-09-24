import requests


class Employer_HH:
    """
    Класс для взаимодействия с HH через API
    """

    def __init__(self):
        """
        Функция инициализации
        """
        self.__url = "https://api.hh.ru/employers"

    def info_employer(self, employer_id):
        """
        Функция получения данных с HH
        """
        data = self.connect_hh(employer_id).json()
        result = {
            "id": data["id"],
            "name": data["name"],
            "vacancies": data["vacancies_url"],
        }
        return result

    def connect_hh(self, employer_id):
        """
        Функция для получения данных с HH по определенным параметрам
        """
        response = requests.get(f"{self.__url}/{employer_id}")
        return response

    @staticmethod
    def get_vacancies(search_query):
        params = {
            "text": search_query,
            "per_page": 5,
        }
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        return response.json()



