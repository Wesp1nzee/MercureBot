from database.datacoonect import db

from abc import ABC, abstractmethod

class DictionaryContainer(ABC):
    """Абстрактный класс"""
    @abstractmethod
    async def create_container(self)-> None:
        pass
    
    @abstractmethod
    async def get_item(self)-> int:
        pass

class DictionaryContainerInf(DictionaryContainer):
    """Хранит количесвто задач по информатики"""

    dictionary: dict = {}

    async def create_container(self)-> None:
        """Создаёт словарь в котором [номер задачи : количество задач в бд]"""
        for i in range(1,11):
            self.dictionary[i] = await db.count_task(i, "informatics")

    async def get_item(self, key)-> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[int(key)]


class DictionaryContainerPhy(DictionaryContainer):
    """Хранит количесвто задач по физики"""

    dictionary: dict = {}

    async def create_container(self)-> None:
        """Создаёт словарь в котором [номер задачи : количество задач в бд]"""
        for i in range(1,21):
            if not i in [17, 18]:
                self.dictionary[str(i)] = await db.count_task(i, "physics")
            else: 
                if i == 18:
                    for g in range(1,4):
                        self.dictionary['18' + '_' + str(g)] = await db.count_task('18' + '_' + str(g), "physics")

            
    async def get_item(self, key)-> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[str(key)]


container_inf = DictionaryContainerInf()
container_phy = DictionaryContainerPhy()