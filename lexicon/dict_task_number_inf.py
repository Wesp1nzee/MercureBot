from database.datacoonect import db

class DictionaryContainerInf:
    """Хранит количесвто задач по информатики"""

    dictionary: dict = {}

    async def create_container(self)-> None:
        """Создаёт словарь в котором [номер задачи : количество задач]"""
        for i in range(1,11):
            self.dictionary[i] = await db.count_task(i, "informatics")

    async def get_item(self, key: int)-> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[key]

container_inf = DictionaryContainerInf()
