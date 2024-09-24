class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(
        self,
        id: str,
        name: str,
        url: str,
        salary_min: str,
        salary_max: str,
        employer_id: str,
    ):
        self.id = id
        self.name = name
        self.url = url
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.company_id = employer_id

    @classmethod
    def cast_to_object_vacancies(cls, data: dict) -> list:
        vacancies_list = []
        for v in data["items"]:
            if v["salary"] is None:
                salary_min = 0
                salary_max = 0
            elif v["salary"]["from"] is None and v["salary"]["to"] is not None:
                salary_min = 0
                salary_max = v["salary"]["to"]
            elif v["salary"]["from"] is not None and v["salary"]["to"] is None:
                salary_max = 0
                salary_min = v["salary"]["from"]
            else:

                salary_max = v["salary"]["to"]
                salary_min = v["salary"]["from"]
            vacancies_list.append(
                cls(
                    id=v["id"],
                    name=v["name"],
                    url=v["url"],
                    salary_min=salary_min,
                    salary_max=salary_max,
                    employer_id=v["employer"]["id"],
                )
            )
        return vacancies_list

    def __str__(self):
        """
        Магический метод для строкового представления объекта
        """
        return f"""Название вакансии: {self.name}, 
    Ссылка на вакансию: {self.url},
    Заработная плата: {self.salary_max}"""
