from database.datacoonect import db

class DictionaryContainerPhy:
    """Хранит количесвто задач по физики"""

    dictionary: dict = {}

    async def create_container(self)-> None:
        """Создаёт словарь в котором [номер задачи : количество задач]"""
        for i in range(1,21):
            if not i == 17:
                self.dictionary[i] = await db.count_task(i, "physics")
            
    async def get_item(self, key: int)-> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[key]

container_phy = DictionaryContainerPhy()