class Employer:

    def __init__(self, id, name):
        """
        Инициализация класса
        """
        self.name = name
        self.id = id

    @classmethod
    def cast_to_object_employers(cls, data: list) -> list:
        employers_list = []
        for e in data:
            employers_list.append(cls(id=e["id"], name=e["name"]))
        return employers_list

    def __str__(self):
        """
        Магический метод для строкового представления объекта
        """
        return f"Название компании: {self.name}"
