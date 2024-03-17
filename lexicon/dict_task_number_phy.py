from database.datacoonect import db

class DictionaryContainerPhy:
    """Хранит количесвто задач по физики"""

    def __init__(self):
        self.dictionary = {}

    async def create_container(self):
        for i in range(1,21):
            if not i == 17:
                self.dictionary[i] = await db.count_task(i, "physics")
            
    async def get_item(self, key):
        return self.dictionary.get(key)

container_phy = DictionaryContainerPhy()