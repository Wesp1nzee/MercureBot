from database.datacoonect import db
import json
from abc import ABC, abstractmethod


class DictionaryContainer(ABC):
    """Абстрактный класс"""

    @abstractmethod
    async def create_container(self) -> None:
        pass

    @abstractmethod
    async def get_item(self) -> int:
        pass


class DictionaryContainerInf(DictionaryContainer):
    """Хранит количесвто задач по информатики"""

    __slots__ = "dictionary"

    def __init__(self) -> None:
        self.dictionary = {}

    async def create_container(self) -> None:
        """Создаёт словарь в котором [номер задачи : количество задач в бд]"""
        for i in range(1, 11):
            self.dictionary[i] = await db.count_task(i, "informatics")

    async def get_item(self, key) -> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[int(key)]
    
    async def get_value(self) -> int:
        """Извлекает из словаря суму всех задач"""
        return sum(self.dictionary.values())


class DictionaryContainerPhy(DictionaryContainer):
    """Хранит количесвто задач по физики"""

    __slots__ = "dictionary"

    def __init__(self) -> None:
        self.dictionary = {}

    async def create_container(self) -> None:
        """Создаёт словарь в котором [номер задачи : количество задач в бд]"""
        for i in range(1, 21):
            if not i in [17, 18]:
                self.dictionary[str(i)] = await db.count_task(i, "physics")
            else:
                if i == 18:
                    for g in range(1, 4):
                        self.dictionary[f"18_{str(g)}"] = await db.count_task(
                            f"18_{str(g)}", "physics"
                        )
                json_object = json.dumps(self.dictionary, indent=4)
                with open("sample2.json", "w") as outfile:
                    outfile.write(json_object)

    async def get_item(self, key) -> int:
        """Извлекает из словаря количество задач по данному номеру"""
        return self.dictionary[str(key)]
    
    async def get_value(self) -> int:
        """Извлекает из словаря суму всех задач"""
        return sum(self.dictionary.values())


container_inf = DictionaryContainerInf()
container_phy = DictionaryContainerPhy()